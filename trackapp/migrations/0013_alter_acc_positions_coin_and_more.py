# Generated by Django 4.0.4 on 2022-05-17 00:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trackapp', '0012_remove_coinprices_id_remove_coinprices_ticker_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acc_positions',
            name='coin',
            field=models.ForeignKey(choices=[('PLS', 'PLS'), ('HEX', 'HEX'), ('PLSX', 'PLSX')], default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='trackapp.coins'),
        ),
        migrations.AlterField(
            model_name='acc_positions',
            name='username_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
