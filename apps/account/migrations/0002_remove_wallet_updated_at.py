# Generated by Django 5.1.4 on 2025-01-28 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='updated_at',
        ),
    ]
