from channels.generic.websocket import JsonWebsocketConsumer
from .models import Player, Group
import json, datetime
from asgiref.sync import async_to_sync


class ChatWatcher(JsonWebsocketConsumer):
    url_pattern = (
            r'^/chatwatcher' +
            '/group/(?P<group>[0-9]+)' +
            '/participant/(?P<participant_code>[a-zA-Z0-9_-]+)' +
            '/player/(?P<player>[0-9]+)' +
            '$')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kwargs = self.scope['url_route']['kwargs']
        self.clean_kwargs(self.kwargs)
        self.groups = [self.get_group_name(self.otree_group)]

    def get_group_name(self, group_id):
        return 'chatwatcher{}'.format(group_id)

    def get_group(self):
        return Group.objects.get(pk=self.otree_group)

    def clean_kwargs(self, kwargs):
        self.otree_group = kwargs['group']
        self.player = kwargs['player']
        self.participant = kwargs['participant_code']

    def receive_json(self, content, **kwargs):
        if content.get('type') == 'out':
            gr = self.get_group()
            gr.both_partners_in_chat = False
            gr.save()
            async_to_sync(self.channel_layer.group_send)(
                self.get_group_name(self.otree_group),
                {
                    "type": "is_over",
                    "text": f"Participant {self.participant} left the chat",
                },
            )

    def connect(self):
        super().connect()
        self.make_a_stamp('connected')
        content = {'accept': True}
        async_to_sync(self.channel_layer.group_send)(
            self.get_group_name(self.otree_group),
            {
                "type": "new_member_connected",
                "text": f"Participant {self.participant} connected"
            }
        )

        self.send_json({'text': json.dumps(content)})

    def is_over(self, event):
        print(event['text'])
        self.send_json({'over': True})

    def new_member_connected(self, event):
        print(f"{event['type']}:: {event['text']}")

    def make_a_stamp(self, status):
        p = Player.objects.get(pk=self.kwargs['player'])
        now = datetime.datetime.now(datetime.timezone.utc)
        p.disconnected_timestamp = now
        p.chat_status = status
        p.save()

    def disconnect(self, message, **kwargs):
        print('we are in disconnect')
        self.make_a_stamp('disconnected')

    def send(self, content):
        self.message.reply_channel.send({'text': json.dumps(content)})
