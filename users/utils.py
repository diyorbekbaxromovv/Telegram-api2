import re
from rest_framework.validators import ValidationError
import requests
import threading
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

russian_phone_regex = r'^\+7\d{10}$'  
uzbek_phone_regex = r'^\+998\d{9}$'  
kazakh_phone_regex = r'^\+7\d{9}$'  
korean_phone_regex = r'^\+82\d{9,10}$'
american_phone_regex = r'^\+1\d{10}$'



def check_email_or_phone(user_input):
    if re.match(email_regex, user_input) is not None:
        return "email" 
    elif re.match(russian_phone_regex, user_input) is not None:
        return 'russian'
    elif re.match(uzbek_phone_regex, user_input) is not None:
        return 'uzbek'
    elif re.match(kazakh_phone_regex, user_input) is not None:
        return 'kazakh'
    elif re.match(korean_phone_regex, user_input) is not None:
        return 'korean'
    elif re.match(american_phone_regex, user_input) is not None:
        return 'american'
    
    
    else:
        data = {
            'status': False,
            'message':'Valid email or phone number was not provided'
        }
        
        raise ValidationError(data)
    
    
 

class SmsThread(threading.Thread):
    def __init__(self, sms):
        self.sms = sms
        super(SmsThread, self).__init__()
        
    def run(self):
        send_message(self.sms)
        
        
def send_message(message_text):
    url = f'https://api.telegram.org/bot7152481554:AAH-ZfJtvyFvXBPYLTTFdq9gvjDH9-nxMdg/sendMessage'
    params = {
        "chat_id": "5665497078",
        "text": message_text
    }
    response = requests.post(url, data=params)
    return response.json()


def send_sms(sms_text):
    sms_thread = SmsThread(sms_text)
    
    sms_thread.start()
    
    sms_thread.join()


