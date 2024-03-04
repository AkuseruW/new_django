from django.contrib import admin
from api.models import (CustomUser, Profile, Photo, Gender, Relationship, UserPreference)

# List of models to register
models_to_register = [CustomUser, Profile, Photo, Gender, Relationship, UserPreference]

# Register models
for model in models_to_register:
    admin.site.register(model)