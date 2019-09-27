from my_simple_survey.consumers import ChatWatcher
from django.conf.urls import url

websocket_routes = [
    url(
        r'^chatwatcher/group/(?P<group>[0-9]+)/participant/(?P<participant_code>[a-zA-Z0-9_-]+)/player/(?P<player>[0-9]+)$',
        ChatWatcher),
]
