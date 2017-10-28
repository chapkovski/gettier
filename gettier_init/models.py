from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)



author = 'Philip Chapkovski, UZH for Simon Cullen, Princeton'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'gettier_init'
    players_per_group = None
    num_rounds = 1
    GETTIER_CHOICES = [
        ('True', 'Yes, he knows it'),
        ('False', 'No, he does not know it'),
    ]


class Subsession(BaseSubsession):
    ...

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    is_it_knowledge = models.BooleanField(verbose_name='Does Bob know that Jill drives an American car? ')
    # timestamp_answer = models.IntegerField()


