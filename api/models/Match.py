from django.db import models

class Match (models.Model):
    id = models.AutoField(primary_key=True)
    user_a = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='matches_as_user_a')
    user_b = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='matches_as_user_b')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)