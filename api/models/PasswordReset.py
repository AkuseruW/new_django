from django.db import models


class PasswordReset(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("CustomUser", on_delete=models.CASCADE)
    token = models.CharField(max_length=155, null=False)
    expires_at = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "api_password_resets"
