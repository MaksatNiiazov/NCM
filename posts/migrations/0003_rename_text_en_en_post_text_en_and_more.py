# Generated by Django 5.0 on 2024-01-24 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='text_en_EN',
            new_name='text_en',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text_ky_KG',
            new_name='text_kg',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text_ru_RU',
            new_name='text_ru',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='title_en_EN',
            new_name='title_en',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='title_ky_KG',
            new_name='title_kg',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='title_ru_RU',
            new_name='title_ru',
        ),
    ]