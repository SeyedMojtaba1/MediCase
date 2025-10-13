from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.LoginView.as_view(), name='login'),
   path('sendresetotp/', views.send_reset_otp, name='send_reset_otp'),
   path('verifyotpresetpass/', views.verify_otp_reset_pass, name='verify_otp_reset_pass'),
   path('chengepass/', views.chenge_pass, name='chenge_pass'),
   path('userprofile/<str:student_number>/', views.ProfileView.as_view(), name='user_profile'),
]