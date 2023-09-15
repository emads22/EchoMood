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
import re

from .models import User, Mood, Genre, Track
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
        # tracks=these_tracks,
        # serialize the list of tracks objects to JSON format before being used in JavaScript code
        tracks_json=serializers.serialize('json', these_tracks),
    )
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
  

 
    
