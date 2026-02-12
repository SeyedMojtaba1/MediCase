from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TutorialViewSet, TutorialPageViewSet

router = DefaultRouter()
router.register(r'tutorials', TutorialViewSet, basename='tutorial')
router.register(r'pages', TutorialPageViewSet, basename='tutorial-page')

urlpatterns = [
    path('', include(router.urls)),
]