from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = 'Create a default superuser for Adrian Molhany portfolio'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='adrian_molhany')
        parser.add_argument('--email', type=str, default='adrian.molhany@gmail.com')
        parser.add_argument('--password', type=str, default='Portfolio2024!')
        parser.add_argument('--force', action='store_true', help='Force create even if superuser exists')

    def handle(self, *args, **options):
        User = get_user_model()

        username = options['username']
        email = options['email']
        password = options['password']
        force = options['force']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            if not force:
                existing_user = User.objects.get(username=username)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ User "{username}" already exists!')
                )
                self.stdout.write(f'Email: {existing_user.email}')
                self.stdout.write(f'Is superuser: {existing_user.is_superuser}')
                return
            else:
                # Delete existing user if force is True
                User.objects.filter(username=username).delete()
                self.stdout.write(f'🗑️ Deleted existing user "{username}"')

        # Check if any superuser exists (but still create our default one)
        existing_superusers = User.objects.filter(is_superuser=True)
        if existing_superusers.exists() and not force:
            self.stdout.write(
                self.style.WARNING(f'⚠️ Other superusers exist: {[u.username for u in existing_superusers]}')
            )
            self.stdout.write('Creating default superuser anyway...')

        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Adrian',
                last_name='Molhany'
            )

            self.stdout.write(
                self.style.SUCCESS(f'🎉 Default superuser "{username}" created successfully!')
            )
            self.stdout.write(f'📧 Email: {email}')
            self.stdout.write(f'🔑 Password: {password}')
            self.stdout.write(f'🌐 Admin URL: https://data-science-portfolio-0738.onrender.com/admin/')
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING('⚠️ SECURITY: Change this password after first login!')
            )
            self.stdout.write(
                self.style.SUCCESS('✅ You can now login and start uploading your portfolio content!')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {e}')
            )
