from django.contrib import admin
from .models import User, Mood, Genre, Track, Playlist


# Register your models here.
admin.site.register(User)
admin.site.register(Mood)
admin.site.register(Genre)
admin.site.register(Track)
admin.site.register(Playlist)
