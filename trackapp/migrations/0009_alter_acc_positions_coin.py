# Generated by Django 4.0.4 on 2022-05-06 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackapp', '0008_acc_positions_username_id_remove_acc_positions_coin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_positions',
            name='coin',
            field=models.ManyToManyField(null=True, to='trackapp.coins'),
        ),
    ]
