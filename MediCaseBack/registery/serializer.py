from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
from .models import Role
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    main_role = serializers.CharField()
    
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
        ]
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            personal_number=validated_data['personal_number'],
            phone_number=validated_data.get('phone_number', ''),
        )
        
        try:
            role = Role.objects.get(name=validated_data['main_role'])
        except Role.DoesNotExist:
            return "Role is not exist."
        
        user.main_role = role
        
        def random_with_N_digits(n):
            range_start = 10**(n-1)
            range_end = (10**n)-1
            return randint(range_start, range_end)

        otp = random_with_N_digits(6)
        user.otp = otp
        user.save()

        subject = 'Please Confirm Your Account'
        message = 'Your 6 Digit Verification Pin: {}'.format(otp)
        email_from = '*****'
        recipient_list = [str(user.email), ]
        send_mail(subject, message, email_from, recipient_list)
        return user
    
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    
class PersonalNumberLoginSerializer(serializers.Serializer):
    personal_number = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)
    
class LoginSerializer(serializers.HyperlinkedModelSerializer):
    main_role = serializers.HyperlinkedRelatedField(
        view_name='role-detail',
        read_only=True,
        lookup_field='name'
    )
    university = serializers.HyperlinkedRelatedField(
        view_name='university-detail',
        read_only=True,
        lookup_field='name'
    )
    faculty = serializers.HyperlinkedRelatedField(
        view_name='faculty-detail',
        read_only=True,
        lookup_field='name'
    )
    department = serializers.HyperlinkedRelatedField(
        view_name='department-detail',
        read_only=True,
        lookup_field='name'
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()
    
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
            'access',
            'refresh',
            'main_role',
            'university',
            'faculty',
            'department'
            ]
        
    def get_access(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh.access_token)

    def get_refresh(self, obj):
        refresh = RefreshToken.for_user(obj)
        return str(refresh)
        
class SendResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def send_otp(self, request):
        email = request.data.get('email', None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        otp = randint(100000, 999999)
        user.otp = otp
        user.otp_expiry = timezone.now() + timedelta(minutes=5)
        user.save()

        subject = 'Please Confirm Your Account'
        message = f'Your 6-digit verification pin: {otp}\n\nThis code expires in 5 minutes.'
        email_from = '*****'
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)

        return f"OTP sent to {email}"   

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

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    main_role = serializers.HyperlinkedRelatedField(
        view_name='role-detail',
        read_only=True
    )
    
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
        ]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['name']
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()