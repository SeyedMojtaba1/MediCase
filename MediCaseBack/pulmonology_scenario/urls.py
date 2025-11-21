from django.urls import path, include
from . import views

urlpatterns = [
   path('scenariocreate/', views.scenario_create, name='scenariocreate'),
   path('scenarioretrieve/<str:tracking_code>/', views.ScenarioRetrieveView.as_view(), name='scenarioretrieve')
]
