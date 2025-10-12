from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.LoginView.as_view(), name='login'),
   path('send_reset_otp/', views.send_reset_otp, name='send_reset_otp'),
   path('verify_otp_reset_pass/', views.verify_otp_reset_pass, name='verify_otp_reset_pass'),
]