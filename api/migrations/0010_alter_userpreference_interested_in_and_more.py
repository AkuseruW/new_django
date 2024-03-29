# Generated by Django 5.0.2 on 2024-03-03 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_userpreference_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='interested_in',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interested_in', to='api.gender'),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='relationship',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relationship', to='api.relationship'),
        ),
    ]
