# Generated by Django 4.1 on 2022-08-29 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling_app', '0003_questions_option1_questions_option1_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='option1_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option2_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option3_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='questions',
            name='option4_count',
            field=models.IntegerField(default=0),
        ),
    ]
