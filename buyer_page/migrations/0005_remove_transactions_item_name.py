# Generated by Django 3.1.2 on 2020-10-21 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buyer_page', '0004_auto_20201021_0125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactions',
            name='item_name',
        ),
    ]