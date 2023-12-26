from django.urls import path
from .views import *

urlpatterns = [
    path('get-groups/', GetEventiGroup.as_view()),
   path('create-group/', CreateGroup.as_view()),
    path('update-group/<int:pk>', UpdateGroup.as_view()),
    path('join-group/', JoinGroupView.as_view()),
    path('leave-group/', LeaveGroup.as_view()),
    path('get-group-members/', GetGroupMembers.as_view()),
    # path('get-group-plages/', GetGroupPlages.as_view()),
#     path('delete-group/<int:pk>', DeleteGroup.as_view()),
    path('get-group-plages/', GetGroupPlages.as_view()),
    path('create-group-plages/', CreateEventiGroupPlages.as_view()),

]
