from channels.routing import route, route_class
from my_simple_survey.consumers import ChatWatcher
print('aaaa',ChatWatcher.url_pattern)
# NOTE: otree_extensions is part of
# otree-core's private API, which may change at any time.
channel_routing = [
    route_class(ChatWatcher, path=ChatWatcher.url_pattern),

]