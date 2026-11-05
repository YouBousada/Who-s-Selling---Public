from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile

@receiver(user_signed_up)
def create_user_profile_on_signup(sender, request, user, **kwargs):
    """
    Create a profile for a new user upon social signup.
    """
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        profile.is_new_user = True
        profile.save()