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
from django import forms

from .models import User, Mood, Genre, Track
from .tools import fetch_tracks_info, sync_drive_db, create_context, create_playlist, shuffle_list



# <==================================================< Forms >==================================================>
class MoodForm(forms.Form):    
    mood = forms.ChoiceField(
        label='Enter your mood ',
        # choices must be list of tuples (value, display_label), and added first choice as empty value. (genres are instances of Model table)
        choices=[('', 'Select a mood')] + [(mood.name, mood.name) for mood in Mood.objects.all()],
        initial='',     # here empty value is selected at first
        widget=forms.Select(attrs={'class': 'form-select form-select-lg'})
        )
    
    

# <==================================================<Views Functions>==================================================>
def index(request): 
    drive_tracks = fetch_tracks_info()
    # sync the tracks from the drive with the tracks from db
    sync_drive_db(drive_tracks)
    # fetch all tracks in db
    these_tracks = Track.objects.all();
    # create the default context
    context = create_context(
        mood_form=MoodForm(),
        tracks=these_tracks,
        # serialize the list of tracks objects to JSON format before being used in JavaScript code
        tracks_json=serializers.serialize('json', these_tracks),
    )
    return render(request, "capstone/index.html", context=context)
                  

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


def mood_tracks(request):
    # create the default context
    context = create_context(
        mood_form=MoodForm()
    )

    if request.method != "POST":
        context['message'] = "Only POST method"
        # handle other HTTP methods (like GET) as needed
        return render(request, "capstone/error.html", context)
    
    else:
        mood_form = MoodForm(request.POST)
        # validate form (mood) 
        if mood_form.is_valid(): 
            context['selected_mood'] = request.POST.get("mood")
            this_mood = Mood.objects.get(name=context['selected_mood'])
            context['tracks'] = create_playlist(this_mood)
            # serialize list of tracks objects to JSON format before using it in JavaScript code 
            context['tracks_json'] = serializers.serialize('json', context['tracks'])            
            # redirect to same page 'index' bt with the collection of tracks based on this mood selected
            return render(request, "capstone/index.html", context=context)
        
        # otherwise not validated
        else:
            # do nothing cz its a form of one field so automatically will stay in same page
            pass
  

 
    
