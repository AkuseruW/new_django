from django.db import models


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    provider_id = models.CharField(max_length=155, null=False)
    provider = models.CharField(max_length=155, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
