# Generated by Django 4.1.7 on 2024-06-27 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capstone', '0011_playlist_user_playlists'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='audio',
            field=models.BinaryField(default=b''),
        ),
    ]
