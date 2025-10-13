from .models import User, UserRole, Role

from .serializer import (
    RegisterSerializer, 
    EmailLoginSerializer,
    SendResetOTPSerializer,
    VerifyOTPResetPassSerializer,
    ChengePassSerializer,
    ProfileSerializer,
)

from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework import generics, permissions

class SignupViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        try:
            role_name = request.data.get('role', None)
            if not role_name:
                raise ValueError("Role must be provided.")
            role = Role.objects.get(name=role_name)
            UserRole.objects.create(user=user, role=role)
        except Role.DoesNotExist:
            return Response({"detail": "Role does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except UserRole.DoesNotExist:
            return Response({"detail": "UserRole does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            "user": {
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": role.name,
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
        
        return Response({
            'email': user.email,
            'student_number': user.student_number,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_image': user.profile_image,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

@api_view(['POST'])
def send_reset_otp(request):
    serializer = SendResetOTPSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.send_otp(request=request)
    return Response({"message": message}, status=status.HTTP_200_OK)

@api_view(["POST"])
def verify_otp_reset_pass(request):
    serializer = VerifyOTPResetPassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.verify_otp(request=request)
    return Response({"message": message}, status=status.HTTP_200_OK)

@api_view(["POST"])
def chenge_pass(request):
    serializer = ChengePassSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    message = serializer.validate_and_change_password(request=request)
    return Response({"message": message}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [JWTAuthentication]
    serializer_class = ProfileSerializer
    lookup_field = "student_number"