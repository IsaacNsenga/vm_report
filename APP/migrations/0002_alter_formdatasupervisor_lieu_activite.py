# Generated by Django 5.1.4 on 2025-02-01 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formdatasupervisor',
            name='lieu_activite',
            field=models.CharField(max_length=100),
        ),
    ]
