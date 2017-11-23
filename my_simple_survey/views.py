from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class DecisionPage(Page):
    def is_displayed(self):
        return not self.player.unmatched


class SkipPage(Page):
    def is_displayed(self):
        return self.player.unmatched


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def get_players_for_group(self, waiting_players):

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
    def get_timeout_seconds(self):
        return self.session.config.get('chat_seconds', 120)


    def vars_for_template(self):
        # award bonus to anyone who makes it this far
        self.player.payoff = Constants.reach_payoff


class EndSurvey(DecisionPage):
    form_model = models.Player
    form_fields = ['is_it_still_knowledge', 'reason', 'experience', ]


class DemographicInfo(DecisionPage):
    form_model = models.Player
    form_fields = ['age', 'gender', 'education', ]


class ExitPage(SkipPage):
    pass


page_sequence = [
    GroupingWaitPage,
    Chats,
    EndSurvey,
    DemographicInfo,
    ExitPage,
]
