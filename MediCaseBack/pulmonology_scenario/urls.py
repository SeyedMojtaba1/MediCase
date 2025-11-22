from django.urls import path, include
from . import views

urlpatterns = [
   path('scenariocreate/', views.scenario_create, name='scenariocreate'),
   path('scenarioretrieve/<str:tracking_code>/', views.ScenarioRetrieveView.as_view(), name='scenarioretrieve'),
   path('feedbackcreate/<str:scenario_tracking_code>', views.feedback_create, name='feedbackcreate'),
   path('feedbackretrieve/<str:tracking_code>/', views.FeedbackRetrieveView.as_view(), name='feedbackretrieve'),
]
