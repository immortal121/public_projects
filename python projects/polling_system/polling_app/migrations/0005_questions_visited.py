# Generated by Django 4.1 on 2022-08-30 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling_app', '0004_alter_questions_option1_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='visited',
            field=models.BooleanField(default=False),
        ),
    ]