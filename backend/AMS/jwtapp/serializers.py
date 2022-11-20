from email import utils
from xml.dom import ValidationErr
from rest_framework import serializers
from jwtapp.models import Mio_airline, Mio_flight_schedule, Mio_terminal, User
from jwtapp.utils import Util

# email reset
"-------------"
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
"-------------"

from django.core.exceptions import ValidationError



class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','first_name','last_name','roles','password', 'password2','terms_conditions','airline_code']
        extra_kwargs={'password':{'write_only':True}}

    # it is used for the validation of the data that we are getting from the frontend:
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError('password and confirm password mismatch')
        return attrs
        # return super().validate(attrs)

    # since our model is custom...we need to have this method to create the user:
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        # return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','roles','airline_code']
    
    def to_representation(self, instance):
        data = super(UserProfileSerializer,
                     self).to_representation(instance)
        response = {
            "id": data['id'],
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "email": data['email'],
            "roles": data['roles'],
            "airline_code": data['airline_code'],
        }

        return response
        
class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)

    class Meta:
        model=User
        fields=['password','password2']

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("password and password2 do not match")
        user.set_password(password)
        user.save()

        # But problem is here we are not getting the user in the serializer,we need to pass the user from the view to the serializer ,so we need to use context.
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print("encoded uid - ",uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print("password reset token - ",token)
            link="http://localhost:3000/api/user/reset/"+uid+"/"+token
            print("password reset link - ",link)
            body="click following link to reset password - " + link
            # send email:
            data={
                "subject":"Reset your password",
                "body":body,
                "to_email":user.email,
            }
            Util.send_mail(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not registered user")


class UserPasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type': 'password'},write_only=True)

    class Meta:
        model=User
        fields=['password','password2']

    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password!=password2:
                raise serializers.ValidationError("password and password2 do not match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError("Token is not validated or Expired")
            user.set_password(password)
            user.save()
            return attrs    
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is not valid or Expired")
        

class MioAirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mio_airline
        fields=['airline_flight_key','airline_code','flight_code','airline_name','is_available']
    
    def to_representation(self, instance):
        data = super(MioAirlineSerializer,
                     self).to_representation(instance)
        response = {
            "airline_flight_key": data['airline_flight_key'],
            "airline_code": data['airline_code'],
            "airline_name": data['airline_name'],
            "flight_code": data['flight_code'],
            "is_available": data['is_available']
        }
        return response

class MioTerminalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mio_terminal
        fields=['terminal_gate','gate_status']

    def to_representation(self, instance):
        return super().to_representation(instance)


class MioFlightScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mio_flight_schedule
        fields=['fact_guid','airline_flight_key','source','destination','arrival_departure','time','terminal_gate_key','baggage_carousel','remarks']
    
    def to_representation(self, instance):
        return super().to_representation(instance)
