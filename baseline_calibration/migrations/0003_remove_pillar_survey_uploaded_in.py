# Generated by Django 3.1 on 2022-08-01 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseline_calibration', '0002_pillar_survey_uploaded_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pillar_survey',
            name='uploaded_in',
        ),
    ]
