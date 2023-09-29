import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Room, RoomMessage, Post


class Roommers(WebsocketConsumer):
    """
    The member of the Room
    """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    def connect(self):
        # read info from self.scope
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.room = Room.objects.get(name=self.room_name)
        self.user = self.scope['user']
        self.user_inbox = f'inbox_{self.user.username}'
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

        # send all online users by self.send func
        self.send(json.dumps({
            'type': 'user_list',
            'users': [user.username for user in self.room.online.all()],
        }))

        # check if the user is valid
        if self.user.is_authenticated:
            # create a user inbox for private messages
            async_to_sync(self.channel_layer.group_add)(
                self.user_inbox,
                self.channel_name,
            )
            # send the join event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_join',
                    'user': self.user.username,
                }
            )
            self.room.online.add(self.user)

    def disconnect(self, close_code):
        # disconnect the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name,
        )

        # send the leave event to the room
        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                self.user_inbox,
                self.channel_name,
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_leave',
                    'user': self.user.username,
                }
            )

            self.room.online.remove(self.user)


    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        post_name = text_data_json['post_name']
        
        # check if the user is valid
        if not self.user.is_authenticated:
            return

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
            }
        )
        
        RoomMessage.objects.create(
            user=self.user, 
            room=self.room, 
            belong_post = Post.objects.get(title=post_name, belong_room=self.room),
            content=message
        )


    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

    def user_join(self, event):
        self.send(text_data=json.dumps(event))

    def user_leave(self, event):
        self.send(text_data=json.dumps(event))

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))