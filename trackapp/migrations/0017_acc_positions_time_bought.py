# Generated by Django 3.2.13 on 2022-05-22 20:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0016_remove_acc_positions_time_bought'),
    ]

    operations = [
        migrations.AddField(
            model_name='acc_positions',
            name='time_bought',
            field=models.DateTimeField(default=datetime.datetime.now, null=True),
        ),
    ]
