"""
URL configuration for datasci_portfolio project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.portfolio.urls')),
    path('projects/', include('apps.projects.urls')),
    path('skills/', include('apps.skills.urls')),
    path('blog/', include('apps.blog.urls')),
    path('contact/', include('apps.contact.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('chat/', include('apps.chat.urls')),
    path('legal/', include('apps.legal.urls')),
]

# Serve media files in development and production
# Note: In production, consider using cloud storage (AWS S3, Cloudinary) for better performance
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Data Science Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Welcome to Portfolio Administration"
