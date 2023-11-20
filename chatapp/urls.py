from django.urls import path
from .views import *

urlpatterns = [
    path('room-messages/<str:user_id>/', RoomMessagesView.as_view(), name='room_messages'),
    path('room-messages/<str:user_id>/<int:room_id>/', RoomMessagesView.as_view(), name='room_messages'),

    path('user-chatrooms/', ChatRoomListView.as_view(), name='user_chatrooms')
]
