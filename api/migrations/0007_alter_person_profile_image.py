# Generated by Django 4.2.6 on 2023-12-13 10:08

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_person_favorite_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.file_path),
        ),
    ]