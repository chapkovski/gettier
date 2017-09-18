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
    name_in_url = 'my_simple_survey'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass



GETTIER_CHOICES = (
        ('True', 'Yes, he knows it'),
        ('False', 'No, he does not know it'),
    )

YESNO_CHOICES = (
        ('True', 'Yes, I have read a story similar to this one before.'),
        ('False', 'No, I have never read a story similar to this one.'),
    )


# if isItStillKnowledge == isItKnowledge, ask them why they changed their mind; else ask why they didn't change their minds

SURVEY_DEFINITIONS = (
    {
        'page_title': 'Please answer the following question:',
        'survey_fields': [
            ('isItStillKnowledge', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Does Bob know that Jill drives an American car?',   # survey question
                'field': models.CharField(choices=GETTIER_CHOICES),
            }),
            ('reason', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Please explain in 2-3 lines why you did or did not change your initial answer to this question',   # survey question
                'field': models.CharField(blank=True),
            }),
            ('experience',{
                'text': 'Have you ever read a story like the one in this experiment in any other context before?',   # survey question
                'field': models.CharField(choices=YESNO_CHOICES),
            }),
        ]
    },
)


Player = create_player_model_for_survey('my_simple_survey.models', SURVEY_DEFINITIONS)
