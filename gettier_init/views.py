from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from otreeutils.surveys import SurveyPage, setup_survey_pages


class Vignette(Page):
    pass

class SurveyPage1(SurveyPage):
    pass

class MovingOnPage(Page):
    def is_displayed(self):
        self.session.vars['isExcess'] = False
        if self.player.isItKnowledge == 'True':
            self.participant.vars['isItKnowledge'] = 'True'
            self.session.vars['knows'] += 1
            if self.session.vars['knows'] - self.session.vars['notKnows'] > 1:  # set this to however many people can be kept waiting at a time
                self.session.vars['isExcess'] = True
        else:
            self.participant.vars['isItKnowledge'] = 'False'
            # print('*******participant.vars is', self.participant.vars['isItKnowledge'])
            self.session.vars['notKnows'] += 1
            if self.session.vars['notKnows'] - self.session.vars['knows'] > 1:  # set this to however many people can be kept waiting at a time
                self.session.vars['isExcess'] = True
        if self.session.vars['isExcess']:
            self.participant.vars['movingOn'] = 'False'
        else:
            self.participant.vars['movingOn'] = 'True'
        return False


survey_pages = [
    SurveyPage1,
]

vignette_page = [
    Vignette,
]

moving_page = [
    MovingOnPage,
]

setup_survey_pages(models.Player, survey_pages)

page_sequence = [
]

page_sequence.extend(vignette_page)
page_sequence.extend(survey_pages)
page_sequence.extend(moving_page)
