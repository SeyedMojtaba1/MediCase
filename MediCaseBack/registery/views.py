from .models import User, Role

from .serializer import (
    RegisterSerializer, 
    LoginSerializer,
    EmailLoginSerializer,
    SendResetOTPSerializer,
    VerifyOTPSerializer,
    ResetPassSerializer,
    ChengePassSerializer,
    ProfileSerializer,
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
            return Response({"detail": "email or password is incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
        
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
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="None",
            max_age = 10 * 60,
        )

        return response

@extend_schema(
    request=SendResetOTPSerializer
)
@api_view(['POST'])
def send_reset_otp(request):
    serializer = SendResetOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.send_otp(request=request)
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
@permission_classes([JWTAuthentication])
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
    
    def get_object(self):
        return self.request.user

class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

class LogoutView(generics.GenericAPIView):
    permission_classes =[JWTAuthentication]
    serializer_class = LogoutSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        refresh = serializer.validated_data['refresh']
        
        try:
            token = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh = request.COOKIES.get('refresh_token')

        if refresh is None:
            return Response({'detail': 'No refresh token cookie found'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TokenRefreshSerializer(data={'refresh': refresh})
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data['access']

        response = Response({'access': access}, status=status.HTTP_200_OK)
        return response