# Generated by Django 3.1.2 on 2020-10-26 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buyer_page', '0008_listing_min_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='current_price',
            field=models.IntegerField(default=0),
        ),
    ]
