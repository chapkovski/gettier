from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        is_it_knowledge = random.choice(['True', 'False'])

        yield (views.Vignette, {
            'is_it_knowledge': is_it_knowledge
        })