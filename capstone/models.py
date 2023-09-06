from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    pass


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'
    

class Mood(models.Model):
    name = models.CharField(max_length=50, unique=True)
    genres = models.ManyToManyField('Genre', related_name='moods')

    def __str__(self):
        return f'{self.name}'


class Track(models.Model):
    title = models.CharField(max_length=200)
    gdrive_id = models.CharField(max_length=200, unique=True)
    artist = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)    # automatically populated with current date
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genre_tracks")

    def __str__(self):
        return f'{self.title} - {self.artist} -- ({self.gdrive_id}) | {self.genre.name}'




