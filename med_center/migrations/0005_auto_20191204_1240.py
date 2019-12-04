# Generated by Django 3.0 on 2019-12-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med_center', '0004_scheduletime'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduletime',
            name='is_weekend',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='scheduletime',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='scheduletime',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
