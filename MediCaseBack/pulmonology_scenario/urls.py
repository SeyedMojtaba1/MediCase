from django.urls import path, include
from . import views

urlpatterns = [
   path('scenariocreate/', views.scenario_create, name='scenariocreate'),
   path('scenarioretrieve/<str:tracking_code>/', views.ScenarioRetrieveView.as_view(), name='scenarioretrieve'),
   path('scenariolist/<str:personal_number>/', views.ScenarioListView.as_view(), name='scenariolist'),
   path('feedbackcreate/<str:scenario_tracking_code>', views.feedback_create, name='feedbackcreate'),
   path('feedbackretrieve/<str:tracking_code>/', views.FeedbackRetrieveView.as_view(), name='feedbackretrieve'),
   path('feedbacklist/<str:personal_number>/', views.FeedbackListView.as_view(), name='feedbacklist'),
   path('studentranking/', views.StudentRankingListView.as_view(), name='studentranking'),
   path('sectionleaderboard/<str:section_id>/', views.SectionLeaderboardView.as_view()),
   path('studentrankinsection/<str:section_id>/', views.StudentRankInSectionView.as_view()),
]
