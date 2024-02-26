from django.db import models

class NotificationContext (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=155, null=False)
    translations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_notification_contexts'

class Notification (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    context = models.ForeignKey(NotificationContext, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
