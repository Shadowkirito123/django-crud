# Generated by Django 5.0.6 on 2024-06-23 17:38

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0034_alter_task_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='imagen',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=None),
        ),
    ]
