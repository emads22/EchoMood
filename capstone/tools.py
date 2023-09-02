from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .apps import all_about, things, matter


def fetch_tracks_info():
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
            # list all files in the specified folder (as per docs)
            response = drive_service.files().list(q=f"'{folder_id}' in parents").execute()
            tracks = response.get('files', [])    
            return tracks     

        except HttpError as http_error:
             return f'An HTTP error occurred: {http_error}'

    except Exception as e:
        print(f'An error occurred: {e}')
        
