from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from otreeutils.surveys import SurveyPage, setup_survey_pages


class DemographicInfo(SurveyPage):
    pass

class Vignette(Page):
    pass

class SurveyPage1(SurveyPage):
    pass


class ExitPage (Page):
      def is_displayed(self):
        self.session.vars['isExcess'] = False
        if self.player.isItKnowledge == 'True':
            self.participant.vars['isItKnowledge'] = 'True'
            self.session.vars['knows'] += 1
            if self.session.vars['knows'] - self.session.vars['notKnows'] > 5: #set this to however many people can be kept waiting at a time
                self.session.vars['isExcess'] = True
        else:
            self.participant.vars['isItKnowledge'] = 'False'
            # print('*******participant.vars is', self.participant.vars['isItKnowledge'])
            self.session.vars['notKnows'] += 1
            if self.session.vars['notKnows'] - self.session.vars['knows'] > 5: #set this to however many people can be kept waiting at a time
                self.session.vars['isExcess'] = True
        if self.session.vars['isExcess']:
            self.participant.vars['movingOn'] = 'False'
            return True
        else:
            self.participant.vars['movingOn'] = 'True'
            return False


survey_pages = [
    DemographicInfo,
    SurveyPage1,
]

survey_pages1 = [
    DemographicInfo,
]

survey_pages2 = [
    SurveyPage1,
]

last_page = [
    ExitPage,
]

vignette_page = [
    Vignette,
]

setup_survey_pages(models.Player, survey_pages)

page_sequence = [
]

page_sequence.extend(vignette_page)
page_sequence.extend(survey_pages2)
page_sequence.extend(survey_pages1)
page_sequence.extend(last_page)