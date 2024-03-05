from django.db import models


class ReportContext(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=155, null=False)
    translations = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Report(models.Model):
    id = models.AutoField(primary_key=True)
    reporter_user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="reports_as_reporter"
    )
    reported_user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="reports_as_reported"
    )
    context = models.ForeignKey(ReportContext, on_delete=models.CASCADE)
    description = models.CharField(max_length=155, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
