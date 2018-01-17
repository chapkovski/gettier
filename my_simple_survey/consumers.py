from channels import Group
from channels.generic.websockets import WebsocketConsumer
from .models import Player, Group as OtreeGroup, Constants
import json, datetime


class ChatWatcher(WebsocketConsumer):
    url_pattern = (
        r'^/chatwatcher' +
        '/group/(?P<group>[0-9]+)' +
        '/participant/(?P<participant_code>[a-zA-Z0-9_-]+)' +
        '/player/(?P<player>[0-9]+)' +
        '$')

    def get_group_name(self, group_id):
        return 'chatwatcher{}'.format(group_id)

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """

        return [self.get_group_name(kwargs['group'])]

    def clean_kwargs(self, kwargs):
        self.otree_group = self.kwargs['group']
        self.player = self.kwargs['player']
        self.participant = self.kwargs['participant_code']

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
        self.clean_kwargs(kwargs)
        msg = json.loads(text)
        if self.is_over(msg):
            Group(self.get_group_name(kwargs['group'])).send(
                {'text': json.dumps({'over': True})})

    def connect(self, message, **kwargs):
        print('im connected')
        self.make_a_stamp('connected')
        content = {'accept': True}

        Group('chatwatcher{}'.format(kwargs['group'])).send(
            {'text': json.dumps(
                {'togr': 'message to group from participant {}'.format(kwargs['participant_code'])})}
        )
        self.message.reply_channel.send({'text': json.dumps(content)})
        return super().connect(message, **kwargs)

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
