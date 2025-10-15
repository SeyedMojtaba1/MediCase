from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')

urlpatterns = [
   path('login/', views.LoginView.as_view(), name='login'),
   path('sendresetotp/', views.send_reset_otp, name='send_reset_otp'),
   path('verifyotpresetpass/', views.verify_otp_reset_pass, name='verify_otp_reset_pass'),
   path('chengepass/', views.chenge_pass, name='chenge_pass'),
   path('userprofile/<str:personal_number>/', views.ProfileView.as_view(), name='user_profile'),
   path('', include(router.urls)),
]