
import json
import requests
from decouple import config


TOKEN_URL = """https://zoom.us/oauth/token/"""

def fetch_token(request, ):
    """fetch access token using code """
    auth_code = json.loads(request.data).get("code")

    body = {
        "code": f"{auth_code}",
        "grant_type": "authorization_code",
        "client_id": config("ZOOM_CLIENT_ID_DEV"),
    }

    response = requests.request(
        method="POST",
        url=TOKEN_URL,
        data=body,
    )

    print(response.status_code, response.text)
    return json.dumps({
        "data": response.json(),
    })