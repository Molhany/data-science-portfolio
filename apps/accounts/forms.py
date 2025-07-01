from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, ProjectRequest


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Email Address'
        })
    )
    phone_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': '+263771234567'
        })
    )
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Your Address',
            'rows': 3
        })
    )
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'City'
        })
    )
    country = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Country'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'country', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
            'placeholder': 'Confirm Password'
        })


class UserProfileForm(forms.ModelForm):
    """User profile update form"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'country', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'rows': 4
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
        }


class ProjectRequestForm(forms.ModelForm):
    """Project request form"""
    class Meta:
        model = ProjectRequest
        fields = ['title', 'description', 'requirements', 'budget_range', 'timeline', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'placeholder': 'Project Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'placeholder': 'Describe your project in detail...',
                'rows': 5
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'placeholder': 'List your specific requirements...',
                'rows': 4
            }),
            'budget_range': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'placeholder': 'e.g., $500 - $1000'
            }),
            'timeline': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500',
                'placeholder': 'e.g., 2-4 weeks'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-white dark:bg-dark-800 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500'
            }),
        }
