# Generated by Django 3.2.1 on 2021-05-08 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_photo_uploader'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='view_count',
            field=models.BigIntegerField(default=0),
        ),
    ]
