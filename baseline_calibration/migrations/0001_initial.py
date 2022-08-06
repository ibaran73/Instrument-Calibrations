# Generated by Django 3.1 on 2022-08-01 07:31

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0006_calibration_report_notes'),
        ('calibrationsites', '0005_auto_20220616_1023'),
        ('instruments', '0007_auto_20220721_1101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accreditation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_from_date', models.DateField(help_text='The date the period of appointment commences.')),
                ('valid_to_date', models.DateField(help_text='The date the period of appointment finishes.')),
                ('LUM_constant', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50.0)])),
                ('LUM_ppm', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50.0)])),
                ('statement', models.TextField(help_text='eg. Accredited as a verifying authority for units of lenght according to ISO 17025:2012', verbose_name='Statement of accreditation')),
                ('certificate_upload', models.FileField(blank=True, null=True, upload_to='accreditation_certificates/', verbose_name='Accreditation Certificate')),
                ('accredited_company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.company')),
            ],
            options={
                'ordering': ['accredited_company', 'valid_to_date'],
            },
        ),
        migrations.CreateModel(
            name='Pillar_Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_date', models.DateField()),
                ('computation_date', models.DateField()),
                ('observer', models.CharField(blank=True, max_length=25, null=True)),
                ('weather', models.CharField(choices=[('Sunny/Clear', 'Sunny/Clear'), ('Partially cloudy', 'Partially cloudy'), ('Cloudy', 'Cloudy'), ('Overcast', 'Overcast'), ('Drizzle', 'Drizzle'), ('Raining', 'Raining'), ('Stormy', 'Stormy')], help_text='Weather conditions', max_length=25)),
                ('job_number', models.CharField(help_text='Job reference eg., JN 20212216', max_length=25)),
                ('mets_applied', models.BooleanField(default=True, help_text='Meterological corrections have been applied in the EDM instrument.', verbose_name='Atmospheric corrections applied')),
                ('edmi_calib_applied', models.BooleanField(default=False, help_text='The EDMI calibration correction has been applied prior to data import.', verbose_name='EDMI calibration corrections applied')),
                ('staff_calib_applied', models.BooleanField(default=True, help_text='The staff calibration correction has been applied prior to data import.', verbose_name='staff calibration corrections applied')),
                ('thermo_calib_applied', models.BooleanField(default=True, help_text='The thermometer calibration correction has been applied prior to data import.', verbose_name='thermometer calibration corrections applied')),
                ('baro_calib_applied', models.BooleanField(default=True, help_text='The barometer calibration correction has been applied prior to data import.', verbose_name='barometer calibration corrections applied')),
                ('hygro_calib_applied', models.BooleanField(default=True, help_text='The hygrometer correction has been applied prior to data import.', verbose_name='Hygrometer calibration corrections applied')),
                ('psy_calib_applied', models.BooleanField(default=True, help_text='The psychrometer correction has been applied prior to data import.')),
                ('outlier_criterion', models.DecimalField(decimal_places=1, default=2, help_text='Number of standard deviations for outlier detection threashold.', max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('fieldnotes_upload', models.FileField(blank=True, null=True, upload_to='fieldnotes/', verbose_name='Scanned fieldnotes')),
                ('zero_point_correction', models.FloatField(blank=True, help_text='If: Instrument Correction (m) = 1.00000013.L + 0.0003, Zero Point Correction = 0.0003m', validators=[django.core.validators.MinValueValidator(-0.1), django.core.validators.MaxValueValidator(0.1)])),
                ('zpc_uncertainty', models.FloatField(blank=True, help_text='Uncertainty of the zero point correction (m) at 95% Confidence Level', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(0.1)], verbose_name='zero point correction uncertainty')),
                ('variance', models.FloatField(blank=True, help_text='Variance of least squares adjustment of the calibration')),
                ('degrees_of_freedom', models.IntegerField(blank=True, help_text='Degrees of freedom of calibration', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)])),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('accreditation', models.ForeignKey(help_text='corresponding certification survey.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='baseline_calibration.accreditation')),
                ('barometer', models.ForeignKey(help_text='Barometer used for survey', limit_choices_to={'mets_specs__mets_model__inst_type': 'baro'}, on_delete=django.db.models.deletion.PROTECT, related_name='field_barometer', to='instruments.mets_inst')),
                ('baseline', models.ForeignKey(help_text='Baseline under survey', on_delete=django.db.models.deletion.CASCADE, to='calibrationsites.calibrationsite')),
                ('edm', models.ForeignKey(help_text='EDM used for survey', on_delete=django.db.models.deletion.PROTECT, to='instruments.edm_inst')),
                ('hygrometer', models.ForeignKey(blank=True, help_text='Hygrometer, if used for survey', limit_choices_to={'mets_specs__mets_model__inst_type': 'hygro'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='field_hygrometer', to='instruments.mets_inst')),
                ('level', models.ForeignKey(help_text='Digital level used for survey', on_delete=django.db.models.deletion.PROTECT, to='instruments.digitallevel')),
                ('prism', models.ForeignKey(help_text='Prism used for survey', on_delete=django.db.models.deletion.PROTECT, to='instruments.prism_inst')),
                ('psychrometer', models.ForeignKey(blank=True, help_text='Psychrometer, if used for survey', limit_choices_to={'mets_specs__mets_model__inst_type': 'psy'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='field_psychrometer', to='instruments.mets_inst')),
                ('staff', models.ForeignKey(help_text='barcoded staff used for survey', on_delete=django.db.models.deletion.PROTECT, to='instruments.staff')),
                ('thermometer', models.ForeignKey(help_text='Thermometer used for survey', limit_choices_to={'mets_specs__mets_model__inst_type': 'thermo'}, on_delete=django.db.models.deletion.PROTECT, related_name='field_thermometer', to='instruments.mets_inst')),
            ],
            options={
                'ordering': ['baseline', 'survey_date'],
            },
        ),
        migrations.CreateModel(
            name='Uncertainty_Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='e.g., 2021 baseline calibration', max_length=30)),
                ('std_dev_of_zero_adjustment', models.DecimalField(decimal_places=4, help_text='Standard deviation applied to set of observations when all measured distances in set of observations are the same. (m)', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(0.01)])),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='accounts.company')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Uncertainty_Budget_Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(choices=[('01', 'EDM scale factor'), ('02', 'EDMI measurement'), ('03', 'EDM zero offset'), ('04', 'Temperature'), ('05', 'Pressure'), ('06', 'Humidity'), ('07', 'LS fit unc fixed term'), ('08', 'LS fit unc proportional term'), ('09', 'Centring'), ('10', 'Heights'), ('11', 'Offsets')], help_text='Grouping of uncertainty source', max_length=3)),
                ('description', models.CharField(max_length=256)),
                ('units', models.CharField(blank=True, choices=[('ppm', 'Parts per million (ppm)'), ('%', 'percent (%)'), ('1:x', 'Ratio (1:x)'), ('mm', 'millimetres (mm)'), ('m', 'metres (m)'), ('°C', 'Degrees Celcius (°C)'), ('hPa', 'hectopascals (hPa)'), ('mmHg', 'Millimetre of mercury (mmHg)')], help_text='Units of input quantity component', max_length=4, null=True)),
                ('ab_type', models.CharField(choices=[('A', 'A'), ('B', 'B')], default='B', help_text='Type A for a statistically derived component or Type B for any other derivation e.g. calibration report, manufacturers specification or an estimate based on experience.', max_length=1, verbose_name='type')),
                ('distribution', models.CharField(choices=[('N', 'Normal'), ('R', 'Rectangular')], default='N', help_text='A normal distribution represents most physical situations. Notable exceptions include rounding and resolution of a digital instrument. These components would typically be rectangular in distribution (equal probability anywhere within the estimated uncertainty range).', max_length=1)),
                ('std_dev', models.FloatField(blank=True, help_text='Standard deviation in terms of the units specified', null=True)),
                ('uc95', models.FloatField(blank=True, help_text='Uncertainty at 95% confidence in terms of the units specified', null=True, verbose_name='Uncertainty')),
                ('k', models.FloatField(default=2.0, help_text='The coverage factor for each input quantity. Typically 2.0 for a 95% confidence interval (normal distribution) or sqrt(3) for a rectangular distribution.', null=True, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)], verbose_name='k')),
                ('degrees_of_freedom', models.IntegerField(default=30, help_text='Degrees of freedom of calibration For a Type B estimate use the following as a guide:  3 for not very confident, 10 for moderate confidence, 30 for very confident.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)], verbose_name='dof')),
                ('uncertainty_budget', models.ForeignKey(help_text='Prism used for survey', on_delete=django.db.models.deletion.CASCADE, to='baseline_calibration.uncertainty_budget')),
            ],
            options={
                'ordering': ['uncertainty_budget', 'group', 'pk'],
            },
        ),
        migrations.CreateModel(
            name='Std_Deviation_Matrix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('std_uncertainty', models.FloatField(help_text='One Sigma Standard deviation of certified distance - Type A uncertianty only from LSA', verbose_name='One Sigma Standard deviation')),
                ('from_pillar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='distance_standard_deviation_from_pillar', to='calibrationsites.pillar')),
                ('pillar_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseline_calibration.pillar_survey')),
                ('to_pillar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='distance_standard_deviation_to_pillar', to='calibrationsites.pillar')),
            ],
        ),
        migrations.AddField(
            model_name='pillar_survey',
            name='uncertainty_budget',
            field=models.ForeignKey(help_text='Preset uncertainty budget', on_delete=django.db.models.deletion.PROTECT, to='baseline_calibration.uncertainty_budget'),
        ),
        migrations.CreateModel(
            name='Level_Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reduced_level', models.DecimalField(decimal_places=4, max_digits=7)),
                ('rl_standard_deviation', models.DecimalField(decimal_places=4, max_digits=7)),
                ('pillar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calibrationsites.pillar')),
                ('pillar_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseline_calibration.pillar_survey')),
            ],
            options={
                'ordering': ['pillar_survey', 'pillar__order'],
            },
        ),
        migrations.CreateModel(
            name='EDM_Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inst_ht', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Instrument height')),
                ('tgt_ht', models.DecimalField(decimal_places=3, max_digits=4, verbose_name='Target height')),
                ('hz_direction', models.DecimalField(decimal_places=6, max_digits=12)),
                ('raw_slope_dist', models.DecimalField(decimal_places=5, max_digits=9, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)], verbose_name='slope distance')),
                ('raw_temperature', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50.0)])),
                ('raw_pressure', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1500.0)])),
                ('raw_humidity', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100.0)])),
                ('use_for_alignment', models.BooleanField(default=True, help_text='This observation (will) / (will not) be used for the alignment survey.', verbose_name='Use for alignment survey')),
                ('use_for_distance', models.BooleanField(default=True, help_text='This observation (will) / (will not) be used to determine certified distances for the range calibration survey.', verbose_name='Use for surveying the certified distances')),
                ('from_pillar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_pillar', to='calibrationsites.pillar')),
                ('pillar_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseline_calibration.pillar_survey')),
                ('to_pillar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_pillar', to='calibrationsites.pillar')),
            ],
            options={
                'ordering': ['pillar_survey', 'from_pillar', 'to_pillar'],
            },
        ),
        migrations.CreateModel(
            name='Certified_Distance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField(verbose_name='certified distance')),
                ('a_uncertainty', models.FloatField(verbose_name='type A uncertainty of certified distance')),
                ('k_a_uncertainty', models.FloatField(default=2.0, verbose_name='Coverage factor for type A uncertainty of certified distance')),
                ('combined_uncertainty', models.FloatField(verbose_name='combined uncertainty of certified distance')),
                ('k_combined_uncertainty', models.FloatField(default=2.0, verbose_name='Coverage factor for combined uncertainty of certified distance')),
                ('offset', models.FloatField(verbose_name='pillar offset')),
                ('os_uncertainty', models.FloatField(verbose_name='pillar offset uncertainty')),
                ('k_os_uncertainty', models.FloatField(default=2.0, verbose_name='Coverage factor for pillar offset uncertainty')),
                ('reduced_level', models.FloatField()),
                ('rl_uncertainty', models.FloatField(verbose_name='Reduced level uncertainty')),
                ('k_rl_uncertainty', models.FloatField(default=2.0, verbose_name='Coverage factor for reduced level uncertainty')),
                ('uploaded_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_on', models.DateTimeField(auto_now=True, null=True)),
                ('from_pillar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certified_distance_from_pillar', to='calibrationsites.pillar')),
                ('pillar_survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseline_calibration.pillar_survey')),
                ('to_pillar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='certified_distance_to_pillar', to='calibrationsites.pillar')),
            ],
            options={
                'ordering': ['pillar_survey__survey_date', 'to_pillar__order'],
            },
        ),
        migrations.AddConstraint(
            model_name='uncertainty_budget_source',
            constraint=models.CheckConstraint(check=models.Q(('std_dev__isnull', False), ('uc95__isnull', False), _connector='OR'), name='not_both_null'),
        ),
        migrations.AlterUniqueTogether(
            name='uncertainty_budget',
            unique_together={('name', 'company')},
        ),
        migrations.AlterUniqueTogether(
            name='level_observation',
            unique_together={('pillar_survey', 'pillar')},
        ),
        migrations.AlterUniqueTogether(
            name='certified_distance',
            unique_together={('from_pillar', 'to_pillar', 'pillar_survey')},
        ),
        migrations.AlterUniqueTogether(
            name='accreditation',
            unique_together={('accredited_company', 'valid_from_date', 'valid_to_date')},
        ),
    ]
