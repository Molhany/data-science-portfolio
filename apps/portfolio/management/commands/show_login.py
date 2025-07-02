from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Display default login credentials for admin access'

    def handle(self, *args, **options):
        User = get_user_model()
        
        self.stdout.write("🔑 ADMIN LOGIN CREDENTIALS")
        self.stdout.write("=" * 50)
        
        # Check if default superuser exists
        try:
            user = User.objects.get(username='adrian_molhany')
            self.stdout.write(
                self.style.SUCCESS("✅ Default superuser found!")
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR("❌ Default superuser not found!")
            )
            self.stdout.write("Run: python manage.py create_admin")
            return
        
        # Display login information
        self.stdout.write("")
        self.stdout.write("🌐 Admin Panel URL:")
        self.stdout.write("https://data-science-portfolio-0738.onrender.com/admin/")
        self.stdout.write("")
        
        self.stdout.write("👤 Login Credentials:")
        self.stdout.write(f"Username: adrian_molhany")
        self.stdout.write(f"Password: Portfolio2024!")
        self.stdout.write(f"Email: {user.email}")
        self.stdout.write("")
        
        self.stdout.write(
            self.style.WARNING("⚠️ SECURITY: Change password after first login!")
        )
        self.stdout.write("")
        
        # Show user status
        self.stdout.write("📊 User Status:")
        self.stdout.write(f"Is Active: {user.is_active}")
        self.stdout.write(f"Is Superuser: {user.is_superuser}")
        self.stdout.write(f"Is Staff: {user.is_staff}")
        self.stdout.write(f"Date Joined: {user.date_joined}")
        self.stdout.write(f"Last Login: {user.last_login or 'Never'}")
        
        # Show all superusers
        all_superusers = User.objects.filter(is_superuser=True)
        if all_superusers.count() > 1:
            self.stdout.write("")
            self.stdout.write("👥 All Superusers:")
            for su in all_superusers:
                self.stdout.write(f"  - {su.username} ({su.email})")
        
        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS("🚀 Ready to login and manage your portfolio!")
        )
