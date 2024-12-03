# Generated by Django 4.2.11 on 2024-12-03 16:30

import django.core.validators
from django.db import migrations, models
import iam.models


class Migration(migrations.Migration):

    dependencies = [
        ('iam', '0002_alter_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=iam.models.User.get_user_picture_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])]),
        ),
    ]