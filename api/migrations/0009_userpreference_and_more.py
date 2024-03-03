# Generated by Django 5.0.2 on 2024-03-03 14:09

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_customuser_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('location_min_distance', models.FloatField(blank=True, null=True)),
                ('location_max_distance', models.FloatField(blank=True, null=True)),
                ('age_min', models.IntegerField(blank=True, null=True)),
                ('age_max', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('interested_in', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interested_in', to='api.gender')),
                ('relationship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationship', to='api.relationship')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='interestedingender',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='interestedingender',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='interestedingender',
            name='user',
        ),
        migrations.AlterUniqueTogether(
            name='interestedinrelation',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='interestedinrelation',
            name='relationship',
        ),
        migrations.RemoveField(
            model_name='interestedinrelation',
            name='user',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.DeleteModel(
            name='InterestedInGender',
        ),
        migrations.DeleteModel(
            name='InterestedInRelation',
        ),
    ]
