# Generated by Django 5.1.5 on 2025-01-20 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_leeftijd'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdata',
            name='profiel_foto',
            field=models.ImageField(default='default_profile.png', upload_to=''),
        ),
    ]
