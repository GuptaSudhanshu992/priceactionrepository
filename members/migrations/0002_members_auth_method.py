# Generated by Django 5.1 on 2024-08-28 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='auth_method',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
