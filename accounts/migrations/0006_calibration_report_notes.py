# Generated by Django 3.1 on 2022-06-20 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20220118_1211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calibration_Report_Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('B', 'Baseline Calibration'), ('R', 'Range Calibration'), ('E', 'EDMI Calibration'), ('S', 'Staff Calibration')], help_text='Report type that the notes will be added to', max_length=1)),
                ('note_type', models.CharField(choices=[('M', 'Manditory'), ('C', 'Company Specific')], help_text='Will this note appear accross all company reports', max_length=1)),
                ('note', models.TextField(help_text='Notes to be detailed at the end of each report', verbose_name='Report Note')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
            ],
            options={
                'ordering': ['company', 'report_type', 'note_type'],
            },
        ),
    ]
