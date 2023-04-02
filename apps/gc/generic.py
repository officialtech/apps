"""generic module for reusable code """

import json
import requests

from decouple import config

from apps.gc.constant import USER_PROFILE, TOKEN_URL

def get_request_google(url, payload):
    """send get request to get auth tokens like access/refresh token """
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request(
        method="POST",
        url=url,
        data=json.dumps(payload),
        headers=headers,
        timeout=10,
    )
    return response.json(), response.status_code

def regenerate_access_token(refresh_token, url=TOKEN_URL, client_id=None, client_secret=None, grant_type="refresh_token"):
    """regenerating access token using refresh token """
    payload = {
        "refresh_token": refresh_token,
        "client_id": client_id if client_id else config('CLIENT_ID'),
        "client_secret": client_secret if client_secret else config('CLIENT_SECRET'),
        "grant_type": grant_type,
    }
    return get_request_google(url=url, payload=payload)
    


def user_profile(access_token):
    """getting user profile details using access token """
    header = {
        "Authorization": f"Bearer {access_token}",
    }
    data = {}
    response = requests.request(method="GET", url=USER_PROFILE, headers=header, data=data, timeout=10)
    return response.json()