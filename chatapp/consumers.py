import json
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import ChatRoom, ChatRoomParticipants, Messages, ChatParticipantsChannel

User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer for handling chat functionality.

    Attributes:
        user_id (str): The ID of the user associated with the consumer.
        group_name (str): The name of the group/channel for the chat.
        to_user (str): The ID of the user to whom the message is being sent.
    """

    async def connect(self):
        """
        Called when the WebSocket is handshaking as part of the connection process.
        Performs necessary setup tasks and accepts the connection.
        """
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        await self.save_user_channel()

        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when the WebSocket closes for any reason.
        Performs necessary cleanup tasks.
        
        Args:
            close_code (int): The close code indicating the reason for disconnection.
        """
        await self.delete_user_channel()

        await self.disconnect(close_code)

    async def receive_json(self, text_data=None, byte_data=None):
        """
        Called when a message is received from the WebSocket.
        Handles the received message and sends it to the appropriate recipients.

        Args:
            text_data (str): The received message data as a JSON string.
            byte_data (bytes): The received message data as bytes.
        """
        message = text_data['message']
        self.to_user = text_data['to_user']
        to_user_channel, to_user_id = await self.get_user_channel(self.to_user)
        self.group_name = f'{self.user_id}-{self.to_user}'
        message_response = await self.save_message(self.group_name, self.user, message)
        message_response['type'] = 'send.message'

        channel_layer = get_channel_layer()

        await self.channel_layer.group_add(
            self.group_name,
            str(self.channel_name)
        )
        if to_user_channel != None and to_user_id != None:
            await self.channel_layer.group_add(
                self.group_name,
                str(to_user_channel)
            )

        await channel_layer.group_send(
            self.group_name, message_response
        )

    async def send_message(self, event):
        """
        Sends a message to the WebSocket connection.

        Args:
            event (dict): The event data containing the message details.
        """
        print(event)

        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user_channel(self, to_user):
        """
        Retrieves the channel and user ID associated with the given user.

        Args:
            to_user (str): The ID of the user.

        Returns:
            tuple: A tuple containing the channel name and user ID.
        """
        try:
            send_user_channel = ChatParticipantsChannel.objects.filter(
                user=to_user).latest('id')
            channel_name = send_user_channel
            user_id = send_user_channel.user.user_uid
        except Exception as e:
            channel_name = None
            user_id = None

        return channel_name, user_id

    @database_sync_to_async
    def save_user_channel(self):
        """
        Saves the user's channel in the database.
        """
        self.user = User.objects.get(user_uid=self.user_id)

        ChatParticipantsChannel.objects.create(
            user=self.user,
            channel=self.channel_name
        )

    @database_sync_to_async
    def delete_user_channel(self):
        """
        Deletes the user's channel from the database.
        """
        ChatParticipantsChannel.objects.filter(user=self.user).delete()

    @database_sync_to_async
    def save_message(self, room, user, content):
        """
        Saves the message in the database and updates the chat room details.

        Args:
            room (str): The name of the chat room.
            user (User): The user sending the message.
            content (str): The content of the message.

        Returns:
            dict: A dictionary containing the details of the saved message.
        """
        try:
            ChatRoomParticipants.objects.get_or_create(
                Q(room__name=f'{self.user.user_uid}-{self.to_user}') |
                Q(room__name=f'{self.to_user}-{self.user.user_uid}'), user=self.user)
            ChatRoomParticipants.objects.get_or_create(
                Q(room__name=f'{self.user.user_uid}-{self.to_user}') |
                Q(room__name=f'{self.to_user}-{self.user.user_uid}'), user=self.to_user)
        except Exception as e:
            print(e)

        try:
            chatroom = ChatRoom.objects.get(Q(name=f'{self.user.user_uid}-{self.to_user}') |
                                            Q(name=f'{self.to_user}-{self.user.user_uid}'))
            chatroom.last_message = content 
            chatroom.last_sent_user = self.user
        except Exception as e:
            chatroom = ChatRoom.objects.create(
                name=str(room),
                last_message=content,
                last_sent_user=self.user
            )

        message = Messages.objects.create(
            room=chatroom, user=self.user, content=content
        )

        message_response = {
            'message_id': message.id,
            'message_room': chatroom.id,
            'message_content': message.content,
            'message_user': str(message.user.user_uid),
            'message_created_at': str(message.created_at),
        }

        return message_response
