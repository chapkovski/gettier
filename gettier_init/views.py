from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import time


class Vignette( Page):
    form_model = models.Player
    form_fields = ['is_it_knowledge']

    # def is_it_knowledge_choices(self):
    #     choices = Constants.GETTIER_CHOICES.copy()
    #     random.shuffle(choices)
    #     return choices

    def before_next_page(self):
        self.participant.vars['is_it_knowledge'] = self.player.is_it_knowledge
        self.participant.vars['timestamp_answer'] = time.time()


page_sequence = [Vignette, ]
