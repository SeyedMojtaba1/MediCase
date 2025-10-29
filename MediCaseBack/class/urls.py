from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'semesters', views.SemesterViewSet, basename='semester')
router.register(r'subjects', views.SubjectViewSet, basename='subject')

urlpatterns = [
   path('', include(router.urls)),
   path('sectioncreate/', views.SectionCreateView.as_view(), name='sectioncreate'),
   path('studentsubjectcreate/', views.StudentSubjectCreateView.as_view(), name='studentsubjectcreate'),
   path('studentsubjectlist/', views.StudentSubjectListView.as_view(), name='studentsubjectlist'),
   path('studentsubjectretrieve/<str:subject>/', views.StudentSubjectRetrieveView.as_view(), name='studentsubjectretrieve'),
]