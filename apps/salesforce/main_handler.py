"""main module handler for salesforce """

import json
import requests

from decouple import config

from apps.salesforce.constant import PROFILE
from apps.salesforce.db_ops import save_profile

from apps.salesforce.contact import fetch_sf_contact_schema
from apps.salesforce.lead import fetch_sf_lead_schema
from apps.salesforce.account import fetch_sf_account_schema
from apps.salesforce.opportunity import fetch_sf_opportunity_schema


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



def fetch_user_details(access_token, ):
    """fetching user profile details in SF """

    _headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.request(
        method="GET",
        url=PROFILE,
        headers=_headers,
        timeout=10,
    )

    # save user details to DB
    save_profile()

    return json.dumps({
        "status": response.status_code,
        "data": response.json(),
    })


def fetch_contact_schema(request, ):
    """fetch schema of contact from SF """
    _instance_url = request.headers.get("instance_url", "if empty")
    _access_token = request.headers.get("access_token", "if empty")
    return fetch_sf_contact_schema(instance_url=_instance_url, access_id=_access_token)


def fetch_lead_schema(request, ):
    """fetch schema of lead from SF """
    _instance_url = request.headers.get("instance_url", "if empty")
    _access_token = request.headers.get("access_token", "if empty")
    return fetch_sf_lead_schema(instance_url=_instance_url, access_id=_access_token)


def fetch_account_schema(request, ):
    """fetch schema of account from SF """
    _instance_url = request.headers.get("instance_url", "if empty")
    _access_token = request.headers.get("access_token", "if empty")
    return fetch_sf_account_schema(instance_url=_instance_url, access_id=_access_token)


def fetch_opportunity_schema(request, ):
    """fetch schema of opportunity from SF """
    _instance_url = request.headers.get("instance_url", "if empty")
    _access_token = request.headers.get("access_token", "if empty")
    return fetch_sf_opportunity_schema(instance_url=_instance_url, access_id=_access_token)

