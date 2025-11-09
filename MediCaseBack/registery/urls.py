from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'roles', views.RoleViewSet, basename='role')
router.register(r"signup", views.SignupViewSet, basename="signup")
router.register(r"setprofileimage", views.SetProfileImageViewSet, basename="setprofileimage")
router.register(r"users", views.UserViewSet, basename='user')

urlpatterns = [
   path('login/', views.LoginView.as_view(), name='login'),
   path('sendresetotp/', views.send_reset_otp, name='send_reset_otp'),
   path('verifyotp/', views.verify_otp, name='verify_otp'),
   path('resetpass/', views.reset_pass, name='reset_pass'),
   path('chengepass/', views.chenge_pass, name='chenge_pass'),
   path('chengepass/', views.chenge_pass, name='chenge_pass'),
   path('userprofile/', views.ProfileView.as_view(), name='user_profile'),
   path('logout/', views.LogoutView.as_view(), name='logout'),
   path('token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
   path('', include(router.urls)),
]