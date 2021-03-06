from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from gettier_init.models import SettingsMod
import json
from otree.models_concrete import ChatMessage
from django.db import models as djmodels
from gettier_init.models import CONFIDENCE_CHOICES
from gettier_init.widgets import LikertWidget

author = 'Simon Cullen, Philipp Chapkovski'

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
    players_per_group = None
    num_rounds = 1
    reach_payoff = .25
    threshold_sec = 5


class Subsession(BaseSubsession):
    settings = models.CharField()

    def creating_session(self):
        self.settings = json.dumps(SettingsMod.load().as_dict())


class Group(BaseGroup):
    words_exchanged = models.IntegerField()
    both_partners_in_chat = models.BooleanField()
    def set_chat_payoff(self):
        settings = json.loads(self.subsession.settings)
        pay_per_word = settings['pay_per_word']
        participants = [p.participant for p in self.get_players()]
        allchatmessages = ChatMessage.objects.filter(participant__in=participants).values_list('body', flat=True)
        flatten_m = ' '.join(allchatmessages).split()
        lwords = len(flatten_m)
        self.words_exchanged = lwords
        Player.objects.filter(group=self).update(chat_earnings=lwords * pay_per_word)


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
    chat_earnings = models.CurrencyField(doc='payment get for chatting', default=0)
    chat_status = models.StringField()
    disconnected_timestamp = djmodels.DateTimeField(blank=True, null=True)
    reach_payoff = models.FloatField(doc='extra bonus for reaching chat stage', initial=0)
    early_finish = models.BooleanField(doc='if decided to abandon the waiting page clickin Finish the study')
    payoff_set = models.BooleanField(doc='check if payoff already set', )
    wp_timer_start = djmodels.DateTimeField(null=True, blank=True)
    sec_spent = models.IntegerField(doc='number of seconds spent on waiting page')
    sec_earned = models.FloatField(doc='dollars earned for waiting')
    in_wp = models.BooleanField(doc='to count waiting players',
                                initial=False)
    unmatched = models.BooleanField(doc='for those who havent been matched with those with the opposite view',
                                    initial=True)
    wp_passed = models.BooleanField(doc='checking if the player has already passed first wp page',
                                    initial=False)
    is_it_still_knowledge = models.StringField(choices=GETTIER_CHOICES,
                                               verbose_name="""Does Bob know that Jill drives an American car?""",
                                               widget=widgets.RadioSelect)

    still_confidence = models.IntegerField(
        choices=CONFIDENCE_CHOICES,
        widget=LikertWidget,
    )

    reason = models.TextField(blank=True,
                              verbose_name="""Please explain in 2-3 lines why you did or did not change
                                   your initial answer to this question""")
    experience = models.StringField(choices=YESNO_CHOICES,
                                    verbose_name="""Have you ever read a story like the one in 
                                      this experiment in any other context before?""",
                                    widget=widgets.RadioSelect)
    age = models.IntegerField(verbose_name="How old are you?", min=15, max=100)
    gender = models.StringField(choices=GENDER_CHOICES,
                                verbose_name='What is your gender?')
    race = models.StringField(choices=RACE_CHOICES,
                              verbose_name='What is your race?',
                              )
    education = models.StringField(choices=EDUCATION_CHOICES,
                                   verbose_name='What is the highest level of education you have achieved?')

    def set_payoff(self):
        self.payoff = self.reach_payoff + self.sec_earned + self.chat_earnings

    @property
    def other(self):
        return self.get_others_in_group()[0]
