# Generated by Django 3.0.2 on 2020-05-31 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20200531_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]