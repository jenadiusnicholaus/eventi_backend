
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from authentication.messages_handler import MessageHandler
from .serializers import GetUserSerializer, RegisterUserSerializer, LoginUserSerializer
import vonage
import random
import string
import pyotp
import base64
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone
import pytz





client = vonage.Client(key="d4ed6a01", secret="2DLWoByfIAizn1QM_")
sms = vonage.Sms(client)

User = get_user_model()
EXPIRY_TIME = 1   # seconds


# accounts/utils.py

class GenerateOtpRandomly:
    @staticmethod
    def generate_otp(length=6):
        characters = string.digits
        otp = ''.join(random.choice(characters) for _ in range(length))
        return otp


class GenerateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "JAHAOI0300330030238JAFKALA"


class GenerateOTP(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request):
        EXPIRY_TIME = 50 # seconds

        phone_number = request.query_params.get('phone_number', '')
        complete_phone_number = "+255"+phone_number
        keygen = GenerateKey()
        key = base64.b32encode(keygen.returnValue(complete_phone_number).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME, digits=6)  # TOTP Model for OTP is created

        try:
            user = User.objects.get(phone_number=complete_phone_number)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            User.objects.create(
                phone_number=complete_phone_number,
            )
            user = User.objects.get(phone_number=complete_phone_number) 
        if user.is_verified == True and is_otp_valid(otp_created_at=user.otp_created_at,EXPIRY_TIME=EXPIRY_TIME):

            return Response({"message":"User is already verified"}, status=400)
        elif is_otp_valid(otp_created_at=user.otp_created_at,EXPIRY_TIME=EXPIRY_TIME):
            return Response({"message":"OTP is still valid"}, status=400)
        
        else:

            user.otp=OTP.now() # user Newly created Model
            user.is_verified = False
            user.otp_created_at = timezone.localtime(timezone.now())
            user.save()  # Save the data
            
            # MessageHandler.send_otp_via_message(phone_number, OTP.now())
            # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
            return Response({'massege':f" An OTP ({OTP.now()}) is Sent to your phone Number"}, status=200)

       
def is_otp_valid(otp_created_at, EXPIRY_TIME):

    # Ensure otp_created_at is timezone aware
    otp_cD = timezone.localtime(otp_created_at)

  
    otp_created_at_aware = otp_cD.replace(tzinfo=pytz.timezone('Africa/Dar_es_Salaam'))

    # Get the current time (timezone aware)
    now_aware = datetime.now(pytz.timezone('Africa/Dar_es_Salaam'))

    # Calculate the remaining time
    remaining_time = (otp_created_at_aware + timedelta(seconds=EXPIRY_TIME)) - now_aware

    # If remaining_time is greater than zero, OTP is still valid
    return remaining_time.total_seconds() > 0


# accounts/views.p
class ValidateOTP(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number', '')
        otp = request.data.get('otp_code', '')

        try:
            user = User.objects.filter(phone_number=phone_number, otp=otp)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = GenerateKey()
        key = base64.b32encode(keygen.returnValue(phone_number).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = EXPIRY_TIME)  # TOTP Model 
   
        if user.exists:
            _user =user.first()
            if _user.is_verified == True and is_otp_valid(otp_created_at=_user.otp_created_at,EXPIRY_TIME=EXPIRY_TIME):
                return Response({"message":"User is already verified", 'user':GetUserSerializer(_user).data}, status=400)
            elif is_otp_valid(otp_created_at=_user.otp_created_at,EXPIRY_TIME=EXPIRY_TIME):  # Verifying the OTP
                access_token = AccessToken.for_user(_user)
                refresh_token = RefreshToken.for_user(_user)
                _user.is_verified = True
                _user.save()
        
                return Response({'message':"You are authorised", 'access_token':str(access_token), 'refresh_token': str(refresh_token), 'user':GetUserSerializer(_user).data }, status=200)
            return Response({"message":"OTP is wrong/expired"}, status=400)

        else:
            return Response("User does not exist", status=404)  # False Call
        
       



# accounts/views.p
class GetUsers(APIView):
    def post(self, request):
        user = User.objects.all()
        serializer = GetUserSerializer(user, many=True)
        return Response(serializer.data, status=200)



