from rest_framework import serializers
from .models import User, VIA_PHONE, VIA_EMAIL, RUSSIAN, UZBEK, KAZAK, KOREAN, AMERICAN
from .utils import check_email_or_phone, send_sms
from rest_framework.validators import ValidationError
from django.db.models import Q



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
        
    
    def validate_email_phone(self, email_phone):
        user = User.objects.filter(Q(email=email_phone) | Q(phone_number=email_phone))
        
        if user.exists():
            data = {
                "status": False, 
                "message": "Foydalanuvchi allaqachon ro'yxatdan o'tgan"
            }
                
            raise ValidationError(data)
        return email_phone
    
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
        
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        auth_type = validated_data.get('auth_type')
        if auth_type == VIA_EMAIL:
            code = user.create_confirmation_code(VIA_EMAIL)
            send_sms(code)
            
        elif auth_type == VIA_PHONE:
            code = user.create_confirmation_code(VIA_PHONE)
            send_sms(code)
            
        else:
            data = {
                "status": False, 
                "message": "Code yuborishda hatolik mavjud"
            }
            raise ValidationError(data)
        
        return user
    
    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        
        data['access'] = instance.token()['access']
        data['refresh'] = instance.token()['refresh']
        
        return data 