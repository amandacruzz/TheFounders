# Generated by Django 4.0.4 on 2022-05-06 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0004_acc_positions_date_created_alter_acc_positions_coin_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=4, null=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='acc_positions',
            name='coin',
            field=models.CharField(choices=[('PLS', 'PLS'), ('HEX', 'HEX'), ('PLSX', 'PLSX')], max_length=4, null=True),
        ),
    ]
