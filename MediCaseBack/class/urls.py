from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'semesters', views.SemesterViewSet, basename='semester')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r"setsectionimage", views.SetSectionImageViewSet, basename="setsectionimage")
router.register(r'hospitals', views.HospitalViewSet, basename='hospital')

urlpatterns = [
   path('', include(router.urls)),
   path('sectionlist/', views.SectionListView.as_view(), name='sectionlist'),
   path('sectionretrieve/<str:section_id>/', views.SectionRetrieveView.as_view(), name='sectionretrieve'),
   path('sectioncreate/', views.SectionCreateView.as_view(), name='sectioncreate'),
   path('sectionupdate/<str:section_id>/', views.SectionUpdateViewSet.as_view({'put': 'update'}), name='sectionupdate'),
   path('studentsectioncreate/', views.StudentSectionCreateView.as_view(), name='studentsectioncreate'),
   path('studentsectionlist/', views.StudentSectionListView.as_view(), name='studentsectionlist'),
   path('studentsectionretrieve/<str:section_id>/', views.StudentSectionRetrieveView.as_view(), name='studentsectionretrieve'),
   path('studentsectionremove/', views.StudentSectionRemoveView.as_view(), name='studentsectionremove'),
   path('memberssectiontlist/<str:section_id>/', views.MembersSectionListView.as_view(), name='memberssectionlist'),
   path('studentsubjectcreate/', views.StudentSubjectCreateView.as_view(), name='studentsubjectcreate'),
   path('studentsubjectlist/', views.StudentSubjectListView.as_view(), name='studentsubjectlist'),
   path('studentsubjectretrieve/<str:subject>/', views.StudentSubjectRetrieveView.as_view(), name='studentsubjectretrieve'),
   path('hospitalsubjectcreate/', views.HospitalSubjectCreateView.as_view(), name='hospitalsubjectcreate'),
   path('hospitalsubjectlist/', views.HospitalSubjectListView.as_view(), name='hospitalsubjectlist'),
   path('hospitalsubjectretrieve/<str:subject>/', views.HospitalSubjectRetrieveView.as_view(), name='hospitalsubjectretrieve'),
]