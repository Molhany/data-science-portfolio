from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Profile, Education, Experience, Achievement
from apps.projects.models import Project
from apps.skills.models import Skill, SkillCategory
from apps.blog.models import BlogPost


class HomeView(TemplateView):
    """Main homepage view with portfolio overview"""
    template_name = 'portfolio/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get profile information
        try:
            profile = Profile.objects.filter(is_active=True).first()
        except Profile.DoesNotExist:
            profile = None
            
        # Get recent projects
        recent_projects = Project.objects.filter(is_featured=True)[:3]
        
        # Get skills by category
        skill_categories = SkillCategory.objects.prefetch_related('skills').all()
        
        # Get recent blog posts
        recent_posts = BlogPost.objects.filter(is_published=True)[:3]
        
        # Get education and experience
        education = Education.objects.all()[:2]
        experience = Experience.objects.all()[:2]
        achievements = Achievement.objects.all()[:3]
        
        context.update({
            'profile': profile,
            'recent_projects': recent_projects,
            'skill_categories': skill_categories,
            'recent_posts': recent_posts,
            'education': education,
            'experience': experience,
            'achievements': achievements,
        })
        
        return context


class AboutView(TemplateView):
    """Detailed about page"""
    template_name = 'portfolio/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            profile = Profile.objects.filter(is_active=True).first()
        except Profile.DoesNotExist:
            profile = None
            
        education = Education.objects.all()
        experience = Experience.objects.all()
        achievements = Achievement.objects.all()
        
        context.update({
            'profile': profile,
            'education': education,
            'experience': experience,
            'achievements': achievements,
        })
        
        return context


class ResumeView(TemplateView):
    """Resume/CV page"""
    template_name = 'portfolio/resume.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            profile = Profile.objects.filter(is_active=True).first()
        except Profile.DoesNotExist:
            profile = None
            
        education = Education.objects.all()
        experience = Experience.objects.all()
        achievements = Achievement.objects.all()
        skills = Skill.objects.filter(is_featured=True)
        
        context.update({
            'profile': profile,
            'education': education,
            'experience': experience,
            'achievements': achievements,
            'skills': skills,
        })
        
        return context


def portfolio_data_api(request):
    """API endpoint for portfolio data (for charts and analytics)"""
    try:
        profile = Profile.objects.filter(is_active=True).first()
    except Profile.DoesNotExist:
        profile = None
    
    # Skills data for charts
    skills_data = []
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    for category in skill_categories:
        category_data = {
            'category': category.name,
            'skills': []
        }
        for skill in category.skills.all():
            category_data['skills'].append({
                'name': skill.name,
                'proficiency': skill.proficiency_level
            })
        skills_data.append(category_data)
    
    # Projects data
    projects_data = {
        'total': Project.objects.count(),
        'featured': Project.objects.filter(is_featured=True).count(),
        'by_category': []
    }
    
    # Experience timeline data
    experience_data = []
    for exp in Experience.objects.all():
        experience_data.append({
            'company': exp.company,
            'position': exp.position,
            'start_date': exp.start_date.isoformat(),
            'end_date': exp.end_date.isoformat() if exp.end_date else None,
            'is_current': exp.is_current
        })
    
    data = {
        'profile': {
            'name': profile.name if profile else '',
            'title': profile.title if profile else '',
        },
        'skills': skills_data,
        'projects': projects_data,
        'experience': experience_data,
    }
    
    return JsonResponse(data)
