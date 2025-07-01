from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.SkillsView.as_view(), name='list'),
    path('api/skills-data/', views.skills_data_api, name='skills_data_api'),
]
