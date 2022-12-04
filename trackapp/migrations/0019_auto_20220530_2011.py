# Generated by Django 3.2.13 on 2022-05-30 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0018_alter_acc_positions_time_bought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_positions',
            name='coin',
            field=models.CharField(choices=[('HEX', 'HEX'), ('PLS', 'PLS'), ('PLSX', 'PLSX'), ('eETH', 'eETH'), ('INC', 'INC')], default='', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='coinprices',
            name='symbol',
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coins',
            name='ticker',
            field=models.CharField(choices=[('HEX', 'HEX'), ('PLS', 'PLS'), ('PLSX', 'PLSX'), ('eETH', 'eETH'), ('INC', 'INC')], max_length=8, null=True),
        ),
    ]
