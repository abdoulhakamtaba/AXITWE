# Generated by Django 3.0.2 on 2020-05-31 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200531_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
