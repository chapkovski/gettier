# from django.views.generic import TemplateView

import gettier_init.pages as v

# urls.py
from django.conf.urls import url
from otree.urls import urlpatterns
from django.contrib.auth.decorators import login_required

# TODO: add login required if login is indeed required
urlpatterns.append(url(r'^vignette$', v.VignetteView.as_view(), name='vignette_customization'), )
