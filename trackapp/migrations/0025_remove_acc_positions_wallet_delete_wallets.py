# Generated by Django 4.1.3 on 2022-12-04 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0024_wallets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acc_positions',
            name='wallet',
        ),
        migrations.DeleteModel(
            name='Wallets',
        ),
    ]