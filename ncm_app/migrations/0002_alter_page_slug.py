# Generated by Django 5.0 on 2024-01-24 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ncm_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
