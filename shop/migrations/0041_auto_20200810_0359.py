# Generated by Django 3.0.2 on 2020-08-10 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0040_auto_20200810_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='username',
            name='username',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]