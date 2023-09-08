from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from .apps import all_about, things, matter
from .models import Genre, Track


def fetch_tracks_info(page_token=None):
    """ using the Drive v3 API, get a service account to access the Google Drive API and retrieve file names and IDs from a specific folder """

    # scopes are defined in the project in google cloud console
    scopes = ['https://www.googleapis.com/auth/drive.readonly']
    # drive ID of the folder we want to read tracks from
    folder_id = '1IrFRyAt87RgIFwbVBjvewRvn9G5yKGS7'

    try:
        service_account_info = all_about(things, matter)
        # create creds using the service account info 
        creds = service_account.Credentials.from_service_account_info(
            service_account_info,
            scopes=scopes
        )
        # build the Google Drive API service object
        drive_service = build('drive', 'v3', credentials=creds)

        try:
            # list all files in the specified folder (as per docs) (trashed=false means not in trash)
            query = f"'{folder_id}' in parents and trashed=false"
            # by default 'page_token' is None cz 1st page
            if page_token:
                response = drive_service.files().list(q=query, pageToken=page_token).execute()
            else:
                response = drive_service.files().list(q=query).execute()

            tracks = response.get('files', [])   
            # response is dict that contains the response data from Google Drive API request, if 'nextPageToken' key not existent default value None
            next_page_token = response.get('nextPageToken', None)

            # check if there are more pages to fetch
            if next_page_token:
                # recursively fetch the next page
                remaining_tracks = fetch_tracks_info(page_token=next_page_token)
                # combine the contents of 'tracks' and 'remaining_tracks' lists into a single list
                tracks.extend(remaining_tracks) 

            return tracks     

        except HttpError as http_error:
            return f'An HTTP error occurred: {http_error}'

    except Exception as error:
        return f'An error occurred: {error}'
    

# use 'transaction.atomic()' to ensure that either all changes are committed to the db or none of them if an error occurs during synchronization
@transaction.atomic
def sync_drive_db(drive_tracks):
    """ populate the db of this server with info of new tracks added in drive, also remove any track info from db if the track not existent anymore in drive """

    drive_tracks_titles = []
    for track in drive_tracks:
        title = track['name'][:-4].split(" - ")
        # collect track names in a list
        drive_tracks_titles.append(title[1])
        # fetch the genre and test if error of non existence rises
        try:
            # get the genre object of this track from the title
            this_genre = Genre.objects.get(name=title[2])
        # handle the case when the genre doesn't exist in db
        except ObjectDoesNotExist:
            this_genre = "N/A"

        # use get_or_create to either get an existing track or create a new one ('obj' is he retrieved or created object, 'created' is a
        # boolean to indicate whether the object was created (True) or retrieved from the database)
        track, created = Track.objects.get_or_create(
            gdrive_id=track['id'],
            defaults={
                'title': title[1],
                'artist': title[0],                
                'genre': this_genre
            }
        )
    
    # catch tracks that don't meet this criteria (tracks that arent existent in drive anymore)
    db_tracks = Track.objects.exclude(title__in=drive_tracks_titles)
    db_tracks.delete()


def create_context(**kwargs):
    """ 
    creates context template to avoid repeating the passing args in views everytime. use get() to set a default value 'None' if key not available
    """
    
    context = {
        "mood_form": kwargs.get("mood_form", None),
        "tracks": kwargs.get("tracks", None),
        "tracks_json": kwargs.get("tracks_json", None),
        "message": kwargs.get("message", None),
        "selected_mood": kwargs.get("selected_mood", None),
        "this_mood_genres": kwargs.get("this_mood_genres", None),
        }

    return context