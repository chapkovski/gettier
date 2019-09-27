from my_simple_survey.consumers import ChatWatcher
from django.conf.urls import url


websocket_routes = [
    url(ChatWatcher.url_pattern,
        ChatWatcher),
]
