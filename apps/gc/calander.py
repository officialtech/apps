"""handle calander related task """
from __future__ import print_function

import datetime
import os.path

from decouple import config

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError, Error

from apps.gc.constant import SCOPES

def create_client_service(access_token, refresh_token):
    """creating calander service for using calander APIs """

    info = {
        "client_id": config('CLIENT_ID'),
        "client_secret": config('CLIENT_SECRET'),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    creds = Credentials.from_authorized_user_info(info=info, scopes=SCOPES.strip().split(" "))
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Error as eror:
        print(f"{eror} | while creating calander service")
        return


def test_events():
    """testing events """
    client = create_client_service(access_token="access_token", refresh_token="refresh_token")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = client.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(f"events: {events}")
    return events


def insert_event(access_token, refresh_token, event):
    """inserting event """
    service = create_client_service(access_token=access_token, refresh_token=refresh_token)
    service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1, sendNotifications=True).execute()
    print(f"Event created!")
    return service
