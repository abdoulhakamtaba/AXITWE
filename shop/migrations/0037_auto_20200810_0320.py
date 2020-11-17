# Generated by Django 3.0.2 on 2020-08-10 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0036_item_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=20, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='item',
            name='username',
        ),
    ]