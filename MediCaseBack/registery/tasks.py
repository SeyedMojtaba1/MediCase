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
    <body style="font-family: Tahoma, 'Vazirmatn', sans-serif; background-color: #E0F2F1; padding: 30px; direction: rtl;">
        <div style="max-width: 520px; margin: auto; background-color: #ffffff; border-radius: 12px; padding: 35px 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); text-align: right;">

        <h2 style="color: #00695C; text-align: center; margin-bottom: 25px;">
            تأیید حساب کاربری
        </h2>

        <p style="font-size: 16px; color: #444; line-height: 1.8;">
            سلام <strong>{user.first_name or 'کاربر گرامی'}</strong> 🌷،<br><br>
            رمز عبور یکبار مصرف (OTP) شما برای تأیید حساب:
        </p>

        <div style="text-align: center; margin: 30px 0;">
            <span style="display: inline-block; background-color: #009688; color: #fff; padding: 12px 26px; font-size: 22px; font-weight: bold; letter-spacing: 4px; border-radius: 8px;">
            {otp}
            </span>
        </div>

        <p style="font-size: 15px; color: #666; line-height: 1.7;">
            ⚠️ این کد تا <strong>۵ دقیقه</strong> دیگر منقضی می‌شود.<br>
            اگر شما این درخواست را انجام نداده‌اید، لطفاً این ایمیل را نادیده بگیرید.
        </p>

        <hr style="margin: 30px 0; border: none; border-top: 1px solid #e0e0e0;">

        <p style="text-align: center; font-size: 13px; color: #999;">
            &copy; {timezone.now().year} MediCase-Isfahan<br>
            تمامی حقوق محفوظ است.
        </p>
        </div>
    </body>
    </html>
    """

    email_message = EmailMultiAlternatives(subject, text_content, from_email, to)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

    return f"OTP sent to {email}"
