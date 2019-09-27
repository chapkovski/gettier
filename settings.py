import os
from os import environ

import dj_database_url

import otree.settings

EXTENSION_APPS = ['my_simple_survey']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_URLCONF = 'urls'
# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# don't share this with anybody.
SECRET_KEY = 'ss&7jxiw%)56%bnks==zqu*n3d0=jauj5t53p+2ig7t)l6+2)e'




# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = 'STUDY'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False



# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree',   'crispy_forms',]


DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are experiments using various vignettes that experimental 
    philosophers have studied.
</p>
"""

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


mturk_hit_settings = {
    'keywords': ['bonus', 'study', 'survey', 'experiment'],
    'title': 'Psychology Experiment',
    'description': 'Read a short paragraph and answer a question. Possible to get $0.25 bonus pay if selected. Without bonus: total expected time = 1 minute. With bonus, total expected time: 3 minutes.',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 5,
    'expiration_hours': 5 , # 5 hours
    'grant_qualification_id': '3CGA0BEV5WTPG8BZF5JS6FIHGOF6P3', # uncomment to prevent retakes (live)
    # 'grant_qualification_id': '3RKPNJXSGKRQ6FK6D45DFQ8YI6EESG', # uncomment to prevent retakes (sandbox)

    'qualification_requirements': [
        { # qualification 1: prevent retakes
             'QualificationTypeId': "3CGA0BEV5WTPG8BZF5JS6FIHGOF6P3", # uncomment for live version
          #  'QualificationTypeId': "3RKPNJXSGKRQ6FK6D45DFQ8YI6EESG", # uncomment for sandbox version
            'Comparator': "DoesNotExist",
        },
        { # qualification 2: US only (same for live and sandbox)
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{'Country': "US"}],
        },
        {  # qualification 3: completed at least 99 hits (same for live and sandbox)
            'QualificationTypeId': "00000000000000000040",
            'Comparator': "GreaterThanOrEqualTo",
            'IntegerValues': [99],
        },

    ]
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.00,
   # 'participation_fee': 0.15,
    'participation_fee': 0.10,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

SESSION_CONFIGS = [

    {
        'name': 'Gettier',
        'display_name': "Gettier Survey (Winberg, Nichols, and Stich, 2001)",
        'num_demo_participants': 7,
        'app_sequence': ['gettier_init', 'my_simple_survey'],
        'chat_seconds': 120,
    },
    ]


