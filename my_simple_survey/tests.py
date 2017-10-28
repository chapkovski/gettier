from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants, EDUCATION_CHOICES, GENDER_CHOICES, GETTIER_CHOICES, YESNO_CHOICES


class PlayerBot(Bot):

    def play_round(self):
        if not self.player.unmatched:
            yield (views.Chats)
            yield (views.EndSurvey, {
                'is_it_still_knowledge': GETTIER_CHOICES[0][0],
                'reason': 'because I said so',
                'experience': YESNO_CHOICES[0][0],
            })
            yield (views.DemographicInfo, {
                'age': 32,
                'gender': GENDER_CHOICES[0][0],
                'education': EDUCATION_CHOICES[0][0],
            })
        if self.player.unmatched:
            yield (views.ExitPage)
