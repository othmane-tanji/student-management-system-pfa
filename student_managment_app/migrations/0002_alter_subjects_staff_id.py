# Generated by Django 5.2 on 2025-04-09 11:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_managment_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjects',
            name='staff_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
