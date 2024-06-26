# Generated by Django 5.0.6 on 2024-06-23 17:43

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0035_alter_task_description_alter_task_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=None),
        ),
        migrations.AlterField(
            model_name='task',
            name='imagen',
            field=models.ImageField(default=None, upload_to='static/'),
        ),
    ]
