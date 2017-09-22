from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otreeutils.surveys import create_player_model_for_survey


author = 'Your name here'

doc = """
This software is adapted from oTree, oTreeUtils, and oTreeChat, for the purpose 
of (1) pairing mTurkers into chat rooms on the basis of their response to a 
thought-experiment. "Gettier_init" pairs mTurkers with different intuitions about
the "Gettier case" (borrowed from Winberg, Nichols, and Stich's 2001, 
Normativity and Epistemic Intuitions (https://www.jstor.org/stable/43154374). 
Since researchers may wish to test cases where there will not be an approximately
equal number of mTurkers on either side (although see Cullen 2010 for techniques
to manipulate initial responses), this software implements a system for advancing
excess participants on either side of an issue to the end of the survey without
waiting for a participant to chat with.
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
        ('True', 'Yes, he knows that Jill drives an American car'),
        ('False', 'No, he does not know that Jill drives an American car'),
    )

YESNO_CHOICES = (
        ('True', 'Yes, I have read a story very similar to this one before.'),
        ('False', 'No, I have never read a story very similar to this one.'),
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

MOVINGON_CHOICES = (
    ('True', 'Yes'),
    ('True', 'No'),
)


# if isItStillKnowledge == isItKnowledge, ask them why they changed their mind; else ask why they didn't change their minds

SURVEY_DEFINITIONS = (
    {
#        'page_title': 'Does Bob know that Jill drives an American car?',
        # Leaving page_title blank #
        'page_title': ' ',
        'survey_fields': [
            ('isItStillKnowledge', {   # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Does Bob know that Jill drives an American car',   # survey question
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
                 'text': 'What is the highest level of education you have achieved?',  # survey question
                 'field': models.CharField(choices=EDUCATION_CHOICES),  # put in free response slot?
             }),
            ('movingOn', {  # field name (which will also end up in your "Player" class and hence in your output data)
                'text': 'Select "Yes" for this question:',   # survey question
                'field': models.CharField(choices=MOVINGON_CHOICES),
             }),
        ]
    },
)


Player = create_player_model_for_survey('my_simple_survey.models', SURVEY_DEFINITIONS)
