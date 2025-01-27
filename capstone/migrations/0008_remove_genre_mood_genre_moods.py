# Generated by Django 4.1.7 on 2023-09-06 07:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("capstone", "0007_alter_genre_mood_alter_track_genre"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="genre",
            name="mood",
        ),
        migrations.AddField(
            model_name="genre",
            name="moods",
            field=models.ManyToManyField(related_name="genres", to="capstone.mood"),
        ),
    ]
