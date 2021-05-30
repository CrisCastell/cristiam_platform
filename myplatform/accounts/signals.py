  
from django.db.models.signals import post_save, pre_save
from notes.models import Category
from .models import Account
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


def create_first_category(sender, instance, created, **kwargs):
    if created:

        Category.objects.create(author=instance, title="Uncategorized")
    
post_save.connect(create_first_category, sender=Account)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)