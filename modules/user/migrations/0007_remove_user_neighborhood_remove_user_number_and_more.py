# Generated by Django 5.1.4 on 2025-01-18 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_user_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='neighborhood',
        ),
        migrations.RemoveField(
            model_name='user',
            name='number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='street',
        ),
    ]