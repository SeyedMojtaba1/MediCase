from django.urls import path, include
from . import views

urlpatterns = [
   path('scenariocreate/', views.scenario_create, name='scenariocreate'),
   path('scenarioretrieve/<str:tracking_code>/', views.ScenarioRetrieveView.as_view(), name='scenarioretrieve'),
   path('scenariolist/', views.ScenarioListView.as_view(), name='scenariolist'),
   path('feedbackcreate/<str:scenario_tracking_code>', views.feedback_create, name='feedbackcreate'),
   path('feedbackretrieve/<str:tracking_code>/', views.FeedbackRetrieveView.as_view(), name='feedbackretrieve'),
   path('feedbacklist/', views.FeedbackListView.as_view(), name='feedbacklist'),
   path('studentranking/', views.StudentRankingListView.as_view(), name='studentranking'),
   path('sectionleaderboard/<str:section_id>/', views.SectionLeaderboardView.as_view()),
   path('studentrankinsection/<str:section_id>/', views.StudentRankInSectionView.as_view()),
   path('feedbackrankinsection/<str:tracking_code>/', views.FeedbackRankInSectionView.as_view()),
   path('sectionleaderboard/<str:section_id>/', views.SectionLeaderboardBySectionIdView.as_view()),
   path('daily-scenario/start/', views.GetDailyScenarioView.as_view(), name='start-daily-scenario'),
   path('daily-scenario/ranking/', views.DailyScenarioRankingView.as_view(), name='daily-scenario-ranking'),
   path('advancedranking/', views.AdvancedUniversityRankingView.as_view(), name='advanced-ranking'),
   path('toggle-share-feedback/<str:tracking_code>/', views.toggle_feedback_share, name='toggle-share-feedback'),
   path('shared-feedback/<str:tracking_code>/', views.SharedFeedbackRetrieveView.as_view(), name='shared-feedback-retrieve'),
]
