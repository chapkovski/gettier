from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random, json, datetime


class DecisionPage(Page):
    def is_displayed(self):
        return not self.player.unmatched


class SkipPage(Page):
    def is_displayed(self):
        return self.player.unmatched


class GroupingWaitPage(WaitPage):
    _allow_custom_attributes = True
    body_text = 'Waiting for another participant...'
    group_by_arrival_time = True
    template_name = 'my_simple_survey/wp.html'
    settings = None
    # some defaults for pay per pin and min before allowed to leave:
    pay_per_min = .1
    wait_before_leave = 30

    # def dispatch(self, *args, **kwargs):
    #     super().dispatch(*args, **kwargs)
    #     if self.request.method == 'POST':
    #         end_of_game = self.request.POST.dict().get('endofgame')
    #         if end_of_game is not None:
    #             models.Player.objects.filter(pk=self.player.pk).update(early_finish=True)
    #     response = super().dispatch(*args, **kwargs)
    #     return response

    def record_secs_waited(self, p):
        p.sec_spent = int((
                                  datetime.datetime.now(datetime.timezone.utc) - p.wp_timer_start).total_seconds())

        p.sec_earned = int(round(p.sec_spent / 60 * self.pay_per_min, 2))

    def is_displayed(self):
        if self.player.early_finish:
            return False
        self._is_frozen = False
        self.settings = json.loads(self.subsession.settings)
        self.pay_per_min = self.settings.get('pay_per_min', self.pay_per_min)
        self.wait_before_leave = self.settings.get('wait_before_leave', self.wait_before_leave)
        if not self.player.wp_timer_start:
            self.player.wp_timer_start = datetime.datetime.now(datetime.timezone.utc)
        self.record_secs_waited(self.player)
        return True

    def vars_for_template(self):
        return {'time_left': max(self.wait_before_leave - self.player.sec_spent, 0)}

    def get_players_for_group(self, waiting_players):
        for w in waiting_players:
            self.record_secs_waited(w)

        waiting_players.sort(key=lambda p: p.participant.vars.get('timestamp_answer'))
        true_players = [p for p in waiting_players if p.participant.vars.get('is_it_knowledge')]
        false_players = [p for p in waiting_players if not p.participant.vars.get('is_it_knowledge')]
        if len(true_players) >= 1 and len(false_players) >= 1:
            passers = true_players[:1] + false_players[:1]
            for p in passers:
                p.in_wp = False
                p.unmatched = False
                p.wp_passed = True
                p.save()
            return passers
        if self.session.mturk_num_participants != -1:
            num_participants = self.session.mturk_num_participants
        else:
            num_participants = len(self.session.get_participants())
        answered = [p for p in self.session.get_participants() if p.vars.get('is_it_knowledge') != None]
        left = num_participants - len(answered)
        if left <= 0:
            losers = waiting_players
            for l in losers:
                l.unmatched = True
                l.save()
            return losers


class Chats(DecisionPage):
    # def get_timeout_seconds(self):
    #     settings = json.loads(self.subsession.settings)
    #     return settings['max_chat_sec']

    def vars_for_template(self):
        p = self.participant
        partner = self.player.other.participant
        choices = dict(p.vars['choices_order'])
        user_answer = choices[p.vars['is_it_knowledge']]
        another_answer = choices[partner.vars['is_it_knowledge']]

        settings = json.loads(self.subsession.settings)

        return {'chat_instructions': settings['chat_instructions'],
                'vignette': settings['vignette'],
                'min_chat_sec': settings['min_chat_sec'],
                'pay_per_word': settings['pay_per_word'],
                'user_answer': user_answer,
                'another_answer': another_answer}

    def before_next_page(self):
        self.player.reach_payoff = Constants.reach_payoff
        self.group.set_chat_payoff()


class EndSurvey(DecisionPage):
    form_model = 'player'
    form_fields = ['is_it_still_knowledge', 'still_confidence', 'reason', 'experience', ]

    def is_it_still_knowledge_choices(self):
        choices = self.participant.vars['choices_order']
        return choices

    def vars_for_template(self):
        settings = json.loads(self.subsession.settings)
        still_confidence_label = 'How confident are you  in your answer?'
        return {'vignette': settings['vignette'],
                'isitknowledgelabel': settings['label'],
                'still_confidence_label': still_confidence_label
                }


class DemographicInfo(DecisionPage):
    form_model = 'player'
    form_fields = ['age', 'gender', 'education', ]


class Results(DecisionPage):
    def is_displayed(self):
        if not self.player.payoff_set:
            self.player.set_payoff()
            self.player.payoff_set = True

        return super().is_displayed()


class ExitPage(SkipPage):
    def is_displayed(self):
        return super().is_displayed() and not self.player.early_finish


class EarlyFinish(SkipPage):
    def is_displayed(self):
        return self.player.early_finish


page_sequence = [
    GroupingWaitPage,
    Chats,
    EndSurvey,
    DemographicInfo,
    Results,
    ExitPage,
    EarlyFinish,
]
