from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from drf_spectacular.utils import extend_schema
from .serializer import ScenarioCreateSerializer, ScenarioRetrieveSerializer
from .models import PulmonologyScenario
from .scenario_creator import scenario_creator
from django.contrib.auth import get_user_model
from .utils import senario_creator_celery
import secrets
import string

User = get_user_model()

ALPHABET = string.ascii_uppercase + string.digits

def generate_tracking_code(length: int = 10) -> str:
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))

@extend_schema(
    responses=ScenarioCreateSerializer
)
@authentication_classes([JWTAuthentication])
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def scenario_create(request):
    user = request.user
    
    try:
        user = User.objects.get(personal_number=user.personal_number)
    except User.DoesNotExist:
        return Response(
            {"detail": "User is not exist."}
        )
    
    if user.scenario_credit <= 0:
        return Response(
            {"detail": "User Have not enough credit."}
        )
        
    tracking_code = generate_tracking_code(10)
    senario_creator_celery.delay(user.personal_number, tracking_code)

    return Response({"tracking_code": tracking_code}, status=status.HTTP_200_OK)

class ScenarioRetrieveView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScenarioRetrieveSerializer
    queryset = PulmonologyScenario.objects.all()
    lookup_field = 'tracking_code'
    lookup_value_regex = '[^/]+'
    
    # def retrieve(self, request, *args, **kwargs):
    #     serializer = self.get_queryset(data=request.data)
    #     serializer.is_valid(raise_exception=True)
        