"""main handler for slack module """

import requests
from apps.slack.constant import client_id, client_secret, redirect_url

def get_access_token(code):
    """getting access token using auth code """

    access_token_url = "https://slack.com/api/oauth.access"
    payload=f"code={code}&client_id={client_id}&client_secret={client_secret}&grant_type=authorization_code&redirect_uri={redirect_url}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", access_token_url, headers=headers, data=payload, timeout=10)
    return response.json()
