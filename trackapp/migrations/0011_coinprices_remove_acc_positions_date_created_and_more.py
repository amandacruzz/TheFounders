# Generated by Django 4.0.3 on 2022-05-16 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0010_remove_acc_positions_coin_acc_positions_coin'),
    ]

    operations = [
        migrations.CreateModel(
            name='coinPrices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=4, null=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('derivedUSD', models.FloatField(default=None, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='acc_positions',
            name='date_created',
        ),
        migrations.AlterField(
            model_name='acc_positions',
            name='coin',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='trackapp.coins'),
        ),
        migrations.AlterField(
            model_name='acc_positions',
            name='quantity',
            field=models.FloatField(default=None, null=True),
        ),
    ]
