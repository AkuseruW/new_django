from django.db import models

class Role (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=155, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    