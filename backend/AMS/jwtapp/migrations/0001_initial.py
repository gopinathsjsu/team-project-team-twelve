# Generated by Django 4.1.2 on 2022-10-26 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mio_airline',
            fields=[
                ('airline_flight_key', models.CharField(blank=True, max_length=100, primary_key=True, serialize=False)),
                ('airline_code', models.CharField(max_length=50)),
                ('flight_code', models.CharField(max_length=50)),
                ('airline_name', models.CharField(max_length=50)),
                ('is_available', models.BooleanField(default=False)),
            ],
            options={
                'unique_together': {('airline_code', 'flight_code')},
            },
        ),
        migrations.CreateModel(
            name='Mio_terminal',
            fields=[
                ('terminal_gate', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('gate_status', models.CharField(default='open', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mio_flight_schedule',
            fields=[
                ('fact_guid', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('arrival_departure', models.CharField(max_length=12)),
                ('time', models.DateTimeField()),
                ('baggage_carousel', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('airline_flight_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flight_key', to='jwtapp.mio_airline')),
                ('terminal_gate_key', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='airport_terminal_gate', to='jwtapp.mio_terminal')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('tc', models.BooleanField()),
                ('roles', models.CharField(choices=[('airport_employee', 'airport_employee'), ('airline_employee', 'airline_employee'), ('admin', 'admin')], max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('airline_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airline', to='jwtapp.mio_airline')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
