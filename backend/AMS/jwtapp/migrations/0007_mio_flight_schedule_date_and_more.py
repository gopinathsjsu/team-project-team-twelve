# Generated by Django 4.1.2 on 2022-11-25 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0006_mio_airline_main_alter_mio_airline_airline_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mio_flight_schedule',
            name='date',
            field=models.DateField(default=datetime.date(2022, 11, 25)),
        ),
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(20, 55, 9, 624569)),
        ),
    ]