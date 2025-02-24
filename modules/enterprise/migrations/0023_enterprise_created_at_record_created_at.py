# Generated by Django 5.1.4 on 2025-02-18 19:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0022_companymetrics_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Data de criação do registro'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='record',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Data de criação do registro'),
            preserve_default=False,
        ),
    ]
