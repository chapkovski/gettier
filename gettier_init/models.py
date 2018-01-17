from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

import json, random

author = 'Philip Chapkovski, UZH for Simon Cullen, Princeton'

doc = """
Your app description
"""
from django.db import models as djmodels


class SingletonModel(djmodels.Model):
    """Singleton Django Model
    Ensures there's always only one entry in the database, and can fix the
    table (by deleting extra entries) even if added via another mechanism.
    Also has a static load() method which always returns the object - from
    the database if possible, or a new empty (default) instance if the
    database is still empty. If your instance has sane defaults (recommended),
    you can use it immediately without worrying if it was saved to the
    database or not.
    Useful for things like system-wide user-editable settings.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()


vignette_text = """ Bob has a friend, Jill, who has driven a Buick for many years.
           Bob therefore thinks that Jill drives an American car. He is not aware,
           however, that her Buick has recently been stolen, and he is also not
           aware that Jill has replaced it with a Pontiac, which is a different
           kind of American car."""


class SettingsMod(SingletonModel):
    label = models.CharField(verbose_name='Question for vignette',
                             default='Does Bob know that Jill drives an American car? ')
    vignette = models.CharField(verbose_name='Vignette text',
                                widget=djmodels.TextField,
                                initial=" ".join(vignette_text.split())
                                )
    yes_choice = models.CharField(verbose_name='Text for \'Yes\' answer', default='Yes, he knows it')
    no_choice = models.CharField(verbose_name='Text for \'No\' answer', default='No, he does not know it')
    min_chat_sec = models.IntegerField(verbose_name='Minimum time on chat page, in seconds', default=60)
    max_chat_sec = models.IntegerField(verbose_name='Maximum time on chat page, in seconds', default=300)
    pay_per_min = models.FloatField(verbose_name='How much a person earned for minute of waiting',
                                    doc='how much a person earned for waiting', initial=0.1)
    wait_before_leave = models.IntegerField(doc='after how many secs a person can quit waiting page',
                                            initial=300)

    def as_dict(self):
        af = self._meta.get_fields()
        dicttoret = dict()
        for i in af:
            dicttoret[i.name] = getattr(self,i.name)
        return dicttoret


class Constants(BaseConstants):
    name_in_url = 'gettier_init'
    players_per_group = None
    num_rounds = 1
    GETTIER_CHOICES = [
        ('True', 'Yes, he knows it'),
        ('False', 'No, he does not know it'),
    ]


class Subsession(BaseSubsession):
    settings = models.CharField()

    def creating_session(self):
        self.settings = json.dumps(SettingsMod.load().as_dict())
        settings = json.loads(self.settings)
        yes_choice = settings['yes_choice']
        no_choice = settings['no_choice']
        choices = [(True, yes_choice), (False, no_choice)]
        for p in self.session.get_participants():
            curch = choices.copy()
            random.shuffle(curch)
            p.vars['choices_order'] = curch
        for p in self.get_players():
            p.choices_order = p.participant.vars['choices_order']



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choices_order = models.CharField()
    is_it_knowledge = models.BooleanField(verbose_name='Does Bob know that Jill drives an American car? ')
