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
        for w in waiting_players:
            w.in_wp = True
        true_players = [p for p in waiting_players if p.participant.vars.get('is_it_knowledge')]
        false_players = [p for p in waiting_players if not p.participant.vars.get('is_it_knowledge')]
        if len(true_players) >= 1 and len(false_players) >= 1:
            passers = true_players[:1] + false_players[:1]
            for p in passers:
                p.unmatched = False
                p.wp_passed = True
                p.in_wp = False
            return passers
            # unmatched = [p for p in self.subsession.get_players() if not p.wp_passed]
            # print('HOW MANY UNMATCHED: ', len(unmatched))
            # diff = len(waiting_players) - len(unmatched)
            # if diff > 0:
            #     print('IM IN DROPPERS')
            #     # choose_size = (len(waiting_players), diff)
            #     droppers = random.sample(waiting_players, diff)
            #     print('DROPPERS: ', droppers)
            #     for i in droppers:
            #         i.in_wp = False
            #         i.unmatched = True
            #     return droppers

    def is_displayed(self):
        if self.session.mturk_num_participants !=-1:
            num_participants=self.session.mturk_num_participants
        else:
            num_participants = self.session.num_participants
        self.player.wp_passed = True
        unmatched = [p for p in self.subsession.get_players() if not p.wp_passed]
        wp = [p for p in self.subsession.get_players() if p.in_wp]
        passed = [p for p in self.subsession.get_players() if p.wp_passed]
        rest = num_participants-len(wp)-len(passed)
        if rest < len(wp):
            self.player.unmatched = True
            self.player.wp_passed = True
            return False
        return self.round_number == 1


class Chats(DecisionPage):
    timeout_seconds = 240

    def vars_for_template(self):
        # award bonus to anyone who makes it this far
        self.player.payoff = Constants.reach_payoff


class EndSurvey(DecisionPage):
    form_model = models.Player
    form_fields = ['is_it_still_knowledge', 'reason', 'experience', ]


class DemographicInfo(DecisionPage):
    form_model = models.Player
    form_fields = ['age', 'gender', 'age', 'education', ]


class ExitPage(SkipPage):
    ...


page_sequence = [
    GroupingWaitPage,
    Chats,
    EndSurvey,
    DemographicInfo,
    ExitPage,
]
