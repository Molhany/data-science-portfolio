from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import ContactMessage, NewsletterSubscription


class ContactView(TemplateView):
    """Contact form page"""
    template_name = 'contact/contact.html'
    
    def post(self, request, *args, **kwargs):
        """Handle contact form submission"""
        try:
            # Get form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            company = request.POST.get('company', '').strip()
            website = request.POST.get('website', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            message_type = request.POST.get('message_type', 'general')
            
            # Basic validation
            if not all([name, email, subject, message]):
                messages.error(request, 'Please fill in all required fields.')
                return self.get(request, *args, **kwargs)
            
            # Create contact message
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                company=company,
                website=website,
                subject=subject,
                message=message,
                message_type=message_type,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                referrer=request.META.get('HTTP_REFERER', '')
            )
            
            messages.success(request, 'Thank you for your message! I\'ll get back to you soon.')
            return redirect('contact:success')
            
        except Exception as e:
            messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
            return self.get(request, *args, **kwargs)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class ContactSuccessView(TemplateView):
    """Contact form success page"""
    template_name = 'contact/success.html'


@csrf_exempt
def newsletter_signup(request):
    """Handle newsletter signup via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email', '').strip()
            name = data.get('name', '').strip()
            interests = data.get('interests', '').strip()
            
            if not email:
                return JsonResponse({'success': False, 'message': 'Email is required.'})
            
            # Check if already subscribed
            if NewsletterSubscription.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'You are already subscribed!'})
            
            # Create subscription
            subscription = NewsletterSubscription.objects.create(
                email=email,
                name=name,
                interests=interests,
                ip_address=get_client_ip(request),
                source='website_footer'
            )
            
            return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
