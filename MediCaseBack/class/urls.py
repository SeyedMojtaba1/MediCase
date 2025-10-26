from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'semesters', views.SemesterViewSet, basename='semester')

urlpatterns = [
   path('', include(router.urls)),
]