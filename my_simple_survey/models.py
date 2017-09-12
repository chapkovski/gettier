from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


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


class Player (BasePlayer):
    isItStillKnowledge = models.BooleanField()
    bonus = models.CurrencyField()

    # give bonus payment to remaining participants
    def bonus_method(self):
        self.bonus = c(0.25)

