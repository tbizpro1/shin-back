# Generated by Django 5.1.4 on 2025-02-17 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0019_alter_enterprise_revenue_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='companymetrics',
            name='captable',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Porcentagem de participação acionária (exemplo: 12.50 para 12,5%)', max_digits=5, null=True),
        ),
    ]
