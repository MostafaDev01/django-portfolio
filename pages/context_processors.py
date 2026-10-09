from .models import Profile, SocialLinks

def portfolio_globals(request):
    """
    Exposes global portfolio context (profile and social links)
    across all templates (navbar, footer, details, archive).
    """
    return {
        "profile": Profile.objects.first(),
        "sociallinks": SocialLinks.objects.all(),
    }
