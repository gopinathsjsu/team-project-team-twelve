# Generated by Django 4.1.2 on 2022-10-21 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jwtapp', '0003_alter_user_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='flight_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='flight', to='jwtapp.mio_airline'),
        ),
        migrations.AlterField(
            model_name='user',
            name='airline_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='airline', to='jwtapp.mio_airline'),
        ),
    ]