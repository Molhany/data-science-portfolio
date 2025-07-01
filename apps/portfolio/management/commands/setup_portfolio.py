from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.portfolio.models import Profile, Education, Experience, Achievement
from apps.projects.models import ProjectCategory, Technology, Project
from apps.skills.models import SkillCategory, Skill
from apps.blog.models import BlogCategory, BlogPost


class Command(BaseCommand):
    help = 'Set up initial portfolio data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up portfolio data...'))
        
        # Create Profile
        profile, created = Profile.objects.get_or_create(
            name='Data Science Student',
            defaults={
                'title': 'Bachelor of Commerce Honours in Data Science & Informatics',
                'bio': 'Passionate about transforming data into actionable insights and building innovative solutions that drive business value. Currently pursuing BCom Honours in Data Science & Informatics with a focus on machine learning, data analysis, and business intelligence.',

                'location': 'Zimbabwe',
                'linkedin_url': 'https://www.linkedin.com/in/adrian-munashe-38838136a?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app',
                'meta_description': 'Data Science student portfolio showcasing projects, skills, and academic journey',
                'meta_keywords': 'data science, machine learning, python, portfolio, student',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Profile created'))
        
        # Create Education
        education, created = Education.objects.get_or_create(
            institution='University Name',
            degree='bachelor',
            field_of_study='Commerce Honours in Data Science & Informatics',
            defaults={
                'start_date': '2022-01-01',
                'is_current': True,
                'description': 'Comprehensive program covering statistical analysis, machine learning, data visualization, and business intelligence.',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Education record created'))
        
        # Create Skill Categories
        skill_categories_data = [
            {'name': 'Programming Languages', 'icon': 'fas fa-code', 'color': '#3b82f6'},
            {'name': 'Data Science & ML', 'icon': 'fas fa-brain', 'color': '#8b5cf6'},
            {'name': 'Data Visualization', 'icon': 'fas fa-chart-bar', 'color': '#10b981'},
            {'name': 'Databases', 'icon': 'fas fa-database', 'color': '#f59e0b'},
            {'name': 'Tools & Frameworks', 'icon': 'fas fa-tools', 'color': '#ef4444'},
        ]
        
        for cat_data in skill_categories_data:
            category, created = SkillCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Skill category "{cat_data["name"]}" created')
        
        # Create Skills
        skills_data = [
            {'name': 'Python', 'category': 'Programming Languages', 'proficiency': 4, 'years': 2.0},
            {'name': 'R', 'category': 'Programming Languages', 'proficiency': 3, 'years': 1.5},
            {'name': 'SQL', 'category': 'Databases', 'proficiency': 4, 'years': 2.0},
            {'name': 'Machine Learning', 'category': 'Data Science & ML', 'proficiency': 3, 'years': 1.0},
            {'name': 'Data Analysis', 'category': 'Data Science & ML', 'proficiency': 4, 'years': 2.0},
            {'name': 'Pandas', 'category': 'Tools & Frameworks', 'proficiency': 4, 'years': 2.0},
            {'name': 'Matplotlib', 'category': 'Data Visualization', 'proficiency': 3, 'years': 1.5},
            {'name': 'Seaborn', 'category': 'Data Visualization', 'proficiency': 3, 'years': 1.5},
        ]
        
        for skill_data in skills_data:
            try:
                category = SkillCategory.objects.get(name=skill_data['category'])
                skill, created = Skill.objects.get_or_create(
                    name=skill_data['name'],
                    category=category,
                    defaults={
                        'proficiency_level': skill_data['proficiency'],
                        'years_of_experience': skill_data['years'],
                        'is_featured': True,
                    }
                )
                if created:
                    self.stdout.write(f'✓ Skill "{skill_data["name"]}" created')
            except SkillCategory.DoesNotExist:
                continue
        
        # Create Project Categories
        project_categories_data = [
            {'name': 'Machine Learning', 'color': '#8b5cf6', 'icon': 'fas fa-robot'},
            {'name': 'Data Analysis', 'color': '#10b981', 'icon': 'fas fa-chart-line'},
            {'name': 'Web Development', 'color': '#3b82f6', 'icon': 'fas fa-globe'},
            {'name': 'Data Visualization', 'color': '#f59e0b', 'icon': 'fas fa-chart-bar'},
        ]
        
        for cat_data in project_categories_data:
            category, created = ProjectCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Project category "{cat_data["name"]}" created')
        
        # Create Technologies
        technologies_data = [
            {'name': 'Python', 'color': '#3776ab'},
            {'name': 'Django', 'color': '#092e20'},
            {'name': 'Pandas', 'color': '#150458'},
            {'name': 'Scikit-learn', 'color': '#f7931e'},
            {'name': 'Matplotlib', 'color': '#11557c'},
            {'name': 'Jupyter', 'color': '#f37626'},
        ]
        
        for tech_data in technologies_data:
            tech, created = Technology.objects.get_or_create(
                name=tech_data['name'],
                defaults=tech_data
            )
            if created:
                self.stdout.write(f'✓ Technology "{tech_data["name"]}" created')
        
        # Create Blog Categories
        blog_categories_data = [
            {'name': 'Data Science', 'color': '#8b5cf6'},
            {'name': 'Machine Learning', 'color': '#3b82f6'},
            {'name': 'Tutorials', 'color': '#10b981'},
            {'name': 'Career', 'color': '#f59e0b'},
        ]
        
        for cat_data in blog_categories_data:
            category, created = BlogCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'✓ Blog category "{cat_data["name"]}" created')
        
        self.stdout.write(
            self.style.SUCCESS('Portfolio setup completed successfully!')
        )
        self.stdout.write(
            self.style.WARNING('Remember to:')
        )
        self.stdout.write('• Update profile information in Django Admin')
        self.stdout.write('• Add your projects and blog posts')
        self.stdout.write('• Upload profile image and resume')
        self.stdout.write('• Configure email settings for contact forms')
