# Generated by Django 4.1.2 on 2022-12-03 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0018_baggagecar_alter_mio_flight_schedule_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(11, 27, 4, 522166)),
        ),
    ]