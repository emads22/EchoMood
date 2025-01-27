# Generated by Django 4.1.7 on 2023-09-02 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("capstone", "0002_alter_user_groups_alter_user_user_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Mood",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("gdrive_id", models.CharField(max_length=200)),
                ("artist", models.CharField(max_length=100)),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                (
                    "genre",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="genre_tracks",
                        to="capstone.genre",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="genre",
            name="mood",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mood_genres",
                to="capstone.mood",
            ),
        ),
    ]
