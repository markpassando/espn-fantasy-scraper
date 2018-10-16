from django.urls import path
from . import views

urlpatterns = [
  path('getLeagueStandings/', views.GetLeagueStandings.as_view()),
  path('getDraftRecap/', views.GetDraftRecap.as_view()),
]