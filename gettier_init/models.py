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


class Group(BaseGroup):
    pass


GETTIER_CHOICES = (
    ('yes', 'Yes, she really knows it'),
    ('no', 'No, she only believes it'),
)

SURVEY_DEFINITIONS = (
    {
        'page_title': 'Gettier Question',
        'survey_fields': [
            {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Is the Gettier case knowledge?',   # survey question
                'field': models.CharField(choices=GETTIER_CHOICES),
            },
        ]
    }
)


Player = create_player_model_for_survey('gettier_init.models', SURVEY_DEFINITIONS)

