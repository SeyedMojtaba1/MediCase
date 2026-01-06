from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import check_password
from .models import Role
from django.db import transaction
import environ
import os
from .utils import send_reset_otp_task

env = environ.Env()
environ.Env.read_env(env_file='./secrets/secrets.env')

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    main_role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'username', 'first_name', 'last_name', 
            'password', 'phone_number', 'personal_number', 
            'main_role', 'major',
        ]

    def validate_main_role(self, value):
        user = self.context['request'].user
        requester_role = user.main_role.name
        
        try:
            role_instance = Role.objects.get(name=value)
        except Role.DoesNotExist:
            raise serializers.ValidationError("نقش وارد شده وجود ندارد.")

        if requester_role == 'admin':
            if value in ['superadmin', 'admin']:
                raise serializers.ValidationError("ادمین‌ها فقط می‌توانند دانشجو یا استاد تعریف کنند.")
        
        
        return role_instance

    def create(self, validated_data):
        with transaction.atomic():
            role = validated_data.pop('main_role')
            password = validated_data.pop('password')
            
            user = User.objects.create_user(
                password=password,
                scenario_credit=100,
                **validated_data
            )
            
            user.main_role = role
            user.save()
            return user
    
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    
class PersonalNumberLoginSerializer(serializers.Serializer):
    personal_number = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    
class LoginSerializer(serializers.ModelSerializer):
    main_role = serializers.CharField(source='main_role.name', read_only=True)
    university = serializers.CharField(source='university.english_name', read_only=True)
    faculty = serializers.CharField(source='faculty.name', read_only=True)
    department = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 
            'personal_number', 
            'username', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'profile_image', 
            'date_joined', 
            'is_active', 
            'is_staff', 
            'is_superuser',
            'main_role',
            'profile_image',
            'university',
            'faculty',
            'department',
            'major',
            ]

class SetProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']

    def validate_profile_image(self, value):
        limit_mb = 2
        if value.size > limit_mb * 1024 * 1024:
            raise serializers.ValidationError(f"حجم فایل نباید بیشتر از {limit_mb} مگابایت باشد.")

        return value

    def update(self, instance, validated_data):
        new_image = validated_data.get('profile_image')
        
        if new_image and instance.profile_image:
            if os.path.isfile(instance.profile_image.path):
                os.remove(instance.profile_image.path)
        
        return super().update(instance, validated_data)
        
class SendResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def send_otp(self):
        email = self.validated_data['email']

        send_reset_otp_task.delay(email)
        return f"OTP sending initiated for {email}"

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")

        try:
            user = User.objects.get(email=email, otp=otp)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or OTP.")

        if not user.otp_expiry or user.otp_expiry < timezone.now():
            raise serializers.ValidationError("OTP has expired. Please request a new one.")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]

        user.otp_verified = True
        user.pass_expiry = timezone.now() + timedelta(minutes=5)
        user.save()

        return "OTP verified successfully."

class ResetPassSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if not user.otp_verified:
            raise serializers.ValidationError("OTP not verified yet.")
        
        if not user.pass_expiry or user.pass_expiry < timezone.now():
            raise serializers.ValidationError("OTP has expired. Please request a new one.")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]

        user.set_password(new_password)
        user.otp = None
        user.otp_expiry = None
        user.otp_verified = False
        user.pass_expiry = None
        user.save()

        return "Password changed successfully."

class ChengePassSerializer(serializers.Serializer):
    personal_number = serializers.CharField()
    password = serializers.CharField(min_length=8)
    new_password = serializers.CharField(min_length=8)
    
    def validate_and_change_password(self, request):
        personal_number = request.data.get('personal_number', None)
        password = request.data.get('password', None)
        new_password = request.data.get('new_password', None)
        
        try:
            user = User.objects.get(personal_number=personal_number)
            if not check_password(password, user.password):
                return "Password is incorrect."
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")
        
        user.set_password(new_password)
        user.save()
        
        return "Your password Changed successfuly."

class ProfileSerializer(serializers.ModelSerializer):
    main_role = serializers.CharField(source='main_role.name', read_only=True)
    university = serializers.CharField(source='university.english_name', read_only=True)
    faculty = serializers.CharField(source='faculty.name', read_only=True)
    department = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "personal_number",
            "email",
            "phone_number",
            "last_login",
            "date_joined",
            "last_update",
            "scenario_credit",
            "is_active",
            "is_ban",
            "is_staff",
            "is_superuser",
            "profile_image",
            "main_role",
            "university",
            "faculty",
            "department",
            "major",
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'personal_number'}
        }

class UserSerializer(serializers.ModelSerializer):
    main_role = serializers.CharField(source='main_role.name', read_only=True)
    university = serializers.CharField(source='university.english_name', read_only=True)
    faculty = serializers.CharField(source='faculty.name', read_only=True)
    department = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "personal_number",
            "last_login",
            "profile_image",
            "main_role",
            "university",
            "faculty",
            "department",
            "major",
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'personal_number'}
        }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()