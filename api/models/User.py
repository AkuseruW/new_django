from uuid import uuid4

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.gis.db import models as geomodels
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

import api.utils.gets as g
from api.models import Match
from api.utils.CustomUserManager import CustomUserManager

from .Gender import Gender


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


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile", db_index=True
    )
    first_name = models.CharField(max_length=155, null=False)
    last_name = models.CharField(max_length=155, null=False)
    description = models.TextField(max_length=500, null=True)
    instagram = models.TextField(max_length=15, null=True)
    birthdate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.birthdate:
            today = timezone.now().date()
            age = (
                today.year
                - self.birthdate.year
                - (
                    (today.month, today.day)
                    < (self.birthdate.month, self.birthdate.day)
                )
            )

            if age < 18:
                raise ValidationError("The user must be at least 18 years old.")

    def user_age(self):
        if self.birthdate:
            today = timezone.now().date()
            age = (
                today.year
                - self.birthdate.year
                - (
                    (today.month, today.day)
                    < (self.birthdate.month, self.birthdate.day)
                )
            )
            return age


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    profile = models.ForeignKey(Profile, default=None, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, **kwargs):
        self.image.delete(save=False)
        super().delete()


class UserPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    interested_in = models.ForeignKey(
        "Gender",
        on_delete=models.CASCADE,
        related_name="interested_in",
        null=True,
        blank=True,
    )
    relationship = models.ForeignKey(
        "Relationship",
        on_delete=models.CASCADE,
        related_name="relationship",
        null=True,
        blank=True,
    )
    location_max_distance = models.FloatField(null=True, blank=True)
    age_min = models.IntegerField(null=True, blank=True)
    age_max = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
