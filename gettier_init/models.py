from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otreeutils.surveys import create_player_model_for_survey


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'gettier_init'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars['knows'] = 0
        self.session.vars['notKnows'] = 0
        self.session.vars['isExcess'] = False


class Group(BaseGroup):
    pass


# ONLY CHANGE THE SECOND PARAMETER IN EACH SET OF PARENTHESES BELOW. THESE ARE THE STRINGS DISPLAYED TO THE USER.
# EDITING THE FIRST PARAMETER OF ANY SET OF PARENTHESES COULD BREAK THE CODE.
GETTIER_CHOICES = (
    ('True', 'Yes, he knows it'),
    ('False', 'No, he does not know it'),
)



SURVEY_DEFINITIONS = (
    {
        #'page_title': 'Does Bob know that Jill drives an American car?',
        #LEAVE PAGE TITLE BLANK
        'page_title': ' ',
        'survey_fields': [
            ('isItKnowledge', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': '',   # survey question
                'field': models.CharField(choices=GETTIER_CHOICES),
            }),
        ]
    },
)


Player = create_player_model_for_survey('gettier_init.models', SURVEY_DEFINITIONS)



