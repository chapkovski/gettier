from channels.routing import route, route_class
from my_simple_survey.consumers import ChatWatcher
from otree.chat.otree_extensions.routing import channel_routing as chat_routing
# NOTE: otree_extensions is part of
# otree-core's private API, which may change at any time.
channel_routing = chat_routing + [
    route_class(ChatWatcher, path=ChatWatcher.url_pattern),

]