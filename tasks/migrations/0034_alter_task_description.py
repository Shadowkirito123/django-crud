# Generated by Django 5.0.6 on 2024-06-23 17:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0033_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]