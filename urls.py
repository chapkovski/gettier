
# from django.views.generic import TemplateView

import gettier_init.views as v

# urls.py
from django.conf.urls import url
from otree.urls import urlpatterns
from django.contrib.auth.decorators import login_required

urlpatterns.append(url(r'^vignette$', login_required(v.VignetteView.as_view()), name='vignette_customization'),)