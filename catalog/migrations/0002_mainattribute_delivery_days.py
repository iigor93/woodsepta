# Generated by Django 5.0.1 on 2024-04-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainattribute',
            name='delivery_days',
            field=models.IntegerField(blank=True, null=True, verbose_name='Производство дней'),
        ),
    ]
