from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta
from .models import PageView, PortfolioMetrics, ContentInteraction, ProjectAnalytics
from apps.projects.models import Project
from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage


class AnalyticsView(TemplateView):
    """Analytics dashboard view"""
    template_name = 'analytics/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get recent metrics
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Basic stats
        context.update({
            'total_page_views': PageView.objects.count(),
            'unique_visitors': PageView.objects.filter(is_unique_visitor=True).count(),
            'total_projects': Project.objects.filter(is_published=True).count(),
            'total_blog_posts': BlogPost.objects.filter(is_published=True).count(),
            'total_messages': ContactMessage.objects.count(),
            'recent_messages': ContactMessage.objects.filter(created_at__gte=week_ago).count(),
        })
        
        return context


def portfolio_stats_api(request):
    """API endpoint for portfolio statistics"""
    
    # Date ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Page views over time (last 30 days)
    page_views_data = []
    for i in range(30):
        date = today - timedelta(days=i)
        views = PageView.objects.filter(created_at__date=date).count()
        page_views_data.append({
            'date': date.isoformat(),
            'views': views
        })
    
    # Device breakdown
    device_stats = PageView.objects.values('device_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Top pages
    top_pages = PageView.objects.values('page_url', 'page_title').annotate(
        views=Count('id')
    ).order_by('-views')[:10]
    
    # Geographic data
    country_stats = PageView.objects.exclude(country='').values('country').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Project analytics
    project_stats = []
    for project in Project.objects.filter(is_published=True)[:5]:
        try:
            analytics = ProjectAnalytics.objects.get(project_slug=project.slug)
            project_stats.append({
                'title': project.title,
                'views': analytics.total_views,
                'github_clicks': analytics.github_clicks,
                'demo_clicks': analytics.demo_clicks
            })
        except ProjectAnalytics.DoesNotExist:
            project_stats.append({
                'title': project.title,
                'views': 0,
                'github_clicks': 0,
                'demo_clicks': 0
            })
    
    # Contact form submissions over time
    contact_data = []
    for i in range(7):
        date = today - timedelta(days=i)
        submissions = ContactMessage.objects.filter(created_at__date=date).count()
        contact_data.append({
            'date': date.isoformat(),
            'submissions': submissions
        })
    
    data = {
        'page_views_timeline': list(reversed(page_views_data)),
        'device_breakdown': list(device_stats),
        'top_pages': list(top_pages),
        'country_stats': list(country_stats),
        'project_analytics': project_stats,
        'contact_timeline': list(reversed(contact_data)),
        'summary': {
            'total_views': PageView.objects.count(),
            'unique_visitors': PageView.objects.filter(is_unique_visitor=True).count(),
            'avg_session_duration': PageView.objects.aggregate(
                avg_duration=Avg('time_on_page')
            )['avg_duration'] or 0,
            'bounce_rate': 0.35,  # Mock data - implement actual calculation
            'weekly_growth': 12.5,  # Mock data - implement actual calculation
        }
    }
    
    return JsonResponse(data)
