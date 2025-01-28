# Generated by Django 5.1.4 on 2025-01-28 19:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_wallet_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='rial_balance',
            field=models.DecimalField(decimal_places=4, default=0, help_text='rial', max_digits=20, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
