from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.core import serializers

from .models import User, Mood, Genre, Track
from .tools import fetch_tracks_info, sync_drive_db


def index(request): 
    drive_tracks = fetch_tracks_info()
    # sync the tracks from the drive with the tracks from db
    sync_drive_db(drive_tracks)
    # fetch all tracks in db
    these_tracks = Track.objects.all();
    # serialize the list of tracks objects to JSON format before being used in JavaScript code
    tracks_json = serializers.serialize('json', these_tracks)
    return render(request, "capstone/index.html", {
        'tracks': these_tracks,
        'tracks_json': tracks_json,
        'genres': Genre.objects.all(),
        'moods': Mood.objects.all()
    })
                  

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")
    

def this_genre_tracks(request):
    if request.method != "POST":
        pass
    else:
        selected_genre = request.POST.get("genre")
        if Genre.objects.filter(name=selected_genre).exists():
            this_genre = Genre.objects.get(name=selected_genre)
            genre_exists = True
        else:
            genre_exists = False
        
        return render(request, "capstone/index.html", {
            'tracks': this_genre.genre_tracks.all() if genre_exists else [],
            'genres': Genre.objects.all()
        })
    
