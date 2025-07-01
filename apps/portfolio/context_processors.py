from .models import Profile

def profile_context(request):
    """
    Context processor to make profile data available globally across all templates
    """
    try:
        profile = Profile.objects.first()
        return {
            'profile': profile
        }
    except Profile.DoesNotExist:
        return {
            'profile': None
        }
