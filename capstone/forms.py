from django import forms
from .models import Mood


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
        # choices must be list of tuples (value, display_label), and added first choice as empty value. (genres are instances of Model table)
        choices=[('', 'Select your mood')] + [(mood.name, mood.name)
                                              for mood in Mood.objects.all()],
        initial='',     # here empty value is selected at first
        widget=forms.Select(attrs={'class': 'form-select form-select-lg fs-4 py-3 mood-form',
                                   'autofocus': 'autofocus'
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
