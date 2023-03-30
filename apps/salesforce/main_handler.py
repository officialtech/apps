"""main module handler for salesforce """

import json
import requests
from decouple import config

def get_auth_url():
    """cooking oauth url for salesforce """

    oauth_url = f"""{config("SALESFORCE_BASE_URL")}/services/oauth2/authorize?response_type=code&client_id={config("SALESFORCE_CONSUMER_KEY")}&redirect_uri={config("SALESFORCE_REDIRECT_URL")}&scope={config("SALESFORCE_SCOPE")}""".replace(" ", "%20")

    print(f"oAuth URL Salesforce: {oauth_url}")
    return json.dumps({"url": oauth_url, "message": "click the url and authenticate with SF"})


def get_oauth_tokens(code: str):
    """get oauth access and refresh tokens """
    oauth_url = f"""{config("SALESFORCE_BASE_URL")}/services/oauth2/token"""
    print(f"oAuth code URL: {oauth_url}")
    payload={
        'code': code,
        'grant_type': "authorization_code",
        'client_id': config("SALESFORCE_CONSUMER_KEY"),
        'client_secret': config("SALESFORCE_CONSUMER_SECRET"),
        'redirect_uri': config("SALESFORCE_REDIRECT_URL"),
        'format': "json",
    }
    headers = {}
    response = requests.request("POST", oauth_url, headers=headers, data=payload, timeout=10)
    print(response.text)

    return response.json()



def get_schemas(schema):
    """get schemas for given type """

    if schema == "contact":
        from apps.salesforce.contact import contact_schema
        return contact_schema()


    elif schema == "opportunity":
        from apps.salesforce.opportunity import oppertunity_schema
        return oppertunity_schema()

    elif schema == "lead":
        from apps.salesforce.lead import lead_schema
        return lead_schema()

    elif schema == "account":
        from apps.salesforce.account import account_schema
        return account_schema()

    else:
        return json.dumps({
            "schema": [],
            "message": "invalid schmea type",
        })
