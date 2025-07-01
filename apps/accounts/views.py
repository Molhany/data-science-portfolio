from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import CustomUser, UserProfile, ProjectPurchase, ProjectRequest
from .forms import CustomUserCreationForm, UserProfileForm, ProjectRequestForm


class RegisterView(CreateView):
    """User registration view"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Create user profile
        UserProfile.objects.create(user=self.object)
        messages.success(self.request, 'Account created successfully! Please log in.')
        return response


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'portfolio:home')
            messages.success(request, f'Welcome back, {user.get_full_name()}!')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('portfolio:home')


@login_required
def profile_view(request):
    """User profile view"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'profile': profile,
        'purchases': ProjectPurchase.objects.filter(user=request.user),
        'project_requests': ProjectRequest.objects.filter(user=request.user),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def request_project_view(request):
    """Project request view"""
    if request.method == 'POST':
        form = ProjectRequestForm(request.POST)
        if form.is_valid():
            project_request = form.save(commit=False)
            project_request.user = request.user
            project_request.save()
            messages.success(request, 'Project request submitted successfully! We will review it and get back to you.')
            return redirect('accounts:profile')
    else:
        form = ProjectRequestForm()
    
    return render(request, 'accounts/request_project.html', {'form': form})


@csrf_exempt
@login_required
def purchase_project(request):
    """Handle project purchase"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_slug = data.get('project_slug')
            payment_method = data.get('payment_method')
            payment_phone = data.get('payment_phone', '')
            payment_email = data.get('payment_email', '')
            
            # Get project details (you might want to fetch from Project model)
            project_title = data.get('project_title', 'Unknown Project')
            amount = data.get('amount', 50.00)  # Default price
            
            # Create purchase record
            purchase = ProjectPurchase.objects.create(
                user=request.user,
                project_slug=project_slug,
                project_title=project_title,
                amount=amount,
                payment_method=payment_method,
                payment_phone=payment_phone,
                payment_email=payment_email,
                payment_status='processing'
            )
            
            # Here you would integrate with actual payment gateways
            # For now, we'll simulate successful payment
            if payment_method in ['ecocash', 'onemoney', 'innbucks']:
                # Simulate mobile payment
                purchase.payment_reference = f"MP{purchase.id:06d}"
                purchase.payment_status = 'completed'
                purchase.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Payment processed successfully! You now have access to the project.',
                    'reference': purchase.payment_reference
                })
            else:
                # For international payments, you'd redirect to Stripe/PayPal
                return JsonResponse({
                    'success': True,
                    'message': 'Redirecting to payment gateway...',
                    'redirect_url': f'/accounts/payment/{purchase.id}/'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Payment failed: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
def payment_gateway(request, purchase_id):
    """Payment gateway view for international payments"""
    try:
        purchase = ProjectPurchase.objects.get(id=purchase_id, user=request.user)
        
        # Here you would integrate with Stripe or PayPal
        # For demo purposes, we'll show a success page
        purchase.payment_status = 'completed'
        purchase.payment_reference = f"INTL{purchase.id:06d}"
        purchase.save()
        
        messages.success(request, 'Payment completed successfully!')
        return redirect('accounts:profile')
        
    except ProjectPurchase.DoesNotExist:
        messages.error(request, 'Purchase not found.')
        return redirect('accounts:profile')


@login_required
def purchased_projects(request):
    """View purchased projects"""
    purchases = ProjectPurchase.objects.filter(
        user=request.user,
        payment_status='completed'
    )
    return render(request, 'accounts/purchased_projects.html', {'purchases': purchases})


class PrivacySettingsView(LoginRequiredMixin, TemplateView):
    """Privacy settings view"""
    template_name = 'accounts/privacy_settings.html'
    
    def post(self, request, *args, **kwargs):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        # Update privacy settings
        profile.show_email = request.POST.get('show_email') == 'on'
        profile.show_phone = request.POST.get('show_phone') == 'on'
        profile.show_address = request.POST.get('show_address') == 'on'
        profile.save()
        
        # Update user preferences
        request.user.newsletter_subscription = request.POST.get('newsletter_subscription') == 'on'
        request.user.email_notifications = request.POST.get('email_notifications') == 'on'
        request.user.save()
        
        messages.success(request, 'Privacy settings updated successfully!')
        return redirect('accounts:privacy_settings')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = self.request.user.profile
        except UserProfile.DoesNotExist:
            context['profile'] = UserProfile.objects.create(user=self.request.user)
        return context
