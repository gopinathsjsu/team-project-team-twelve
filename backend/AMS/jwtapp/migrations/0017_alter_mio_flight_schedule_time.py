# Generated by Django 4.1.2 on 2022-12-02 23:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0016_alter_mio_flight_schedule_gate_close_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(23, 0, 47, 805707)),
        ),
    ]
