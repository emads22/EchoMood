from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import random

from .models import Genre, Track
from finalproject.settings import TRACKS_ROOT


# regex to catch a string containing only alphanumeric characters and the specified special characters, with a length between 6 and 8 characters,
# with 4 Positive lookaheads respectively for at least 2 uppercase letters, at least 2 digits, and at least 2 special characters
# from the set [_!@#$%&]
PASSWORD_PATTERN = r"^(?=.*[A-Z].*[A-Z])(?=.*[0-9].*[0-9])(?=.*[_!@#$%&].*[_!@#$%&])[\w!@#$%&]{6,8}$"
PLAYLIST_MAX_TRACKS = 16


def fetch_tracks_info():
    """ 
    retrieve tracks as Path objects from a specific folder in the server 
    """
    try:
        # tracks_dir = MEDIA_ROOT / "tracks"
        all_tracks = list(TRACKS_ROOT.glob("*.mp3"))
        # after successfully loaded (fetched) the tracks (info data) then sync the tracks from the drive with the tracks from db
        sync_drive_db(all_tracks)
        # return the list of tracks (Path objects) fetched from local dir
        return all_tracks

    except Exception as error:
        # handle error by propagating it to caller function
        raise ValueError(f'An error occurred: {error}')


# use 'transaction.atomic()' to ensure that either all changes are committed to the db or none of them if an error occurs during synchronization
@transaction.atomic
def sync_drive_db(server_tracks):
    """ 
    populate the db of this server with info of new tracks added in drive, also remove any track info from db if the track not existent anymore in drive 
    """
    server_tracks_titles = []

    for track in server_tracks:
        # extract the info needed from title (artist, title, genre)
        track_name = track.stem
        artist, title, genre = track_name.split(" - ")

        # collect track titles in a list
        server_tracks_titles.append(title)

        # fetch the genre and test if error of non existence rises
        try:
            # get the genre object of this track from the title
            genre_obj = Genre.objects.get(name=genre)
        # handle the case when the genre doesn't exist in db by assign a default value ("Misc" genre)
        except ObjectDoesNotExist:
            genre_obj = Genre.objects.get(name="Miscellaneous")

        # use get_or_create to either get an existing track or create a new one ('obj' is the retrieved or created object, 'created' is a
        # boolean to indicate whether the object was created (True) or retrieved from the database)
        track_obj, created = Track.objects.get_or_create(
            # gdrive_id=track['id'],
            title=title,
            artist=artist,
            genre=genre_obj,
            audio_file=track.name
        )

    # catch tracks that don't meet this criteria (tracks that arent existent in server anymore) in order to delete them from db
    db_tracks = Track.objects.exclude(title__in=server_tracks_titles)
    db_tracks.delete()


def create_context(**kwargs):
    """ 
    creates context template to avoid repeating the passing args in views everytime. use get() to set a default value 'None' if key not available
    """
    context = {
        "register_form": kwargs.get("register_form", None),
        "login_form": kwargs.get("login_form", None),
        "mood_form": kwargs.get("mood_form", None),
        "playlist_form": kwargs.get("playlist_form", None),
        "playlist": kwargs.get("playlist", None),
        "playlist_json": kwargs.get("playlist_json", None),
        "is_in_user_playlists": kwargs.get("is_in_user_playlists", False),
        "selected_mood": kwargs.get("selected_mood", None),
        # here default value of 'playable' is False not None
        "playable": kwargs.get("playable", False),
    }
    return context


def create_playlist(mood):
    """ 
    generate a playlist of max_tracks number of tracks randomly selected from the list of tracks relative to this mood passed as arg then shuffled
    """
    # get all the genres associated with this mood
    this_mood_genres = mood.genres.all()
    # using the 'genre__in' lookup retrieve all tracks where the genre is in the 'this_mood_genres' queryset,
    # which represents all genres associated with the selected mood. And convert it to a list in order to shuffle it
    tracks_of_this_mood = list(Track.objects.filter(
        genre__in=this_mood_genres).all())
    # generate a random sample (a subset) or a list of unique elements randomly selected from the 'tracks_of_this_mood' list
    playlist = random.sample(tracks_of_this_mood, PLAYLIST_MAX_TRACKS)
    # shuffle this list a "random number between 6 and 9" times
    playlist = shuffle_list(playlist, random.randint(6, 9))
    # after being shuffled convert it back from list to queryset like it was in 'tracks_of_this_mood'
    playlist_queryset = Track.objects.filter(
        pk__in=[track.pk for track in playlist])
    # return playlist as queryset
    return playlist_queryset


def rename_playlist_numbered(playlist_name):
    """ 
    returns a playlist name that differs from the original name passed as arg. increment by 1 if it ends with an int otherwise directly append '_1'
    """
    if playlist_name[-1].isdigit():
        temp = int(playlist_name[-1])
        temp += 1
        result_name = playlist_name.replace(playlist_name[-1], str(temp))
    else:
        result_name = playlist_name + "_1"

    return result_name


def shuffle_list(this_list, num_shuffles):
    """
    recursively shuffle 'this_list' for n number of times then return it 
    """
    if num_shuffles <= 0:
        return this_list
    else:
        random.shuffle(this_list)
        return shuffle_list(this_list, num_shuffles-1)
