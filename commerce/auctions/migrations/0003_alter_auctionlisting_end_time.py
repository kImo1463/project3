# Generated by Django 5.0.2 on 2024-07-10 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlisting_bid_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
