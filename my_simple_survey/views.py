from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from otreeutils.surveys import SurveyPage, setup_survey_pages

class GroupingWaitPage(WaitPage):

    group_by_arrival_time = True

    def get_players_for_group(self, waiting_players):

        true_players = [p for p in waiting_players if p.participant.vars['isItKnowledge'] == 'True']
        false_players = [p for p in waiting_players if p.participant.vars['isItKnowledge'] == 'False']
        if len(true_players) >= 1 and len(false_players) >= 1:
            # this is a Python "list slice"
            return true_players[:1] + false_players[:1]

    def is_displayed(self):
        return self.round_number == 1 and self.participant.vars['movingOn'] == 'True'


class Chats(Page):
    def is_displayed(self):
        return self.participant.vars['movingOn'] == 'True'
    timeout_seconds = 120
    pass


class EndSurvey(SurveyPage):
    def is_displayed(self):
        return self.participant.vars['movingOn'] == 'True'
    pass


survey_pages = [
    EndSurvey,
]

setup_survey_pages(models.Player, survey_pages)

page_sequence = [
    GroupingWaitPage,
    Chats,
]

page_sequence.extend(survey_pages)