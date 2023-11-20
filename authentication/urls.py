from django.urls import path
from .views import RegisterUserView, LoginUserView, LogoutUserView

urlpatterns = [
    path('signup/', RegisterUserView.as_view(), name='user_register'),

    path('login/', LoginUserView.as_view(), name='user_login'),
    path('logout/', LogoutUserView.as_view(), name='user_logout'),
]
