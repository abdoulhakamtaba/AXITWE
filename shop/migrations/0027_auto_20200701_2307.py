# Generated by Django 3.0.2 on 2020-07-01 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0026_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]