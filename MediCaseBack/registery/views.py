from .models import User, Role

from .serializer import (
    RegisterSerializer, 
    LoginSerializer,
    SetProfileImageSerializer,
    EmailLoginSerializer,
    SendResetOTPSerializer,
    VerifyOTPSerializer,
    ResetPassSerializer,
    ChengePassSerializer,
    ProfileSerializer,
    UserSerializer,
    RoleSerializer,
    LogoutSerializer,
)

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

class SignupViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        try:
            role = Role.objects.get(name=serializer.data['main_role'])
        except Role.DoesNotExist:
            return Response({"detail": "Role is not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            "user": {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "main_role": role.name,
            },
            "message": "ثبت نام با موفقیت انجام شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)

# class LoginView(generics.CreateAPIView):
#     serializer_class = EmailLoginSerializer
#     permission_classes = [permissions.AllowAny]
#     queryset = User.objects.all()
    
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         email = serializer.validated_data['email']
#         password = serializer.validated_data['password']  

#         user = authenticate(email=email, password=password)

#         if not user:
#             return Response({"detail": "email or password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
#         refresh = RefreshToken.for_user(user)
#         access_token = str(refresh.access_token)
        
#         output_serializer = LoginSerializer(
#             user,
#             context={'request': request}
#         )
        
#         response = Response(
#             {
#                 "user": output_serializer.data,
#                 "access_token": access_token,
#             },
#             status=status.HTTP_200_OK
#         )

#         response.set_cookie(
#             key="refresh_token",
#             value=str(refresh),
#             httponly=True,
#             secure=False,
#             samesite="Lax",
#             max_age = 7 * 24 * 60 * 60,
#         )

#         return response

class LoginView(generics.CreateAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']  

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"detail": "email or password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        output_serializer = LoginSerializer(
            user,
            context={'request': request}
        )
        
        response = Response(
            {
                "user": output_serializer.data,
                "access_token": access_token,
                "refresh_token": str(refresh),
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age = 7 * 24 * 60 * 60,
        )

        return response

class SetProfileImageView(generics.UpdateAPIView):
    serializer_class = SetProfileImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, personal_number=self.request.user.personal_number)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "تصویر با موفقیت ویرایش شد."},
            status=status.HTTP_200_OK
        )

@extend_schema(
    request=SendResetOTPSerializer
)
@api_view(['POST'])
def send_reset_otp(request):
    serializer = SendResetOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.send_otp()
    return Response({"message": message}, status=status.HTTP_200_OK)

@extend_schema(
    request=VerifyOTPSerializer
)
@api_view(["POST"])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.save()
    return Response({"message": message}, status=status.HTTP_200_OK)

@extend_schema(
    request=ResetPassSerializer
)
@api_view(["POST"])
def reset_pass(request):
    serializer = ResetPassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.save()
    return Response({"message": message}, status=status.HTTP_200_OK)

@extend_schema(
    request=ChengePassSerializer
)
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def chenge_pass(request):
    serializer = ChengePassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.validate_and_change_password(request=request)
    return Response({"message": message}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'personal_number'
    lookup_value_regex = '[^/]+'
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class RoleViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 60, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# class LogoutView(generics.GenericAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request):
#         refresh = request.COOKIES.get('refresh_token')
#         if not refresh:
#             return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             token = RefreshToken(refresh)
#             token.blacklist()
#         except Exception:
#             return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
#         response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#         response.delete_cookie('refresh_token')

#         return response

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.data['refresh']
        if not refresh:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')

        return response

# class CookieTokenRefreshView(TokenRefreshView):
#     def get(self, request):
#         refresh = request.COOKIES.get('refresh_token')

#         if refresh is None:
#             return Response({'detail': 'No refresh token cookie found'}, status=status.HTTP_401_UNAUTHORIZED)

#         serializer = TokenRefreshSerializer(data={'refresh': refresh})
#         serializer.is_valid(raise_exception=True)

#         access = serializer.validated_data['access']

#         response = Response({'access': access}, status=status.HTTP_200_OK)
#         return response
    
class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = LogoutSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.data['refresh']

        if refresh is None:
            return Response({'detail': 'No refresh token cookie found'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TokenRefreshSerializer(data={'refresh': refresh})
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data['access']

        response = Response({'access': access, "refresh": str(refresh)}, status=status.HTTP_200_OK)
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age = 7 * 24 * 60 * 60,
        )
        return response