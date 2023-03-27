"""main handler for slack module """

import json
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
    print("Debugging: ", response.text)

    return response.json()


def get_conversation_list(access_token):
    """lists all channels in a slack team """

    channels_url = "https://slack.com/api/conversations.list"
    payload={}
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.request("GET", channels_url, headers=headers, data=payload, timeout=10)
    print("Debugging: ", response.text)

    return response.json()


def send_message_to_channel(channel_id, message, access_token):
    """send message within your workspace """

    message_url = "https://slack.com/api/chat.postMessage"

    payload = json.dumps({
        "channel": f"{channel_id}",
        "text": f"{message}"
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    response = requests.request("POST", message_url, headers=headers, data=payload, timeout=10)

    print(response.text)
    return response.json()