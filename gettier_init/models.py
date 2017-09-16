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


GETTIER_CHOICES = (
    ('True', 'Yes, she really knows it'),
    ('False', 'No, she only believes it'),
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
)

RACE_CHOICES = (
    ('White', 'White'),
    ('Latino', 'Latino'),
    ('Black', 'African American'),
    ('Native American', 'Native American'),
    ('Asian or Pacific Islander', 'Asian'),
    ('Other', 'Other'),
)

EDUCATION_CHOICES = (
    ('None', 'No schooling completed'),
    ('Grade School', 'Nursery school to 8th grade'),
    ('Some HS', 'Some high school, no diploma'),
    ('HS', 'High school graduate, diploma or the equivalent (for example: GED)'),
    ('Some College', 'Some college credit, no degree'),
    ('Trade School', 'Trade/technical/vocational training'),
    ('Associate', 'Associate degree'),
    ('Bachelor', 'Bachelor’s degree'),
    ('Associate', 'Master’s degree'),
    ('Professional', 'Professional degree'),
    ('Doctorate', 'Doctorate degree'),
    ('Other', 'Other'),
)

SURVEY_DEFINITIONS = (
    {
        'page_title': 'Please answer the following demographic questions:',
        'survey_fields': [
            ('age', {   # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'How old are you?',  # survey question
                 'field': models.CharField(blank=True), # put in free response slot
             }),
            ('gender', {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'What is your gender?',  # survey question
                 'field': models.CharField(choices=GENDER_CHOICES),  # put in free response slot?
             }),
            ('race', {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'What is your race?',  # survey question
                 'field': models.CharField(choices=RACE_CHOICES),  # put in free response slot?
             }),
            ('education', {  # field name (which will also end up in your "Player" class and hence in your output data)
                 'text': 'What is your highest level of education?',  # survey question
                 'field': models.CharField(choices=EDUCATION_CHOICES),  # put in free response slot?
             }),
        ]
    },
    {
        'page_title': 'Gettier Question',
        'survey_fields': [
            ('isItKnowledge', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Is the Gettier case knowledge?',   # survey question
                'field': models.CharField(choices=GETTIER_CHOICES),
            }),
        ]
    },
)


Player = create_player_model_for_survey('gettier_init.models', SURVEY_DEFINITIONS)



