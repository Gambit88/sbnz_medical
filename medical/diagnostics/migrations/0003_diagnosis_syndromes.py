# Generated by Django 2.0.5 on 2018-08-29 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0002_auto_20180827_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosis',
            name='syndromes',
            field=models.ManyToManyField(to='diagnostics.Syndrome', verbose_name='Patient syndromes'),
        ),
    ]
