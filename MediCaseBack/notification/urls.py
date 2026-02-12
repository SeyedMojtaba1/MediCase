from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SystemAnnouncementViewSet,
    UniversityAnnouncementViewSet,
    SectionAnnouncementViewSet
)

router = DefaultRouter()
# آدرس‌دهی جداگانه برای هر سطح
router.register(r'system', SystemAnnouncementViewSet, basename='notification-system')
router.register(r'university', UniversityAnnouncementViewSet, basename='notification-university')
router.register(r'section', SectionAnnouncementViewSet, basename='notification-section')

urlpatterns = [
    path('', include(router.urls)),
]