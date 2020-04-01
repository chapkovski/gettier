from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import time

import json

from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django import forms



class VignetteSettingsForm(forms.ModelForm):
    pass



class VignetteView(UpdateView):
    def get_object(self, queryset=None):
        return models.SettingsMod.load()

    form_class = VignetteSettingsForm
    template_name = 'global/vignette.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('DemoIndex'))


class Vignette(Page):
    form_model = 'player'
    form_fields = ['is_it_knowledge', 'confidence']

    def vars_for_template(self):
        settings = json.loads(self.subsession.settings)
        return {'vignette': settings['vignette'],
                'label': settings['label'],
                }

    def is_it_knowledge_choices(self):
        choices = self.participant.vars['choices_order']
        return choices

    def before_next_page(self):
        self.participant.vars['is_it_knowledge'] = self.player.is_it_knowledge
        self.participant.vars['timestamp_answer'] = time.time()


page_sequence = [Vignette, ]
