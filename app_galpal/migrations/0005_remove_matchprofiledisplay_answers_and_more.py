# Generated by Django 5.0.6 on 2024-06-18 14:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_galpal', '0004_alter_matchprofiledisplay_answers_friendslist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchprofiledisplay',
            name='answers',
        ),
        migrations.AddField(
            model_name='matchprofileanswers',
            name='profile_display',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answers', to='app_galpal.matchprofiledisplay'),
        ),
    ]
