# Generated by Django 3.0.2 on 2020-07-06 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0030_auto_20200706_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='negotiable',
            field=models.BooleanField(default=False),
        ),
    ]
