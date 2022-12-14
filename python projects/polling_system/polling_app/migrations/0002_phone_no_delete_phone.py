# Generated by Django 4.1 on 2022-08-29 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polling_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='phone_no',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ques_can_add', models.PositiveSmallIntegerField(default=5)),
                ('phoneno', models.CharField(blank=True, max_length=13)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='phone',
        ),
    ]
