from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        is_it_knowledge = False
        if self.player.id_in_group == 1:
            is_it_knowledge = True
        if self.player.id_in_group == 2:
            is_it_knowledge = False
        if self.player.id_in_group == 3:
            is_it_knowledge = True
        if self.player.id_in_group == 4:
            is_it_knowledge = False

        yield (views.Vignette, {
            'is_it_knowledge': is_it_knowledge
        })
