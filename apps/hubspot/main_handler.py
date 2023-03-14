"""Main module request handler """

import requests
from decouple import config

from apps.hubspot.constants import TOKEN_URL, HEADERS
from apps.hubspot.auth import AUTH_URI


def create_auth_url():
    """generating auth url of Hubspot """
    return AUTH_URI

def generate_tokens(request):
    """generating auth tokens using auth code """
    payload = f"""code={request.headers.get("code")}&\
                grant_type=authorization_code&\
                client_id={config("CLIENT_ID")}&\
                client_secret={config("CLIENT_SECRET")}&\
                redirect_uri={config("REDIRECT_URI")}""".replace(" ", "")
    tokens = requests.request(
        method="POST",
        url=TOKEN_URL,
        headers=HEADERS,
        data=payload,
    )
    return tokens.json()