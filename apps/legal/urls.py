from django.urls import path
from . import views

app_name = 'legal'

urlpatterns = [
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('terms-of-service/', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    path('cookie-policy/', views.CookiePolicyView.as_view(), name='cookie_policy'),
    path('disclaimer/', views.DisclaimerView.as_view(), name='disclaimer'),
    path('data-protection/', views.DataProtectionView.as_view(), name='data_protection'),
]
