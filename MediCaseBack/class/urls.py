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
   path('sectionupdate/<uuid:section_id>', views.SectionUpdateViewSet.as_view({'put': 'update'}), name='sectionupdate'),
   path('studentsectioncreate/', views.StudentSectionCreateView.as_view(), name='studentsectioncreate'),
   path('studentsectionlist/', views.StudentSectionListView.as_view(), name='studentsectionlist'),
   path('studentsectionretrieve/<str:section>/', views.StudentSectionRetrieveView.as_view(), name='studentsectionretrieve'),
   path('studentsubjectcreate/', views.StudentSubjectCreateView.as_view(), name='studentsubjectcreate'),
   path('studentsubjectlist/', views.StudentSubjectListView.as_view(), name='studentsubjectlist'),
   path('studentsubjectretrieve/<str:subject>/', views.StudentSubjectRetrieveView.as_view(), name='studentsubjectretrieve'),
]