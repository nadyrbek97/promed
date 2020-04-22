# Generated by Django 3.0.3 on 2020-04-22 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Medical Center',
                'verbose_name_plural': 'Medical Centers',
            },
        ),
        migrations.CreateModel(
            name='ScheduleTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('is_weekend', models.BooleanField(default=False)),
                ('med_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_times', to='med_center.MedicalCenter')),
            ],
            options={
                'verbose_name': 'Schedule Time',
                'verbose_name_plural': 'Schedule Times',
            },
        ),
        migrations.CreateModel(
            name='MedCenterPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='med-center-photos/')),
                ('is_logo', models.BooleanField(default=False)),
                ('medical_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='med_center.MedicalCenter')),
            ],
            options={
                'verbose_name': 'Med-Center Photo',
                'verbose_name_plural': 'Med-Center Photos',
            },
        ),
    ]
