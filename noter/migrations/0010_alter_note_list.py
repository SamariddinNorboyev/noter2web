# Generated by Django 5.1.4 on 2025-01-19 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('noter', '0009_note_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='list',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='noter.list'),
        ),
    ]
