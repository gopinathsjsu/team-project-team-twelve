# Generated by Django 4.1.2 on 2022-10-07 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Airport', '0002_rename_last_name_mio_user_last_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mio_user',
            old_name='Last_name',
            new_name='last_name',
        ),
    ]