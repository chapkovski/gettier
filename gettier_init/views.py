from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

from otreeutils.surveys import SurveyPage, setup_survey_pages

class MyPage(SurveyPage):
    pass

class ExitPage (Page):
    def is_displayed(self):
        if self.player.isItKnowledge:
            self.session.vars['knows'] += 1
            if self.session.vars['knows'] - self.session.vars['notKnows'] > 2: self.player.isExcess = True
        else:
            self.session.vars['notKnows'] += 1
            if self.session.vars['notKnows'] - self.session.vars['knows'] > 2: self.player.isExcess = True
        return self.player.isExcess

survey_pages = [
    MyPage
]

setup_survey_pages(models.Player, survey_pages)

page_sequence = [
]

page_sequence.extend(survey_pages)
page_sequence.extend(ExitPage)