# Generated by Django 2.0.5 on 2018-09-10 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.CharField(max_length=500)),
                ('solved', models.BooleanField()),
                ('patientId', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highTemp', models.BooleanField(verbose_name='User had high temperature')),
                ('temp', models.SmallIntegerField(blank=True, verbose_name='Temperature')),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='FileRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('params', models.CharField(max_length=1000)),
                ('extendedRule', models.CharField(choices=[('mv_tll', '(Monitoring ruleset) Amount of urin relieved in last (n) hours. (Params: time_in_hours)'), ('mv_htr', '(Monitoring ruleset) Number of hearthbeats in last (n) secounds. (Params: time_in_secounds)'), ('mv_dih', '(Monitoring ruleset) (x) disease is in patients records history. (Params: disease_name)'), ('mv_owu', '(Monitoring ruleset) Oxygen level went up in last (n) minutes. (Params: time_in_minutes)'), ('mv_owd', '(Monitoring ruleset) Oxygen level went down in last (n) minutes. (Params: time_in_minutes)'), ('dv_hdc', '(Disease detection ruleset) Patient had (x) diagnosed multiple times in last (n) days. (Params: disease_name,number_of_days)'), ('dv_hsc', '(Disease detection ruleset) Patient had (x) symptom multiple times in last (n) days. (Params: syndrome_name,number_of_days)'), ('dv_htc', '(Disease detection ruleset) Patient had high temperature multiple times in last (n) days. (Params: number_of_days)'), ('dv_tac', '(Disease detection ruleset) Patient had temperature above (x) multiple times in last (n) days. (Params: temperature,number_of_days)'), ('dv_hmc', '(Disease detection ruleset) Patient had medicine that is (x) prescribed multiple times in last (n) days. (Params: medicine_type,number_of_days)'), ('pv_rdn', '(Patient data finding ruleset) Names of diseases that had repeated (x) times in last (n) days. (Params: number_of_repeats,number_of_days)'), ('pv_cmt', '(Patient data finding ruleset) Number of medicines of (x) type prescribed in last (n) days. (Params: medicine_type,number_of_days)'), ('pv_dpc', '(Patient data finding ruleset) Number of different doctors prescribing medicine of (x) type in last (n) days (Params: medicine_type,number_of_days)'), ('pv_dmc', '(Patient data finding ruleset) Number of diseases that had medicine of (x) type prescribed in last (n) days (Params: medicine_type,number_of_days)')], max_length=6, verbose_name='Extended rule')),
                ('extendsRuleset', models.CharField(choices=[('monv', 'Extends monitoring ruleset'), ('patv', 'Extends patient data finding ruleset'), ('disv', 'Extends disease detection ruleset')], max_length=4, verbose_name='Extended ruleset')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
                ('medtype', models.CharField(choices=[('0', 'Analgesic'), ('1', 'Antibiotic'), ('2', 'Other')], max_length=1, verbose_name='Medicine type')),
                ('ingredient', models.ManyToManyField(to='diagnostics.Ingredient', verbose_name='Ingredients')),
            ],
        ),
        migrations.CreateModel(
            name='MonitoringInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heartratebeat', models.SmallIntegerField(verbose_name='Heartbeat rate')),
                ('oxygenlevel', models.SmallIntegerField(verbose_name='Level of oxygen in blood')),
                ('liquidlevel', models.SmallIntegerField(verbose_name='Amount of urine produced')),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('surname', models.CharField(max_length=50, verbose_name='Surname')),
                ('alergying', models.ManyToManyField(blank=True, to='diagnostics.Ingredient', verbose_name='Allergic to ingredients')),
                ('alergymed', models.ManyToManyField(blank=True, to='diagnostics.Medicine', verbose_name='Allergic to medicines')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500, verbose_name='Rule title')),
                ('content', models.CharField(max_length=10000, verbose_name='Rule')),
                ('ruletype', models.CharField(choices=[('0', 'Disease decision making rule'), ('1', 'Patient alergy detection rule'), ('2', 'Find disease symptoms rule'), ('3', 'Detect disease based on symptoms rule'), ('4', 'Monitoring alarm rule'), ('5', 'Rule for grouping patients')], max_length=1, verbose_name='Rule type')),
                ('priority', models.IntegerField(verbose_name='Rule priority')),
            ],
            options={
                'permissions': (('run_rules', 'Can run decision making process'), ('manage_rules', 'Can make/change/delete rules')),
            },
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='monitoringinfo',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostics.Patient'),
        ),
        migrations.AlterUniqueTogether(
            name='filerule',
            unique_together={('extendedRule', 'params')},
        ),
        migrations.AddField(
            model_name='disease',
            name='regularsympt',
            field=models.ManyToManyField(related_name='regular_syndrome', to='diagnostics.Symptom', verbose_name='General symptoms'),
        ),
        migrations.AddField(
            model_name='disease',
            name='strongsympt',
            field=models.ManyToManyField(blank=True, related_name='strong_syndrome', to='diagnostics.Symptom', verbose_name='Specific symptoms'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='diagnostics.Disease', verbose_name='Diagnosed disease'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Doctor responsable for diagnosis'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='medicine',
            field=models.ManyToManyField(to='diagnostics.Medicine', verbose_name='Prescribed medicines'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='diagnostics.Patient', verbose_name='Patient'),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='symptoms',
            field=models.ManyToManyField(to='diagnostics.Symptom', verbose_name='Patient symptoms'),
        ),
    ]
