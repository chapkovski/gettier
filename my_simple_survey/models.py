from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Your name here'

doc = """
This software is adapted from oTree, and oTreeChat, for the purpose 
of pairing mTurkers into chat rooms on the basis of their response to a 
thought-experiment. "Gettier_init" pairs mTurkers with different intuitions about
the "Gettier case" (borrowed from Winberg, Nichols, and Stich's 2001, 
'Normativity and Epistemic Intuitions', https://www.jstor.org/stable/43154374). 
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
    reach_payoff = .25


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


GETTIER_CHOICES = (
    ('True', 'Yes, Bob knows that Jill drives an American car'),
    ('False', 'No, Bob does not know that Jill drives an American car'),
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


class Player(BasePlayer):
    is_it_still_knowledge = models.CharField(choices=GETTIER_CHOICES,
                                          verbose_name="""What do you think after chatting with the other player?
                                          Does Bob know that Jill drives an American car?""",
                                             widget=widgets.RadioSelectHorizontal)


    reason = models.TextField(blank=True,
                              verbose_name="""Please explain in 2-3 lines why you did or did not change
                                   your initial answer to this question""")
    experience = models.CharField(choices=YESNO_CHOICES,
                                  verbose_name="""Have you ever read a story like the one in 
                                      this experiment in any other context before?""",
                                  widget=widgets.RadioSelect)
    age = models.IntegerField(verbose_name="How old are you?")
    gender = models.CharField(choices=GENDER_CHOICES,
                              verbose_name='What is your gender?')
    race = models.CharField(choices=RACE_CHOICES,
                            verbose_name='What is your race?',
                            )
    education = models.CharField(choices=EDUCATION_CHOICES,
                                 verbose_name='What is the highest level of education you have achieved?')
