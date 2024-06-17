# Generated by Django 5.0.6 on 2024-06-17 16:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_galpal', '0003_remove_profile_bio_remove_profile_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchprofiledisplay',
            name='answers',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_answers', to='app_galpal.matchprofileanswers'),
        ),
        migrations.CreateModel(
            name='FriendsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_friends', to='app_galpal.profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to='app_galpal.profile')),
            ],
        ),
    ]
