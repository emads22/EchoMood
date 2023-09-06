from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
    

def populate_tracks_db(all_tracks):
    """ populate the db of this server with tracks info """

    for track in all_tracks:
        title = track['name'][:-4].split(" - ")
        # only if a track with this id doesnt exist in db then insert it 
        if not Track.objects.filter(gdrive_id=track['id']).exists():
            new_track = Track(
                title=title[1],
                gdrive_id=track['id'],
                artist=title[0], 
                # get the genre object of this track from the title
                genre=Genre.objects.get(name=title[2])
            )
            new_track.save()
        
