# Generated by Django 3.0.2 on 2020-05-31 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20200531_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='location',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='item',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]