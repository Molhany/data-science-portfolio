from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Project, ProjectCategory, Technology


class ProjectListView(ListView):
    """List all projects with filtering and search"""
    model = Project
    template_name = 'projects/list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.filter(is_published=True)
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by technology
        tech_slug = self.request.GET.get('tech')
        if tech_slug:
            queryset = queryset.filter(technologies__slug=tech_slug)
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                title__icontains=search_query
            ) | queryset.filter(
                description__icontains=search_query
            )
        
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProjectCategory.objects.all()
        context['technologies'] = Technology.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_tech'] = self.request.GET.get('tech')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProjectDetailView(DetailView):
    """Detailed view of a single project"""
    model = Project
    template_name = 'projects/detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get related projects
        project = self.get_object()
        related_projects = Project.objects.filter(
            category=project.category,
            is_published=True
        ).exclude(id=project.id)[:3]
        
        context['related_projects'] = related_projects
        return context


class ProjectCategoryView(ListView):
    """List projects by category"""
    model = Project
    template_name = 'projects/category.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(ProjectCategory, slug=self.kwargs['category_slug'])
        return Project.objects.filter(
            category=self.category,
            is_published=True
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = ProjectCategory.objects.all()
        return context
