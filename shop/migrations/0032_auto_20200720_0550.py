# Generated by Django 3.0.2 on 2020-07-20 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0031_auto_20200706_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='location',
            field=models.CharField(max_length=100),
        ),
    ]
