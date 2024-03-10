from rest_framework import serializers
from .models import User, VIA_PHONE, VIA_EMAIL, RUSSIAN, UZBEK, KAZAK, KOREAN, AMERICAN
from .utils import check_email_or_phone
from rest_framework.validators import ValidationError


class SignUpSerializer(serializers.ModelSerializer):
    auth_type = serializers.CharField(required=False, read_only=True)
    auth_status = serializers.CharField(required=False, read_only=True)
    country_number = serializers.CharField(required=False, read_only=True)
    
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['email_phone']=serializers.CharField(required=False)
        self.fields['country_phone_number']=serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ('auth_type', 'auth_status', 'country_number')
        
        
    
    def validate(self, data):
        user_input = data.get('email_phone')
        email_or_phone = check_email_or_phone(user_input)
        
        if email_or_phone == 'russian':
            data = {
                'auth_type':VIA_PHONE,
                'country_number':RUSSIAN,
                'phone_number':user_input
                
            }
        elif email_or_phone == 'uzbek':
            data = {
                'auth_type':VIA_PHONE,
                'country_number':UZBEK,
                'phone_number':user_input
            }
        elif email_or_phone == 'kazak':
            data = {
                'auth_type':VIA_PHONE,
                'country_number':KAZAK,
                'phone_number':user_input
            }
        elif email_or_phone == 'korean':
            data = {
                'auth_type':VIA_PHONE,
                'country_number':KOREAN,
                'phone_number':user_input
            }
        elif email_or_phone == 'american':
            data = {
                'auth_type':VIA_PHONE,
                'country_number':AMERICAN,
                'phone_number':user_input
            }
        elif email_or_phone == 'email':
            data = {
                'auth_type':VIA_EMAIL,
                'email':user_input
            }
        else:
            data = {
                'status': False, 
                'message': 'Siz kiritgan malumot xato'
            }    
            
            raise ValidationError(data)
        return data
        
     