# Generated by Django 5.0.5 on 2024-05-07 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='complete_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
