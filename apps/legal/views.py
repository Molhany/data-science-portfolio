from django.shortcuts import render
from django.views.generic import TemplateView


class PrivacyPolicyView(TemplateView):
    """Privacy Policy page"""
    template_name = 'legal/privacy_policy.html'


class TermsOfServiceView(TemplateView):
    """Terms of Service page"""
    template_name = 'legal/terms_of_service.html'


class CookiePolicyView(TemplateView):
    """Cookie Policy page"""
    template_name = 'legal/cookie_policy.html'


class DisclaimerView(TemplateView):
    """Disclaimer page"""
    template_name = 'legal/disclaimer.html'


class DataProtectionView(TemplateView):
    """Data Protection page"""
    template_name = 'legal/data_protection.html'
