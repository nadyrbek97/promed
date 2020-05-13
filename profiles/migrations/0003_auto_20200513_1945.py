# Generated by Django 3.0.3 on 2020-05-13 19:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20200513_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Initial Password'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='profile_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='Profile'),
        ),
    ]
