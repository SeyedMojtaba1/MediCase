from rest_framework import viewsets
from rest_framework import permissions
from .serializer import SectionSerializer, SemesterSerializer
from .models import Section, Semester
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator

class SectionViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    lookup_field = 'name'
    lookup_value_regex = '[^/]+'
    @method_decorator(cache_page(20 * 15, cache="api_cache"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SemesterViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SemesterSerializer
    queryset = Semester.objects.all()

