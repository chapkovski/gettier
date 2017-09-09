from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def get_players_for_group(self, waiting_players):

        true_players = [p for p in waiting_players if p.participant.vars['isItKnowledge']]
        false_players = [p for p in waiting_players if not p.participant.vars['isItKnowledge']]
        if len(true_players) >= 1 and len(false_players) >= 1:
            # this is a Python "list slice"
            return true_players[:1] + false_players[:1]

    def is_displayed(self):
        return self.round_number == 1


class Chats(Page):
    timeout_seconds = 120
    pass


class EndSurvey(Page):
    form_model = models.Player
    form_fields = ['isItStillKnowledge']

page_sequence = [
    GroupingWaitPage,
    Chats,
    EndSurvey
]
