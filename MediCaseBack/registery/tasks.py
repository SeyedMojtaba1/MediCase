from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from random import randint
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

@shared_task
def send_reset_otp_task(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return "User does not exist."

    otp = randint(100000, 999999)
    user.otp = otp
    user.otp_expiry = timezone.now() + timedelta(minutes=5)
    user.save()

    subject = '🔐 حسابت رو احراز هویت کن.'
    from_email = settings.EMAIL_HOST_USER
    to = [user.email]

    text_content = f"""
    کد تأیید شما: {otp}
    این کد تا ۵ دقیقه دیگر منقضی می‌شود.
    """

    html_content = f"""
    <html lang="fa" dir="rtl">
        <body style="font-family: Tahoma, 'Vazirmatn', sans-serif; background-color: #E0F2F1; padding: 30px;">
            <div style="max-width: 520px; margin: auto; background-color: #fff; border-radius: 12px; padding: 35px 30px;">
                <h2 style="color: #00695C; text-align: center;">تأیید حساب کاربری</h2>
                <p>کد شما: <strong>{otp}</strong></p>
                <p>این کد تا ۵ دقیقه دیگر منقضی می‌شود.</p>
            </div>
        </body>
    </html>
    """

    email_message = EmailMultiAlternatives(subject, text_content, from_email, to)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    return f"OTP sent to {email}"
