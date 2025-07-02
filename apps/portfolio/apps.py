from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.dispatch import receiver


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.portfolio'
    verbose_name = 'Portfolio'

    def ready(self):
        # Import signals to ensure they're registered
        pass


@receiver(post_migrate)
def create_default_superuser(sender, **kwargs):
    """
    Create default superuser after migrations.
    This ensures there's always a superuser available for admin access.
    """
    if sender.name == 'apps.portfolio':
        from django.contrib.auth import get_user_model

        User = get_user_model()

        # Default superuser credentials
        username = 'adrian_molhany'
        email = 'adrian.molhany@gmail.com'
        password = 'Portfolio2024!'

        # Only create if no superuser exists
        if not User.objects.filter(is_superuser=True).exists():
            try:
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name='Adrian',
                    last_name='Molhany'
                )
                print(f"✅ Default superuser '{username}' created successfully!")
                print(f"📧 Email: {email}")
                print(f"🔑 Password: {password}")
                print("⚠️ Change password after first login!")
            except Exception as e:
                print(f"❌ Error creating default superuser: {e}")
        else:
            existing_superuser = User.objects.filter(is_superuser=True).first()
            print(f"✅ Superuser already exists: {existing_superuser.username}")
