# Generated by Django 5.0.6 on 2024-06-13 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0026_rename_mi_campo_customuser_birthdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='birthdate',
        ),
    ]
