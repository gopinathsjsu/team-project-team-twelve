# Generated by Django 4.1.2 on 2022-12-02 21:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0014_alter_mio_flight_schedule_gate_close_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='gate_close_time',
            field=models.TimeField(blank=True, default=datetime.time(21, 54, 44, 182709), null=True),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='gate_open_time',
            field=models.TimeField(blank=True, default=datetime.time(22, 4, 44, 182723), null=True),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(21, 59, 44, 182699)),
        ),
    ]