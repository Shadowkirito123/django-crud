# Generated by Django 5.0.6 on 2024-06-09 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_userprofile_country'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
