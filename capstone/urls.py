from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("mood", views.this_mood_playlist, name="this_mood_playlist"),
    path("playlists", views.playlists, name="playlists"),
    path("playlists/save/<str:playlist_mood>", views.save_playlist, name="save_playlist"),
    path("playlists/open/<int:playlist_id>", views.open_playlist, name="open_playlist"),
    path("playlists/rename/<int:playlist_id>", views.rename_playlist, name="rename_playlist"),
    path("playlists/delete/<int:playlist_id>", views.delete_playlist, name="delete_playlist"),
    
]
