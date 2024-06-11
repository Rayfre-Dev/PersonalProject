from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='ip_locator_app_user_groups',  # Avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='ip_locator_app_user_permissions',  # Avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class IPAddressLocation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    population = models.CharField(max_length=255, null=True, blank=True)
