from django.db import models

class Gender (models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=155, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# class InterestedInGender (models.Model):
#     id = models.AutoField(primary_key=True)
#     gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
#     user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

#     class Meta:
#         db_table = 'api_interested_in_gender'
#         unique_together = ('gender', 'user')
        