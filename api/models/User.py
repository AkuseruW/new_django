from uuid import uuid4

from django.db import models
from django.contrib.gis.db import models as geomodels
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q

import api.utils.gets as g
from api.models import Match
from .Gender import Gender


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or not password:
            raise ValueError("Email and password are required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True)
    location = geomodels.PointField(null=True, blank=True, srid=4326)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    blocked = models.ManyToManyField(
        "self", symmetrical=False, related_name="blocked_by", blank=True
    )

    likes = models.ManyToManyField(
        "self", symmetrical=False, related_name="liked_by", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        db_table = "api_user"

    def __str__(self):
        return self.email
    
    def block_profile(self, blocked_profile):
        self.likes.remove(blocked_profile)
        blocked_profile.likes.remove(self)

        match_qs = Match.objects.filter(
            Q(profile1=self, profile2=blocked_profile)
            | Q(profile1=blocked_profile, profile2=self)
        )

        if match_qs.exists():
            match_qs.delete()

        conversation = g.get_conversation_between(self, blocked_profile)
        if conversation:
            conversation.delete()

        self.blocked_profiles.add(blocked_profile)

class Profile (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=155, null=False)
    last_name = models.CharField(max_length=155, null=False)
    description = models.TextField(max_length=500, null=True)
    instagram = models.TextField(max_length=15, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.email + ' - ' + self.first_name + ' ' + self.last_name


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self):
        self.image.delete(save=False)
        super().delete()