from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
from django.core.mail import send_mail
from .models import UserRole, Role
from django.contrib.auth import authenticate

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'phone_number', 'student_number']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            student_number=validated_data['student_number'],
            phone_number=validated_data.get('phone_number', '')
        )
        return user
        
        # def random_with_N_digits(n):
        #     range_start = 10**(n-1)
        #     range_end = (10**n)-1
        #     return randint(range_start, range_end)

        # otp = random_with_N_digits(6)
        # user.otp = otp
        # user.save()

        # subject = 'Please Confirm Your Account'
        # message = 'Your 6 Digit Verification Pin: {}'.format(otp)
        # email_from = '*****'
        # recipient_list = [str(user.email), ]
        # send_mail(subject, message, email_from, recipient_list)
        # return user
    
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    
class StudentNumberLoginSerializer(serializers.Serializer):
    student_number = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'student_number', 'username', 'first_name', 'last_name', 'phone_number', 'profile_image', 'date_joined', 'is_active', 'is_staff', 'is_superuser']