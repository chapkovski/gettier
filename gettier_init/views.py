from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from otreeutils.surveys import SurveyPage, setup_survey_pages

class DemographicInfo (Page):
    pass

class SurveyPage1(SurveyPage):
    pass

class ExitPage (Page):
      def is_displayed(self):
        self.session.vars['isExcess'] = False
        if self.player.isItKnowledge == 'True':
            self.participant.vars['isItKnowledge'] = 'True'
            self.session.vars['knows'] += 1
            if self.session.vars['knows'] - self.session.vars['notKnows'] > 2:
                self.session.vars['isExcess'] = True
        else:
            self.participant.vars['isItKnowledge'] = 'False'
            print('*******participant.vars is', self.participant.vars['isItKnowledge'])
            self.session.vars['notKnows'] += 1
            if self.session.vars['notKnows'] - self.session.vars['knows'] > 2:
                self.session.vars['isExcess'] = True
        return self.session.vars['isExcess']


survey_pages = [
    SurveyPage1,
]

last_page = [
    ExitPage,
]

setup_survey_pages(models.Player, survey_pages)

page_sequence = [
    DemographicInfo,
]

page_sequence.extend(survey_pages)
page_sequence.extend(last_page)