# Generated by Django 4.1.2 on 2022-11-25 21:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0009_alter_mio_flight_schedule_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mio_flight_schedule',
            name='time',
            field=models.TimeField(default=datetime.time(21, 38, 30, 838413)),
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date(2022, 11, 25))),
                ('airline_flight_key', models.CharField(max_length=100)),
                ('passenger_id', models.CharField(max_length=50)),
                ('flight_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jwtapp.mio_flight_schedule')),
            ],
        ),
    ]
