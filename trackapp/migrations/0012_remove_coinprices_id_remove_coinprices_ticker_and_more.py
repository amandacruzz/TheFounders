# Generated by Django 4.0.4 on 2022-05-16 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0011_coinprices_remove_acc_positions_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coinprices',
            name='id',
        ),
        migrations.RemoveField(
            model_name='coinprices',
            name='ticker',
        ),
        migrations.AddField(
            model_name='coinprices',
            name='symbol',
            field=models.CharField(default='A', max_length=4, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
