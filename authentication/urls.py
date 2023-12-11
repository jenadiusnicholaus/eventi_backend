from django.urls import path
from .views import GenerateOTP, ValidateOTP, GetUsers

urlpatterns = [
    path('user/', GetUsers.as_view(), name='user'),
    path('generate_OTP/', GenerateOTP.as_view(), name='user_login'),
        path('verify_OTP/', ValidateOTP.as_view(), name='phone_number_verification'),

]
