# Generated by Django 3.2 on 2021-05-04 15:38

from django.db import migrations, models
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo_id',
            field=models.CharField(default=home.models.my_uuid, max_length=16, unique=True),
        ),
        migrations.AlterField(
            model_name='user_comments',
            name='comment_id',
            field=models.CharField(default=home.models.my_uuid, max_length=16, unique=True),
        ),
    ]