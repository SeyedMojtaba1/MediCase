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
import pandas as pd
from rest_framework.response import Response
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, parsers
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework.throttling import ScopedRateThrottle
from django.conf import settings
from .permission import IsAdminOrSuperAdmin

class SignupViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [IsAdminOrSuperAdmin]
    
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def create(self, request):
        if 'file' in request.FILES:
            return self._bulk_create(request)
            
        return self._single_create(request)

    def _single_create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        data = {
            "user": {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.main_role.name if user.main_role else None,
            },
            "message": "ثبت نام تکی با موفقیت انجام شد."
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def _bulk_create(self, request):
        file = request.FILES['file']
        
        if not file.name.endswith('.xlsx'):
            return Response({"error": "فرمت فایل باید xlsx باشد."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file)
            df.dropna(how='all', inplace=True)
        except Exception as e:
            return Response({"error": f"مشکل در خواندن فایل: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        created_users = []
        errors = []

        for index, row in df.iterrows():
            row_data = row.to_dict()
            
            # پاکسازی داده‌ها
            clean_data = {
                'email': row_data.get('email'),
                'username': row_data.get('username'),
                'password': str(row_data.get('password')),
                'first_name': row_data.get('first_name'),
                'last_name': row_data.get('last_name'),
                'phone_number': str(row_data.get('phone_number', '')).replace('.0', ''),
                'personal_number': str(row_data.get('personal_number', '')).replace('.0', ''),
                'main_role': row_data.get('main_role'),
                'major': row_data.get('major'),
            }

            serializer = RegisterSerializer(data=clean_data, context={'request': request})

            if serializer.is_valid():
                try:
                    user = serializer.save()
                    created_users.append({
                        "row": index + 2,
                        "username": user.username,
                        "status": "Success"
                    })
                except Exception as e:
                    errors.append({"row": index + 2, "username": clean_data.get('username'), "error": str(e)})
            else:
                errors.append({"row": index + 2, "username": clean_data.get('username'), "error": serializer.errors})

        response_data = {
            "mode": "bulk",
            "summary": {
                "total": len(df),
                "success": len(created_users),
                "failed": len(errors),
            },
            "successful": created_users,
            "failed": errors
        }
        
        status_code = status.HTTP_201_CREATED if len(errors) == 0 else status.HTTP_207_MULTI_STATUS
        return Response(response_data, status=status_code)

class LoginView(generics.GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'login' 
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request=request, email=email, password=password)

        if not user:
            return Response({"detail": "ایمیل یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        output_serializer = LoginSerializer(user, context={'request': request})
        
        response = Response(
            {
                "user": output_serializer.data,
                "access_token": access_token,
            },
            status=status.HTTP_200_OK
        )

        is_production = not settings.DEBUG 
        
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=is_production,
            samesite="Lax" if not is_production else "Strict",
            max_age=7 * 24 * 60 * 60,
            path="/"
        )

        return response

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
#                 "refresh_token": str(refresh),
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

class SetProfileImageView(generics.UpdateAPIView):
    serializer_class = SetProfileImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        
        return Response(
            {"message": "تصویر پروفایل با موفقیت به‌روزرسانی شد.", "url": response.data.get('profile_image')},
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
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    # نیازی به authentication_classes نیست اگر در settings.py تنظیم شده باشد
    # اما بودنش هم ضرری ندارد.
    
    def get_object(self):
        # این کوئری تمام 5 درخواست را تبدیل به 1 درخواست می‌کند (Join SQL)
        queryset = User.objects.select_related(
            'main_role', 
            'university', 
            'faculty', 
            'department'
        )
        return get_object_or_404(queryset, pk=self.request.user.pk)

class UserViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'personal_number'
    lookup_value_regex = '[^/]+'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'personal_number']

    def get_queryset(self):
        queryset = User.objects.select_related(
            'main_role', 
            'university', 
            'faculty', 
            'department'
        ).all()
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
            
        return queryset

class RoleViewSet(ReadOnlyModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'

    @method_decorator(cache_page(20 * 60, key_prefix="role_api"))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except (TokenError, Exception):
                pass
        
        response = Response({"detail": "با موفقیت خارج شدید."}, status=status.HTTP_200_OK)
        
        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="Lax" 
        )

        return response

# class LogoutView(generics.GenericAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = LogoutSerializer
    
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         refresh = serializer.data['refresh']
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

class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response(
                {'detail': 'رفرش توکن یافت نشد. لطفاً مجدد وارد شوید.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data={'refresh': refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            response = Response({'detail': 'توکن نامعتبر است.'}, status=status.HTTP_401_UNAUTHORIZED)
            response.delete_cookie('refresh_token')
            return response

        validated_data = serializer.validated_data
        access_token = validated_data['access']

        response = Response({'access': access_token}, status=status.HTTP_200_OK)

        if 'refresh' in validated_data:
            new_refresh_token = validated_data['refresh']
            
            is_production = not settings.DEBUG
            response.set_cookie(
                key="refresh_token",
                value=new_refresh_token,
                httponly=True,
                secure=is_production,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,
                path="/"
            )

        return response
    
# class CookieTokenRefreshView(TokenRefreshView):
#     serializer_class = LogoutSerializer
    
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         refresh = serializer.data['refresh']

#         if refresh is None:
#             return Response({'detail': 'No refresh token cookie found'}, status=status.HTTP_401_UNAUTHORIZED)

#         serializer = TokenRefreshSerializer(data={'refresh': refresh})
#         serializer.is_valid(raise_exception=True)

#         access = serializer.validated_data['access']

#         response = Response({'access': access, "refresh": str(refresh)}, status=status.HTTP_200_OK)
#         response.set_cookie(
#             key="refresh_token",
#             value=str(refresh),
#             httponly=True,
#             secure=False,
#             samesite="Lax",
#             max_age = 7 * 24 * 60 * 60,
#         )
#         return response