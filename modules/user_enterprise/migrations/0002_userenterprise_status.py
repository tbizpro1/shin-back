# Generated by Django 5.1.4 on 2024-12-20 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_enterprise', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userenterprise',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')], default='pending', max_length=20, verbose_name='Invitation Status'),
        ),
    ]