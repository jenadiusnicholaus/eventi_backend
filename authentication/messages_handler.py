from django.conf import settings
from twilio.rest import Client


class MessageHandler:
    @staticmethod
    def send_otp_via_message( phone_number, otp):     
    
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
    
        message=client.messages.create(body=f'your otp is:{otp}',from_=f'{settings.TWILIO_PHONE_NUMBER}',to=f'{settings.COUNTRY_CODE}{phone_number}')
        print(message)
        return message
    def send_otp_via_whatsapp( phone_number, otp):     
        client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
        message=client.messages.create(body=f'your otp is:{otp}',from_=f'{settings.TWILIO_WHATSAPP_NUMBER}',to=f'whatsapp:{settings.COUNTRY_CODE}{phone_number}')
