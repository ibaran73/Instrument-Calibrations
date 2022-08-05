# Generated by Django 3.1 on 2022-06-15 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instruments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='staff_type',
            field=models.CharField(choices=[(None, 'Select one of the following'), ('invar', 'Invar'), ('fiberglass', 'Fiber glass'), ('wood', 'Wood'), ('aluminium', 'Aluminium'), ('steel', 'Steel'), ('epoxy', 'Carbon/epoxy'), ('e_glass', 'E-glass'), ('s2_glass', 'S2-glass')], max_length=10),
        ),
    ]
