# Generated by Django 2.0.5 on 2018-09-11 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0002_alarm_alarm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filerule',
            name='extendedRule',
            field=models.CharField(choices=[('mv_tll', '(Monitoring ruleset) Amount of urin relieved in last (n) hours. (Params: time_in_hours)'), ('mv_htr', '(Monitoring ruleset) Number of hearthbeats in last (n) secounds. (Params: time_in_secounds)'), ('mv_dih', '(Monitoring ruleset) (x) disease is in patients records history. (Params: disease_name)'), ('mv_owu', '(Monitoring ruleset) Oxygen level went up in last (n) minutes. (Params: time_in_minutes)'), ('mv_owd', '(Monitoring ruleset) Oxygen level went down in last (n) minutes. (Params: time_in_minutes)'), ('dv_hdc', '(Disease detection ruleset) Patient had (x) diagnosed multiple times in last (n) days. (Params: disease_name,number_of_days)'), ('dv_hsc', '(Disease detection ruleset) Patient had (x) syndrome multiple times in last (n) days. (Params: syndrome_name,number_of_days)'), ('dv_htc', '(Disease detection ruleset) Patient had high temperature multiple times in last (n) days. (Params: number_of_days)'), ('dv_tac', '(Disease detection ruleset) Patient had temperature above (x) multiple times in last (n) days. (Params: temperature,number_of_days)'), ('dv_hmc', '(Disease detection ruleset) Patient had medicine that is (x) prescribed multiple times in last (n) days. (Params: medicine_type,number_of_days)'), ('pv_rdn', '(Patient data finding ruleset) Names of diseases that had repeated (x) times in last (n) days. (Params: number_of_repeats,number_of_days)'), ('pv_cmt', '(Patient data finding ruleset) Number of medicines of (x) type prescribed in last (n) days. (Params: medicine_type,number_of_days)'), ('pv_dpc', '(Patient data finding ruleset) Number of different doctors prescribing medicine of (x) type in last (n) days (Params: medicine_type,number_of_days)'), ('pv_dmc', '(Patient data finding ruleset) Number of diseases that had medicine of (x) type prescribed in last (n) days (Params: medicine_type,number_of_days)'), ('pv_mcn', '(Patient data finding ruleset) Number of diseases that did not have medicine of (x) type prescribed in last (n) days (Params: medicine_type,number_of_days)')], max_length=6, verbose_name='Extended rule'),
        ),
    ]
