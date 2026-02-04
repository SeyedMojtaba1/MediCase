import logging
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from university.models import University, Faculty, Department
import uuid

logger = logging.getLogger('registery')

class Role(models.Model):
    role_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            is_new = self._state.adding
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"Role created: {self.name} (ID: {self.role_id})")
            else:
                logger.info(f"Role updated: {self.name} (ID: {self.role_id})")
        except Exception as e:
            logger.error(f"Error saving Role {self.name}: {e}", exc_info=True)
            raise

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        try:
            if not email:
                raise ValueError("ایمیل مورد نیاز است!")
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save()
            logger.info(f"New user created via UserManager: {email}")
            return user
        except Exception as e:
            logger.error(f"Error creating user {email}: {e}", exc_info=True)
            raise

    def create_superuser(self, email, password=None, **extra_fields):
        try:
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            extra_fields.setdefault("is_active", True)

            if extra_fields.get("is_staff") is not True:
                raise ValueError("سوپر یوزر باید is_staff=True داشته باشد.")
            if extra_fields.get("is_superuser") is not True:
                raise ValueError("سوپر یوزر باید is_superuser=True داشته باشد.")

            user = self.create_user(email, password, **extra_fields)
            logger.warning(f"Superuser created: {email} (ID: {user.user_id})")
            return user
        except Exception as e:
            logger.error(f"Error creating superuser {email}: {e}", exc_info=True)
            raise

class User(AbstractBaseUser):
    MAJOR_TYPES=[
        ('پزشکی', 'Medicine'),
    ]
    
    username_validator = UnicodeUsernameValidator()

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
        blank=False
    )
    personal_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=80, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    scenario_credit = models.IntegerField(default=0)
    personal_credit = models.IntegerField(default=0)
    done_scenarios = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_ban = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        default='defaults/profile/default_profile.jpg',
    )
    otp = models.IntegerField(null=True, blank=True)
    otp_expiry = models.DateTimeField(null=True, blank=True)
    pass_expiry = models.DateTimeField(null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    main_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, related_name='users')
    university = models.ForeignKey(University, on_delete=models.SET_NULL, null=True, related_name='users_uni')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='users_faculty')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='users_department')
    major = models.CharField(default='پزشکی', choices=MAJOR_TYPES, max_length=30)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            is_new = self._state.adding
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"User registered: {self.email} (ID: {self.user_id})")
            else:
                logger.info(f"User profile updated: {self.email} (ID: {self.user_id})")
        except Exception as e:
            logger.error(f"Error saving User {self.email}: {e}", exc_info=True)
            raise
    
class UserRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            is_new = self._state.adding
            super().save(*args, **kwargs)
            if is_new:
                logger.info(f"Role '{self.role.name}' assigned to User '{self.user.email}'")
            else:
                logger.info(f"UserRole updated for User '{self.user.email}' - Role: '{self.role.name}'")
        except Exception as e:
            logger.error(f"Error saving UserRole: {e}", exc_info=True)
            raise
