from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'universities', views.UniversityViewSet, basename='university')
router.register(r'faculties', views.FacultyViewSet, basename='faculty')
router.register(r'departments', views.DepartmentViewSet, basename='department')

urlpatterns = [
   path('', include(router.urls)),
]