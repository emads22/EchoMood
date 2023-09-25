from django.shortcuts import render, get_object_or_404, redirect
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
import time

from .models import User, Mood, Genre, Track, Playlist
from .tools import fetch_tracks_info, sync_drive_db, create_context, create_playlist, rename_playlist_numbered, PASSWORD_PATTERN



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
                                #    'autofocus': 'autofocus'
                                   }),
        required=True
        )
    

class PlaylistForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 
                                      'placeholder': 'Playlist Name',
                                      'autofocus': 'autofocus',
                                      }),
        required=True
        )
    


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
    context['playlist_json'] = serializers.serialize('json', these_tracks)
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
                messages.error(request, "Logged in successfully.")
                return HttpResponseRedirect(reverse("index"))
                # return render(request, "capstone/index.html", context=context)
            # otherwise authentication failed
            else:
                # add a message to the context to pass it to template
                messages.error(request, "Invalid username and/or password.")

    # in case GET method or failed to login due to wrong credentials
    return render(request, "capstone/login.html", context=context)
    

@login_required
def logout_view(request):
    logout(request)    
    messages.error(request, "Logged out successfully.")
    return HttpResponseRedirect(reverse("login"))


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
                    # add a message to pass it to template
                    messages.error(request, "Passwords must match.")
                    # pass the same input values of login form to the template to correct them 
                    context["register_form"] = this_register_form
                # here password matches confirmation
                else:
                    # attempt to create new user
                    try:
                        user = User.objects.create_user(username, email, password)
                        user.save()
                    except IntegrityError:
                        # add a message to pass it to template
                        messages.error(request, "Username already taken.")
                        # pass the same input values of login form to the template to correct them 
                        context["register_form"] = this_register_form
                    else:
                        # user creation was successful so log him in and redirect him to index template
                        login(request, user)
                        # add a message to pass it to template
                        messages.error(request, f"{username} registered successfully.")
                        return HttpResponseRedirect(reverse("index"))
                    
            # here password does not match pattern
            else:
                # add a message to pass it to template
                messages.error(
                    request, 
                    """Valid password (in any order):\n   - 2 or more uppercase letters\n   - 2 or more digits\n   - 2 or more special characters from   _!@#$%&"""
                    )
                # pass the same input values of login form to the template to correct them 
                context["register_form"] = this_register_form
        
    # in case GET method or failed to register due to one of the two reasons above
    return render(request, "capstone/register.html", context=context)


@login_required
def this_mood_playlist(request):
    # create the default context
    context = create_context(
        mood_form=MoodForm(),
        playlist_form=PlaylistForm())

    if request.method != "POST":        
        # handle other HTTP methods (like GET) as needed
        messages.error(request, "Only POST method.")
        return HttpResponseRedirect(reverse('index'))       # alternatively:    return redirect('index')
    
    else:
        mood_form = MoodForm(request.POST)
        # validate form (mood) 
        if mood_form.is_valid(): 
            context['selected_mood'] = request.POST.get("mood")
            this_mood = Mood.objects.get(name=context['selected_mood'])
            this_playlist = create_playlist(this_mood)            
            context['playlist'] = this_playlist        
            # serialize list of tracks objects to JSON format before using it in JavaScript code and also to be able to save playlist in session 
            # and access it in other view functions
            context['playlist_json'] = serializers.serialize('json', this_playlist) 
            # check if this playlist (queryset of tracks) exists in the current user's playlists and pass the boolean var to template 
            for playlist in request.user.playlists.all():
                if set(playlist.tracks.all()) == set(this_playlist):
                    context['is_in_user_playlists'] = True 
            # save the deserialized playlist in the session after defining session data in 'settings.py'
            request.session['playlist'] = context['playlist_json']
            # add 'playable' variable and 'mood_select' to signal showing playing music section and hiding mood selection section
            context['playable'] = True       
            context['mood_select'] = False    
            # redirect to same page 'index' bt with the collection of tracks based on this mood selected
            return render(request, "capstone/index.html", context=context)
        
        # otherwise not validated
        else:
            # do nothing cz its a form of one field so automatically will stay in same page
            pass



@login_required
def playlists(request):
    # create the default context to be also used in 'playlists' template for the rename playlist form
    context = create_context(playlist_form=PlaylistForm())
    return render(request, "capstone/playlists.html", context=context)



@login_required
def save_playlist(request, playlist_mood):    
    if request.method != "POST":
        # handle other HTTP methods (like GET) as needed
        messages.error(request, "Only POST method.")
        return redirect('index')
    
    else:
        try:
            # this time using 'get_object_or_404()' instead of regular 'get()'
            this_mood = get_object_or_404(Mood, name=playlist_mood)
        except Http404:
            # Handle the case where the mood with the given name was not found (get_object_or_404() raises a standard HTTP 404 "Not Found" error)
            messages.error(request, "Invalid Mood. Playlist cannot be saved.")
            return redirect('index')        
        else:
            playlist_form = PlaylistForm(request.POST)
            # validate playlist 
            if playlist_form.is_valid(): 
                # fetch the name of playlist that user entered
                this_playlist_name = request.POST.get("name")

                if not request.session.get("playlist"):
                    # if serialized playlist that is saved in session isnt found (maybe deleted) set a message and redirect to 'index' page
                    messages.error(request, "Playlist Not Found. Select your mood to generate a new one.")
                    return redirect('index')
                else:
                    # deserialize JSON data that was serialized and saved in session if it exists in session (maybe deleted)
                    deserialized_playlist = serializers.deserialize('json', request.session.get("playlist"))
                    # convert it to list to access the objects (list acting like queryset)
                    this_playlist = [item.object for item in deserialized_playlist]
                    # delete the playlist saved in sessions is good practice for security reasons and also to save memory
                    del request.session['playlist']

                    # Check if the playlist exists in the current user's playlists (order of tracks does not matter)
                    current_user = request.user
                    for playlist in current_user.playlists.all():
                        # if these sets are equal, it means that same tracks exist in both this playlist and the user's playlist, regardless of their 
                        # order so no need to save this existant playlist (A set is an unordered collection of unique elements so using a set here 
                        # ensures that the order of the tracks does not matter when comparing them)
                        if set(playlist.tracks.all()) == set(this_playlist):                       
                            messages.error(request, "Another playlist with these tracks already exists.")
                            # redirect to this user 'playlists' page after failing to save playlist cz another playlist wth same tracks exists
                            return redirect('playlists')
                        
                        elif playlist.name == this_playlist_name:
                            # adjust the playlist name by adding number for differentiation
                            this_playlist_name = rename_playlist_numbered(this_playlist_name)
                            break
                    
                    # create a new playlist instance and set its name (no need to use 'save()' when using 'create()')
                    new_playlist = Playlist.objects.create(name=this_playlist_name, mood=this_mood)
                    # add the tracks to the new playlist
                    for track in this_playlist:
                        # First, save the object and then add the relationships. 
                        # (to avoid 'instance is on database "default", value is on database "None"' error) (ref: 
                        # "https://stackoverflow.com/questions/7837033/valueerror-cannot-add-instance-is-on-database-default-value-is-on-databas")
                        track.save()
                        new_playlist.tracks.add(track)
                    # save the new playlist to the database
                    new_playlist.save()
                    # add the new playlist to the current user's playlists
                    current_user.playlists.add(new_playlist)  
                    # send a message of success
                    messages.success(request, "Playlist saved successfully.")
                    # redirect to this user 'playlists' page after saving playlist
                    return redirect('playlists')
            
            # otherwise not validated
            else:
                # do nothing cz its a form of one field so automatically will stay in same page
                pass



@login_required
def open_playlist(request, playlist_id):
    try:
        # attempt to get this playlist
        this_playlist = get_object_or_404(Playlist, pk=playlist_id)
    except Http404:
        # Handle the case where the playlist with the given id was not found (get_object_or_404() raises a standard HTTP 404 "Not Found" error)
        messages.error(request, "Playlist Not found.")
        return redirect('playlists')    
    else:
        context = create_context(
            playlist=this_playlist,
            # serialize the list of tracks objects to JSON format before being used in JavaScript code
            playlist_json=serializers.serialize('json', this_playlist.tracks.all()),
            # add 'playable' variable to signal showing playing music section and hiding playlists section
            playable = True
        )
        # redirect to 'playlists' template        
        return render(request, "capstone/playlists.html", context=context)



@login_required
def rename_playlist(request, playlist_id):
    # create the default context
    context = create_context(playlist_form=PlaylistForm())
        
    if request.method == "POST":
        try:
            # attempt to get this playlist
            this_playlist = get_object_or_404(Playlist, pk=playlist_id)
        except Http404:
            # Handle the case where the playlist with the given id was not found (get_object_or_404() raises a standard HTTP 404 "Not Found" error)
            messages.error(request, "Playlist Not found.")
            return redirect('playlists')    
        else:
            playlist_form = PlaylistForm(request.POST)
            # validate playlist 
            if playlist_form.is_valid(): 
                # fetch the new name of playlist that user entered
                new_playlist_name = request.POST.get("name")
                # check if new name is the same as original name
                if new_playlist_name == this_playlist.name:
                    messages.error(request, "No changes occurred. Playlist name remains the same.")
                    
                else:
                    current_user = request.user
                    if current_user.playlists.filter(name = new_playlist_name).exists():
                        # adjust the playlist name by adding number for differentiation
                        new_playlist_name = rename_playlist_numbered(new_playlist_name)

                    # change this playlist name
                    this_playlist.name = new_playlist_name
                    # save this playlist
                    this_playlist.save()
                    # send message of success 
                    messages.success(request, "Playlist renamed successfully.")
            
            # otherwise not validated
            else:
                # do nothing cz its a form of one field so automatically will stay in same page
                pass

    # in case GET method or failed to rename or even succeded to rename it
    return render(request, "capstone/playlists.html", context=context)



@login_required
def delete_playlist(request, playlist_id):
    try:
        # attempt to get this playlist
        this_playlist = get_object_or_404(Playlist, pk=playlist_id)
    except Http404:
        # Handle the case where the playlist with the given id was not found (get_object_or_404() raises a standard HTTP 404 "Not Found" error)
        messages.error(request, "Playlist Not found.")  
    else:
        # delete the playlist object
        this_playlist.delete()
        # send message of success 
        messages.success(request, "Playlist deleted successfully.")
        
    # redirect to 'playlists' page whether succeeded or failed in deleting the playlist
    return redirect('playlists')







