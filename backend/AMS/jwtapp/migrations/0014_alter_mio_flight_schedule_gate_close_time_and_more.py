# Generated by Django 4.1.2 on 2022-12-02 21:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0013_mio_flight_schedule_gate_close_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='gate_close_time',
            field=models.TimeField(default=datetime.time(21, 53, 12, 621718)),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='gate_open_time',
            field=models.TimeField(default=datetime.time(22, 3, 12, 621734)),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(21, 58, 12, 621708)),
        ),
    ]
