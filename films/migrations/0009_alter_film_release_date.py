# Generated by Django 5.1.5 on 2025-01-21 19:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0008_alter_film_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='release_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
