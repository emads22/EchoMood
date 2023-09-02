from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    pass


class Mood(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'

class Genre(models.Model):
    label = models.CharField(max_length=50)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, blank=True, null=True, related_name="mood_genres")

    def __str__(self):
        return f'{self.label}'

class Track(models.Model):
    title = models.CharField(max_length=200)
    gdrive_id = models.CharField(max_length=200)
    artist = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)    # automatically populated with current date
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, related_name="genre_tracks")

    def __str__(self):
        return f'{self.title} - {self.artist} -- ({self.gdrive_id})'




