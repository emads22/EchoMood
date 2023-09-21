from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.db import IntegrityError
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.core import serializers
from django import forms
# from django.forms.widgets import HiddenInput
import re

from .models import User, Mood, Genre, Track, Playlist
from .tools import fetch_tracks_info, sync_drive_db, create_context, create_playlist, shuffle_list, PASSWORD_PATTERN



# <==================================================< Forms >==================================================>
class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 
                                      'placeholder': 'Username',
                                      'autofocus': 'autofocus'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 
                                          'placeholder': 'Password'}),
        required=True
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 
                                      'placeholder': 'Username',
                                      'autofocus': 'autofocus'}),
        required=True
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 
                                      'placeholder': 'Email Address'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 
                                          'placeholder': 'Password'}),
        required=True
    )
    confirmation = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 
                                          'placeholder': 'Confirm Password'}),
        required=True
    )


class MoodForm(forms.Form):    
    mood = forms.ChoiceField(
        # label='Select your mood ',
        # choices must be list of tuples (value, display_label), and added first choice as empty value. (genres are instances of Model table)
        choices=[('', 'Select your mood')] + [(mood.name, mood.name) for mood in Mood.objects.all()],
        initial='',     # here empty value is selected at first
        widget=forms.Select(attrs={'class': 'form-select form-select-lg fs-4 py-3 mood-form',
                                   'autofocus': 'autofocus'}),
        required=True
        )
    

class PlaylistForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 
                                      'placeholder': 'Playlist Name',
                                      'autofocus': 'autofocus'}),
        required=True
        )
    # define a playlist object hidden field with a default value None (initial)for every instance of PlaylistForm
    # playlist = forms.CharField(
    #     widget=forms.HiddenInput,
    #     initial=None
    #     )
    


# <==================================================<Views Functions>==================================================>
@login_required
def index(request): 
    # create the default context
    context = create_context(mood_form=MoodForm())

    try:
        # attempt to fetch info of the tracks in the google drive
        drive_tracks = fetch_tracks_info() 
    # handle exception (raised value error) from 'fetch_tracks_info()'
    except ValueError as error:
        # in case fetching failed for any reason (network, server,...) then skip syncing and continue with tracks available in the db for the moment
        these_tracks = Track.objects.all() 
        # context['messsage'] = f'An error occurred: {error}'
        # return render(request, "capstone/error.html", context=context)         
    else:
        # if successfully loaded (fetched) then sync the tracks from the drive with the tracks from db
        sync_drive_db(drive_tracks)
        # fetch all tracks info from db
        these_tracks = Track.objects.all()    

    # serialize the list of tracks objects to JSON format before being used in JavaScript code
    context['tracks_json'] = serializers.serialize('json', these_tracks)
    return render(request, "capstone/index.html", context=context)
                  

def login_view(request):
    # create the default context
    context = create_context(login_form=LoginForm())

    if request.method == "POST":
        this_login_form = LoginForm(request.POST)
        # validate form (login) 
        if this_login_form.is_valid(): 
            # Attempt to sign user in
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            # Check if authentication successful
            if user is not None:
                login(request, user)
                # add a message to the context to pass it to template
                context["message"] = "Logged in successfully."
                # return HttpResponseRedirect(reverse("index"))
                return render(request, "capstone/index.html", context=context)
            # otherwise authentication failed
            else:
                # add a message to the context to pass it to template
                context["message"] = "Invalid username and/or password."
                # pass the same input values of login form to the template to correct them 
                context["login_form"] = this_login_form

    # in case GET method or failed to login due to wrong credentials
    return render(request, "capstone/login.html", context=context)
    

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    # create the default context
    context = create_context(register_form=RegisterForm())

    if request.method == "POST":
        this_register_form = RegisterForm(request.POST)
        # validate form (register) 
        if this_register_form.is_valid(): 
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirmation = request.POST.get("confirmation")
            # make sure password matches pattern
            if re.match(PASSWORD_PATTERN, password):
                # make sure password matches confirmation
                if password != confirmation:
                    # add a message to the context to pass it to template
                    context["message"] = "Passwords must match."
                    # pass the same input values of login form to the template to correct them 
                    context["register_form"] = this_register_form
                # here password matches confirmation
                else:
                    # attempt to create new user
                    try:
                        user = User.objects.create_user(username, email, password)
                        user.save()
                    except IntegrityError:
                        # add a message to the context to pass it to template
                        context["message"] = "Username already taken."
                        # pass the same input values of login form to the template to correct them 
                        context["register_form"] = this_register_form
                    else:
                        # user creation was successful so log him in and redirect him to index template
                        login(request, user)
                        # add a message to the context to pass it to template
                        context["message"] = f"{username} registered successfully."
                        # return HttpResponseRedirect(reverse("index"))
                        return render(request, "capstone/index.html", context=context)
            # here password does not match pattern
            else:
                # add a message to the context to pass it to template
                context["message"] = """Valid password (in any order):\n   - 2 or more uppercase letters\n   - 2 or more digits\n   - 2 or more special characters from   _!@#$%&"""
                # pass the same input values of login form to the template to correct them 
                context["register_form"] = this_register_form
        
    # in case GET method or failed to register due to one of the two reasons above
    return render(request, "capstone/register.html", context=context)


@login_required
def this_mood_tracks(request):
    # create the default context
    context = create_context(mood_form=MoodForm())

    if request.method != "POST":
        context['message'] = "Only POST method"
        # handle other HTTP methods (like GET) as needed
        return render(request, "capstone/error.html", context)      # --fix            
    
    else:
        mood_form = MoodForm(request.POST)
        # validate form (mood) 
        if mood_form.is_valid(): 
            context['selected_mood'] = request.POST.get("mood")
            this_mood = Mood.objects.get(name=context['selected_mood'])
            context['playlist'] = create_playlist(this_mood)
            # serialize list of tracks objects to JSON format before using it in JavaScript code 
            context['tracks_json'] = serializers.serialize('json', context['playlist'])  
            # add 'playable' variable and 'mood_select' to signal showing playing music section and hiding mood selection section
            context['playable'] = True       
            context['mood_select'] = False 
            # create an instance of the playlist form and set the initial value for 'playlist' hidden field (default value)
            context['playlist_form'] = PlaylistForm(initial={'playlist': context['playlist']})      
            # redirect to same page 'index' bt with the collection of tracks based on this mood selected
            return render(request, "capstone/index.html", context=context)
        
        # otherwise not validated
        else:
            # do nothing cz its a form of one field so automatically will stay in same page
            pass
  


@login_required
def save_playlist(request, playlist_mood):
    save_playlist = True
    # create the default context
    context = create_context(playlist_form=PlaylistForm())
    
    if request.method != "POST":
        context['message'] = "Only POST method"
        # handle other HTTP methods (like GET) as needed
        return render(request, "capstone/error.html", context)  # Replace with your custom error page --fix       
    
    else:
        try:
            # this time using 'get_object_or_404()' instead of regular 'get()'
            this_mood = get_object_or_404(Mood, name=playlist_mood)
            print(this_mood)

        except Http404:
            # Handle the case where the mood with the given name was not found (get_object_or_404() raises a standard HTTP 404 "Not Found" error)
            return render(request, 'error.html')  # Replace with your custom error page --fix        
        
        else:
            playlist_form = PlaylistForm(request.POST)
            # validate playlist 
            if playlist_form.is_valid(): 
                # fetch the value of hidden field
                this_playlist = request.POST.get("playlist")
                # this_playlist_mood = Mood.objects.get(name=request.POST.get("mood"))
                this_playlist_name = request.POST.get("name")
                # Check if the playlist exists in the current user's playlists (order of tracks does not matter)
                current_user = request.user

                for playlist in current_user.playlists.all():
                    # if these sets are equal, it means that same tracks exist in both this playlist and the user's playlist, regardless of their 
                    # order so no need to save this existant playlist (A set is an unordered collection of unique elements so using a set here 
                    # ensures that the order of the tracks does not matter when comparing them)
                    if set(playlist.tracks.all()) == set(this_playlist):
                        save_playlist = False                        
                        context['message'] = "Playlist already exists."
                        break
                    elif playlist.name == this_playlist_name:
                        save_playlist = False
                        context['message'] = "Playlist with such name already exists."
                        break  
                
                if not save_playlist:
                    return render(request, "capstone/playlists.html", context=context)  # Replace with your custom error page --fix        
                
                # create a new playlist instance and set its name (no need to use 'save()' when using 'create()')
                new_playlist = Playlist.objects.create(name=this_playlist_name, mood=this_mood)
                # add the new playlist to the current user's playlists
                current_user.playlists.add(new_playlist)

                # --fix Delete Playlist

                context['user_playlists'] = current_user.playlists.all()   #--fix    
                # redirect to this user 'playlists' page
                return render(request, "capstone/playlists.html", context=context)
            
            # otherwise not validated
            else:
                # do nothing cz its a form of one field so automatically will stay in same page
                pass



@login_required
def playlists(request):

    return render(request, "capstone/playlists.html")