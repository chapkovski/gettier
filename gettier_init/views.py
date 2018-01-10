from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import time

import json
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field


class VignetteSettingsForm(forms.ModelForm):
    vignette = forms.CharField(widget=forms.Textarea)
    pay_per_min = forms.FloatField(
        help_text='Any float number in US dollars. Set to 0 to not pay for waiting. Then the earnings will not '
                  'be shown to a partiipant.')
    wait_before_leave = forms.IntegerField(help_text='Number in seconds.'
                                                   'Set to negative number to switch off the option to leaver earlier.')

    class Meta:
        model = models.SettingsMod
        fields = '__all__'

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'id-personal-data-form'
        helper.form_method = 'post'
        helper.layout = Layout(
            Field("vignette", css_class=" form-control"),
            Field('label', css_class=" form-control"),
            Field("yes_choice", css_class=" form-control"),
            Field("no_choice", css_class=" form-control"),
            Field("min_chat_sec", css_class=" form-control"),
            Field("max_chat_sec", css_class=" form-control"),
            Field("pay_per_min", css_class=" form-control"),
            Field("wait_before_leave", css_class=" form-control"),
            ButtonHolder(
                Submit('submit', 'Save', css_class='btn btn-success filkinbtn')
            )
        )
        return helper


class VignetteView(UpdateView):
    def get_object(self, queryset=None):
        return models.SettingsMod.load()

    form_class = VignetteSettingsForm
    template_name = 'global/vignette.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('DemoIndex'))


class Vignette(Page):
    form_model = models.Player
    form_fields = ['is_it_knowledge']

    def vars_for_template(self):
        settings = json.loads(self.subsession.settings)
        return {'vignette': settings['vignette'],
                'label': settings['label'],
                }

    def is_it_knowledge_choices(self):
        settings = json.loads(self.subsession.settings)
        yes_choice = settings['yes_choice']
        no_choice = settings['no_choice']
        choices = [(True, yes_choice), (False, no_choice)]
        random.shuffle(choices)
        return choices

    def before_next_page(self):
        self.participant.vars['is_it_knowledge'] = self.player.is_it_knowledge
        self.participant.vars['timestamp_answer'] = time.time()


page_sequence = [Vignette, ]
