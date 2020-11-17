# Generated by Django 3.0.2 on 2020-07-06 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_category_top_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='item_variation',
        ),
        migrations.AlterField(
            model_name='item',
            name='negotiable',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.DeleteModel(
            name='ItemVariation',
        ),
    ]