from asyncio.log import logger
from rest_framework import serializers
from django.conf import settings
from kavenegar import *
from django.contrib.auth import get_user_model
from random import randint
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from .models import Role
from rest_framework_simplejwt.tokens import RefreshToken
from classroom.serializer import StudentCreditSerializer
from django.core.mail import EmailMultiAlternatives
from classroom.models import Subject, StudentCredit
import environ
from .utils import send_reset_otp_task
import logging
import random
import datetime

logger = logging.getLogger('registery')
env = environ.Env()
environ.Env.read_env(env_file='./secrets/secrets.env')

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    main_role = serializers.CharField()
    # فیلد ورودی برای نام درس (فقط نوشتن)
    subject_name = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'email', 
            'username', 
            'first_name', 
            'last_name', 
            'password', 
            'phone_number', 
            'personal_number', 
            'main_role',
            'major',
            'subject_name', 
            'university',
        ]
    
    def create(self, validated_data):
        subject_name = validated_data.pop('subject_name', None)
        university = validated_data.pop('university', None)
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            scenario_credit=0,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            personal_number=validated_data['personal_number'],
            phone_number=validated_data.get('phone_number', ''),
            major=validated_data['major'],
            university=university,
        )
        
        try:
            role = Role.objects.get(name=validated_data['main_role'])
            user.main_role = role
        except Role.DoesNotExist:
            # در صورت نبود نقش، می‌توان خطا داد یا نقش پیش‌فرض گذاشت
            pass
        
        user.save()

        # منطق اختصاص کردیت به درس و آپدیت کردیت کلی
        if subject_name:
            subject = Subject.objects.filter(english_name=subject_name).first()
            if subject:
                credit_amount = 100
                
                # 1. ایجاد کردیت اختصاصی برای درس
                StudentCredit.objects.create(
                    user=user,
                    subject=subject,
                    balance=credit_amount
                )
                
                # 2. اضافه کردن به کردیت کلی کاربر (مجموع همه درس‌ها)
                user.scenario_credit += credit_amount
                user.save() # ذخیره تغییرات در مدل User
                
            else:
                logger.warning(f"Subject '{subject_name}' not found for user {user.username}")

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
    
    def update(self, instance, validated_data):
        profile_image=validated_data['profile_image']
        
        instance.profile_image = profile_image
        
        instance.save()
        return instance
        
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
    
    def validate(self, attrs):
        personal_number = attrs.get('personal_number')
        password = attrs.get('password')
        
        try:
            user = User.objects.get(personal_number=personal_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"personal_number": "کاربر یافت نشد."})
            
        if not check_password(password, user.password):
            raise serializers.ValidationError({"password": "رمز عبور فعلی اشتباه است."})
            
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        
        user.set_password(new_password)
        user.save()
        
        return "رمز عبور با موفقیت تغییر کرد."

class ProfileSerializer(serializers.ModelSerializer):
    main_role = main_role = serializers.CharField(source='main_role.name', read_only=True)
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
    credits = StudentCreditSerializer(source='subject_credits', many=True, read_only=True)
    
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
            "credits",
        ]
        extra_kwargs = {
            'url': {'lookup_field': 'personal_number'}
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return self.get_public_fields(ret)

        current_user = request.user
        role_name = current_user.main_role.name.lower() if current_user.main_role else ""

        if current_user.is_superuser or role_name == 'superadmin':
            return ret

        if role_name == 'admin':
            return self.get_public_fields(ret)

        if role_name == 'teacher':
            return self.get_public_fields(ret)

        else:
            return self.get_public_fields(ret)

    def get_public_fields(self, data):
        public_fields = [
            "first_name",
            "last_name",
            "username",
            "profile_image",
            "university",
            "major",
        ]
        return {key: value for key, value in data.items() if key in public_fields}

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()

class SendMobileOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, required=True)

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) < 10:
            raise serializers.ValidationError("شماره موبایل معتبر نیست.")
        return value

    def send_otp(self):
        phone = self.validated_data['phone_number']
        logger.info(f"OTP Request initiated for phone number: {phone}")
        
        user = User.objects.filter(phone_number=phone).first()
        if not user:
            logger.warning(f"OTP Request failed: User not found for phone {phone}")
            raise serializers.ValidationError("کاربری با این شماره موبایل یافت نشد.")

        otp_code = random.randint(100000, 999999)
        
        user.otp = otp_code
        user.otp_expiry = timezone.now() + datetime.timedelta(minutes=2)
        user.save()
        logger.info(f"OTP generated for user {user.email} (Phone: {phone})")

        try:
            api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
            params = {
                'receptor': phone,
                'template': 'verify',
                'token': str(otp_code),
                'type': 'sms',
            }
            response = api.verify_lookup(params)
            logger.info(f"OTP SMS sent successfully via Kavenegar to {phone}")
            return "کد تایید با موفقیت ارسال شد."
            
        except APIException as e:
            logger.error(f"Kavenegar APIException for {phone}: {e}", exc_info=True)
            raise serializers.ValidationError(f"خطای API کاوه نگار: {e}")
        except HTTPException as e:
            logger.error(f"Kavenegar HTTPException for {phone}: {e}", exc_info=True)
            raise serializers.ValidationError(f"خطای شبکه کاوه نگار: {e}")

class VerifyMobileOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15, required=True)
    otp = serializers.IntegerField(required=True)

    def verify(self):
        phone = self.validated_data['phone_number']
        received_otp = self.validated_data['otp']
        
        logger.info(f"OTP Verification attempt for phone: {phone}")

        user = User.objects.filter(phone_number=phone).first()
        if not user:
            logger.warning(f"OTP Verify failed: User not found for phone {phone}")
            raise serializers.ValidationError("کاربر یافت نشد.")

        if user.otp is None or user.otp != received_otp:
            logger.warning(f"OTP Verify failed: Invalid code for user {user.email}")
            raise serializers.ValidationError("کد تایید اشتباه است.")

        if user.otp_expiry and timezone.now() > user.otp_expiry:
            logger.warning(f"OTP Verify failed: Expired code for user {user.email}")
            raise serializers.ValidationError("کد تایید منقضی شده است.")

        user.otp_verified = True
        user.otp = None
        user.save()
        
        logger.info(f"OTP Verified successfully for user {user.email} (ID: {user.pk})")

        refresh = RefreshToken.for_user(user)
        
        return {
            "message": "احراز هویت موفقیت‌آمیز بود.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.pk
        }