# Generated by Django 3.1 on 2022-08-01 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseline_calibration', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pillar_survey',
            name='uploaded_in',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]