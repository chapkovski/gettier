# from channels import Group
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from .models import Player, Constants
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

    def get_group_name(self, group_id):
        return 'chatwatcher{}'.format(group_id)

    def clean_kwargs(self, kwargs):
        self.otree_group = kwargs['group']
        self.player = kwargs['player']
        self.participant = kwargs['participant_code']

    def is_over(self, msg):
        if msg['type'] == 'checking':
            another_player = Player.objects.get(pk=self.player).get_others_in_group()[0]
            if another_player.chat_status == 'disconnected':
                disconnection_time = another_player.disconnected_timestamp
                now = datetime.datetime.now(datetime.timezone.utc)
                diff = (now - disconnection_time).total_seconds()
                threshold_met = diff > Constants.threshold_sec
                if threshold_met:
                    return True
        if msg['type'] == 'out':
            return True
        return False

    def receive(self, text=None, bytes=None, **kwargs):
        self.clean_kwargs(self.kwargs)
        msg = json.loads(text)
        if self.is_over(msg):
            async_to_sync(self.channel_layer.group_send)(
                self.get_group_name(self.otree_group),
                {
                    "type": "chat.message",
                    "text": json.dumps({'over': True}),
                },
            )

    def connect(self):
        super().connect()
        print('im connected')
        self.clean_kwargs(self.kwargs)
        self.groups += [self.get_group_name(self.otree_group)]
        #
        self.make_a_stamp('connected')
        content = {'accept': True}
        async_to_sync(self.channel_layer.group_send)(
            self.get_group_name(self.otree_group),
            {
                "type": "chat.message",
                "text": json.dumps(
                    {'togr': 'message to group from participant {}'.format(self.participant)})
            },

        )
        #
        # self.message.reply_channel.send({'text': json.dumps(content)})

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
