from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.account.models import UserProfile,Wallet
from django.contrib.auth import get_user_model
User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()


@receiver(post_save, sender=User)
def create_user_predit(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
    else:
        instance.wallet.save()
