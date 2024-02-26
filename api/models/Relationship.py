from django.db import models

class Relationship (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=155, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InterestedInRelation (models.Model):
    id = models.AutoField(primary_key=True)
    relationship = models.ForeignKey('Relationship', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    class Meta:
        db_table = 'api_interested_in_relation'
        