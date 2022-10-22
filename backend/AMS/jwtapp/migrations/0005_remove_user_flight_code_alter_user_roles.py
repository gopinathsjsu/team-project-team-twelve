# Generated by Django 4.1.2 on 2022-10-21 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0004_user_flight_code_alter_user_airline_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='flight_code',
        ),
        migrations.AlterField(
            model_name='user',
            name='roles',
            field=models.CharField(choices=[('airport_employee', 'airport_employee'), ('airline_employee', 'airline_employee'), ('admin', 'admin')], max_length=50, null=True),
        ),
    ]