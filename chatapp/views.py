from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import ChatRoom, Messages, ChatRoomParticipants

User = get_user_model()


class RoomMessagesView(APIView):
    """
    API view for retrieving chat room messages.

    Attributes:
        permission_classes (tuple): Tuple of permission classes for authentication.

    Methods:
        get(request, user_id, room_id=None): Retrieves chat room messages based on user and room ID.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id, room_id=None):
        """
        Retrieves chat room messages based on user and room ID.

        Args:
            request (HttpRequest): The HTTP request object.
            user_id (int): The ID of the user.
            room_id (int, optional): The ID of the room. Defaults to None.

        Returns:
            Response: The HTTP response object containing the chat room messages.
        """
        user = request.user

        if room_id:
            messages = list(Messages.objects.filter(room__id=room_id).values(
                'id', 'room', 'user', 'content', 'created_at'))
        else:
            messages = list(Messages.objects.filter(Q(room__name=f'{user.user_uid}-{user_id}') |
                            Q(room__name=f'{user_id}-{user.user_uid}')).values('id', 'room', 'user', 'content', 'created_at'))

        response_content = {
            'status': True,
            'message': 'Chat Room Messages',
            'data': messages
        }

        return Response(response_content, status=status.HTTP_200_OK)


class ChatRoomListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """
        Retrieves the chat rooms associated with the user and returns a response.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the chat room list.
        """
        user = request.user

        # chatroomparticipants = ChatRoomParticipants

        # room_ids = list(chatroomparticipants.object)

        room_ids = list(ChatRoomParticipants.objects.filter(
            user=user).values_list('room__id', flat=True))
        
        # print(room_ids.)
        chatrooms = list(ChatRoomParticipants.objects.exclude(user__user_uid=user.user_uid).filter(
            room__id__in=room_ids).values('user__username', 'user__user_uid', 'room__id', 'room__name', 'room__last_message', 'room__last_sent_user'))

        response_content = {
            'status': True,
            'message': 'User Chat Room List',
            'data': chatrooms
        }

        return Response(response_content, status=status.HTTP_200_OK)
