# Generated by Django 3.0.2 on 2020-06-05 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_auto_20200605_0424'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='color',
        ),
        migrations.RemoveField(
            model_name='item',
            name='size',
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(max_length=3, upload_to=''),
        ),
    ]