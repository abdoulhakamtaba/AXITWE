# Generated by Django 3.0.2 on 2020-05-31 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_item_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='user',
        ),
    ]