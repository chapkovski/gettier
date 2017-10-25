from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def get_players_for_group(self, waiting_players):
        true_players = [p for p in waiting_players if p.participant.vars.get('is_it_knowledge')]
        false_players = [p for p in waiting_players if not p.participant.vars.get('is_it_knowledge')]
        if len(true_players) >= 1 and len(false_players) >= 1:
            return true_players[:1] + false_players[:1]

    def is_displayed(self):
        return self.round_number == 1


class Chats(Page):
    def is_displayed(self):
        # award bonus to anyone who makes it this far
        self.player.payoff = Constants.reach_payoff
        return True

    timeout_seconds = 240
    pass


class EndSurvey(Page):
    form_model = models.Player
    form_fields = ['is_it_still_knowledge', 'reason', 'experience', ]


class DemographicInfo(Page):
    form_model = models.Player
    form_fields = ['age', 'gender', 'age', 'education', ]


class ExitPage(Page):
    def is_displayed(self):
        return False


page_sequence = [
    GroupingWaitPage,
    Chats,
    EndSurvey,
    DemographicInfo,
    ExitPage,
]
