# Generated by Django 4.1.2 on 2022-11-25 21:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0007_mio_flight_schedule_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(21, 3, 47, 310825)),
        ),
    ]