from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='list'),
    path('<slug:slug>/', views.ProjectDetailView.as_view(), name='detail'),
    path('category/<slug:category_slug>/', views.ProjectCategoryView.as_view(), name='category'),
]
