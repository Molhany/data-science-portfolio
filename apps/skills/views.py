from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from .models import Skill, SkillCategory


class SkillsView(TemplateView):
    """Skills overview page with interactive charts"""
    template_name = 'skills/list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get skills organized by category
        skill_categories = SkillCategory.objects.prefetch_related('skills').all()
        
        # Get featured skills
        featured_skills = Skill.objects.filter(is_featured=True)
        
        context.update({
            'skill_categories': skill_categories,
            'featured_skills': featured_skills,
        })
        
        return context


def skills_data_api(request):
    """API endpoint for skills data (for charts)"""
    
    # Skills by category for charts
    categories_data = []
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    
    for category in skill_categories:
        category_data = {
            'name': category.name,
            'color': category.color,
            'skills': []
        }
        
        for skill in category.skills.all():
            category_data['skills'].append({
                'name': skill.name,
                'proficiency': skill.proficiency_level,
                'proficiency_percentage': skill.get_proficiency_percentage(),
                'years_experience': float(skill.years_of_experience) if skill.years_of_experience else 0,
                'is_certified': skill.is_certified,
                'color': skill.color or category.color
            })
        
        categories_data.append(category_data)
    
    # Skills progression data (mock data for now)
    progression_data = [
        {'month': '2023-01', 'python': 3, 'machine_learning': 2, 'data_analysis': 3},
        {'month': '2023-06', 'python': 4, 'machine_learning': 3, 'data_analysis': 4},
        {'month': '2024-01', 'python': 4, 'machine_learning': 4, 'data_analysis': 4},
        {'month': '2024-06', 'python': 5, 'machine_learning': 4, 'data_analysis': 5},
    ]
    
    # Top skills summary
    top_skills = []
    for skill in Skill.objects.filter(is_featured=True).order_by('-proficiency_level')[:8]:
        top_skills.append({
            'name': skill.name,
            'proficiency': skill.proficiency_level,
            'category': skill.category.name,
            'color': skill.color or skill.category.color
        })
    
    data = {
        'categories': categories_data,
        'progression': progression_data,
        'top_skills': top_skills,
        'total_skills': Skill.objects.count(),
        'certified_skills': Skill.objects.filter(is_certified=True).count(),
    }
    
    return JsonResponse(data)
