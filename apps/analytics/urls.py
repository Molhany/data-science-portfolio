from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsView.as_view(), name='dashboard'),
    path('api/portfolio-stats/', views.portfolio_stats_api, name='portfolio_stats_api'),
]
