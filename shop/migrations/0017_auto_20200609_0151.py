# Generated by Django 3.0.2 on 2020-06-09 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.FileField(upload_to='media/images'),
        ),
    ]
