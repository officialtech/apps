"""module to handle second level main APIs logics """
import requests
import datetime
import uuid

from decouple import config
from google.auth.exceptions import RefreshError

from apps.gc.constant import TOKEN_URL
from apps.gc.db import connect
from apps.gc.generic import get_request_google, user_profile, regenerate_access_token
from apps.gc.calander import insert_event, create_client_service


event = {
  "summary": "Test event from JB 1",
  "location": "800 Howard St., San Francisco, CA 94103",
  "description": "A chance to hear more about developer products.",
  "conferenceData": {
    "conferenceId": uuid.uuid4().hex,
    "createRequest": {
      "requestId": uuid.uuid4().hex
    }
  },
  "start": {
    "dateTime": "2023-03-6T09:00:00-07:00",
    "timeZone": "America/Los_Angeles"
  },
  "end": {
    "dateTime": "2023-04-06T17:00:00-07:00",
    "timeZone": "America/Los_Angeles"
  },
  "recurrence": [
    "RRULE:FREQ=DAILY;COUNT=2"
  ],
  "attendees": [
    {"email": "sandeepsharma34532@gmail.com"},
    {"email": "jbthehellboy@gmail.com"}
  ],
  "reminders": {
    "useDefault": False,
    "overrides": [
      {"method": "email", "minutes": 2460},
      {"method": "popup", "minutes": 10}
    ]
  }
}

def code_handler(request):
    """code handler is used to generate auth tokens and save those token to DB """

    print("Headers: ", request.headers, "Args: ", request.args, "Body: ", request.data)
    code = request.headers.get("code")
    payload = {
        "code": code,
        "client_id": config('CLIENT_ID'),
        "client_secret": config('CLIENT_SECRET'),
        "redirect_uri": config('REDIRECT_URL_GOOGLE'),
        "grant_type": "authorization_code",
    }

    response, status = get_request_google(url=TOKEN_URL, payload=payload)
    profile = user_profile(access_token=response.get("access_token"))
    response["user_id"] = profile.get("id")
    response["email"] = profile.get("email")
    response["status"] = status
    save_creds(response)
    return response
    

def save_creds(creds):
    """save user credentials to db """
    conn = connect()
    cur = conn.cursor()
    query = f"""INSERT INTO `company_integrations` (google, user_id) VALUES({creds.get('refresh_token')!r}, {creds.get('user_id')!r}) """
    print(query)
    cur.execute(query)
    conn.commit() # I don't know why but commit is required here!
    conn.close()
    return True


def insert_event_handler(request):
    """inserting event """

    print("Headers: ", request.headers, "Args: ", request.args, "Body: ", request.data)
    service = insert_event(access_token=request.json.get("access_token"), refresh_token=request.json.get("refresh_token"), event=request.json.get("event"))
    return service.events().list(calendarId="primary").execute()


def get_events_handler(request):
    """get all the events created by user """

    print("Headers: ", request.headers, "Args: ", request.args, "Body: ", request.data)
    client = create_client_service(access_token=request.headers.get("access_token"), refresh_token=request.headers.get("refresh_token"))
    try:
      return client.events().list(calendarId="primary").execute()
    
    except RefreshError as rfer:
        print(f"Refresh Token Error | {rfer}")
        tokens = regenerate_access_token(refresh_token=request.headers.get("refresh_token"))
        client = create_client_service(access_token=tokens.get("access_token"), refresh_token=request.headers.get("refresh_token"))
        return client.events().list(calendarId="primary").execute()


def get_event_handler(request):
    """get all the events created by user """

    print("Headers: ", request.headers, "Args: ", request.args, "Body: ", request.data)
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    client = create_client_service(access_token=request.headers.get("access_token"), refresh_token=request.headers.get("refresh_token"))
    try:
      return client.events().list(
          calendarId="primary",
          timeMin=request.headers.get("date_utc")+"T00:00:00.000Z" if request.headers.get("date_utc") else now,
          timeMax=request.headers.get("date_utc")+"T23:59:59.000Z" if request.args.get("date_utc") else now,
          
      ).execute()
    
    except RefreshError as rfer:
        print(f"Refresh Token Error | {rfer}")
        tokens = regenerate_access_token(refresh_token=request.headers.get("refresh_token"))
        client = create_client_service(access_token=tokens.get("access_token"), refresh_token=request.headers.get("refresh_token"))
        return client.events().list(
            calendarId="primary",
            timeMin=request.headers.get("date_utc")+"T00:00:00.00Z" if request.headers.get("date_utc") else now,
            timeMax=request.headers.get("date_utc")+"T23:59:59.000Z" if request.headers.get("date_utc") else now,
            
          ).execute()
