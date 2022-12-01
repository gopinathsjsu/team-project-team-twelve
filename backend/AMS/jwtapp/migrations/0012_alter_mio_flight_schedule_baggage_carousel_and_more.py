# Generated by Django 4.1.2 on 2022-11-28 19:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0011_rename_passenger_mio_passenger_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='baggage_carousel',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='date',
            field=models.DateField(default=datetime.date(2022, 11, 28)),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(19, 15, 42, 349661)),
        ),
        migrations.AlterField(
            model_name='mio_passenger',
            name='date',
            field=models.DateField(default=datetime.date(2022, 11, 28)),
        ),
    ]