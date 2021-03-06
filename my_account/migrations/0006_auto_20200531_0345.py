# Generated by Django 3.0.2 on 2020-05-31 03:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0006_auto_20200531_0345'),
        ('my_account', '0005_auto_20200531_0345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myaccount',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Item'),
        ),
        migrations.AlterField(
            model_name='myaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
