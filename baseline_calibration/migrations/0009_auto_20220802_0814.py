# Generated by Django 3.2.12 on 2022-08-02 00:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseline_calibration', '0008_delete_calibrated_baseline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pillar_survey',
            name='degrees_of_freedom',
            field=models.IntegerField(blank=True, help_text='Degrees of freedom of calibration', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)]),
        ),
        migrations.AlterField(
            model_name='pillar_survey',
            name='variance',
            field=models.FloatField(blank=True, help_text='Variance of least squares adjustment of the calibration', null=True),
        ),
        migrations.AlterField(
            model_name='pillar_survey',
            name='zero_point_correction',
            field=models.FloatField(blank=True, help_text='If: Instrument Correction (m) = 1.00000013.L + 0.0003, Zero Point Correction = 0.0003m', null=True, validators=[django.core.validators.MinValueValidator(-0.1), django.core.validators.MaxValueValidator(0.1)]),
        ),
        migrations.AlterField(
            model_name='pillar_survey',
            name='zpc_uncertainty',
            field=models.FloatField(blank=True, help_text='Uncertainty of the zero point correction (m) at 95% Confidence Level', null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(0.1)], verbose_name='zero point correction uncertainty'),
        ),
    ]
