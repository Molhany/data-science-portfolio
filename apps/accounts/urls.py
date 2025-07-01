from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('request-project/', views.request_project_view, name='request_project'),
    path('purchase-project/', views.purchase_project, name='purchase_project'),
    path('payment/<int:purchase_id>/', views.payment_gateway, name='payment_gateway'),
    path('purchased-projects/', views.purchased_projects, name='purchased_projects'),
    path('privacy-settings/', views.PrivacySettingsView.as_view(), name='privacy_settings'),
]
