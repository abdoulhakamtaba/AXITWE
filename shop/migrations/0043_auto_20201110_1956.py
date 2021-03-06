# Generated by Django 3.0.2 on 2020-11-10 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0042_auto_20201110_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='discount_price',
        ),
        migrations.AlterField(
            model_name='item',
            name='call_number',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='item',
            name='whatsapp_number',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.FileField(max_length=3, upload_to='media/images'),
        ),
    ]
