import logging
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

logger = logging.getLogger('registery')

class RegisterAuthentication(BaseAuthentication):
    def authenticate(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return None

        User = get_user_model()
        logger.debug(f"Authentication attempt for email: {email}")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.warning(f"Authentication failed: User with email '{email}' not found.")
            raise AuthenticationFailed('No such user')

        if not user.check_password(password):
            logger.warning(f"Authentication failed: Invalid password for user '{user.email}' (ID: {user.id}).")
            raise AuthenticationFailed('Invalid password')

        logger.info(f"User '{user.email}' (ID: {user.id}) authenticated successfully via RegisterAuthentication.")
        return (user, None)
