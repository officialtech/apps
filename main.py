"""main module of this project for APIs """
import json

from flask import Flask, request
from flask_cors import cross_origin
from flask_api import status

from apps.gc.main_handler import code_handler, insert_event_handler, get_events_handler, get_event_handler
from apps.gc.constant import AUTH_URL
from apps.gc.db import connect

from apps.hubspot.main_handler import generate_tokens, create_auth_url
from apps.slack.constant import AUTH_URL_SLACK
from apps.slack.main_handler import get_access_token, get_conversation_list, send_message_to_channel
from apps.salesforce.main_handler import (
    get_auth_url, get_oauth_tokens, get_schemas, fetch_user_details
    )
from apps.salesforce.lead import fetch_lead_data
from apps.salesforce.user_team_member import fetch_user_team_member


app = Flask(__name__)


#########################################################################################
#
#   Google Calander start
#
#########################################################################################

@app.route(rule="/ping/", methods=["GET", ])
@cross_origin()
def ping():
    """checking DB connection """
    conn = connect()
    return json.dumps({"response": conn}) if isinstance(conn, str) else json.dumps({"response": "success"})


@app.route(rule="/auth-url/", methods=["GET", ])
@cross_origin()
def auth_url():
    """creating auth url for authentication """
    print(AUTH_URL)
    return json.dumps({
        "status": status.HTTP_200_OK,
        "url": AUTH_URL,
    })

@app.route("/code/", methods=["GET", ])
@cross_origin()
def code():
    """saving authenticated tokens """
    return code_handler(request=request)

@app.route("/insert/event/", methods=["POST", ])
@cross_origin()
def insert_event():
    """insert event to calander """
    return insert_event_handler(request=request)

@app.route("/get/events/", methods=["GET", ])
@cross_origin()
def get_events():
    """get events from calander """
    return get_events_handler(request=request)


@app.route("/get/event/", methods=["GET", ])
@cross_origin()
def get_event():
    """get events from calander """
    return get_event_handler(request=request)


#########################################################################################
#
#   google Calander end
#
#########################################################################################



#########################################################################################
#
#   Hubspot start
#
#########################################################################################

@app.route(rule="/get/hs/url/", methods=["GET", ])
@cross_origin()
def auth_url_hubspot():
    """generate auth URL """
    return create_auth_url()

@app.route(rule="/get/hs/tokens/", methods=["GET", ])
@cross_origin()
def credentials():
    """exchange authorization code for tokens """
    return generate_tokens(request)


#########################################################################################
#
#   Hubspot end
#
#########################################################################################




#########################################################################################
#
#   Slack start
#
#########################################################################################

@app.route(rule="/get/slack/url/", methods=["GET", ])
@cross_origin()
def auth_url_slack():
    """get auth url of slack """
    return json.dumps({
        "url": AUTH_URL_SLACK.strip(),
        "status": status.HTTP_200_OK,
        "message": "open url and try to authenticate with Slack",
    })

@app.route(rule="/post/slack/code/", methods=["GET", ])
@cross_origin()
def get_access_token_slack():
    """get access token using code """

    _code = request.headers.get("code")
    response = get_access_token(code=_code)
    return response


@app.route(rule="/get/slack/channels/", methods=["GET", ])
@cross_origin()
def get_all_channels():
    """list of all channels in workspace """
    _access_token = request.headers.get("access_token")
    return get_conversation_list(access_token=_access_token)


@app.route(rule="/post/slack/message/", methods=["POST", ])
@cross_origin()
def send_message():
    """send message to particular channel of given workspace """
    CHANNEL_ID = ""
    _access_token = request.headers.get("access_token")
    _body = eval(request.data)
    _channel_id = _body.get("channel", CHANNEL_ID)
    text = _body.get("text")
    return send_message_to_channel(channel_id=_channel_id, message=text, access_token=_access_token)


#########################################################################################
#
#   Slack end
#
#########################################################################################




#########################################################################################
#
#   Salesforce start
#
#########################################################################################

@app.route(rule="/get/sf/url/", methods=["GET", ])
@cross_origin()
def get_oauth_url():
    """get SF oAuth URL """
    return get_auth_url()


@app.route(rule="/post/sf/code/", methods=["GET", ])
@cross_origin()
def oauth_token():
    """fetch tokens using oauth code """
    _code = request.headers.get("code")
    return get_oauth_tokens(code=_code)


@app.route(rule="/get/sf/schema/", methods=["GET", ])
@cross_origin()
def get_schema_main():
    """get SF schemas """
    schema_type = request.headers.get("schema")
    return get_schemas(schema=schema_type)


@app.route(rule="/get/sf/profile/", methods=["GET", ])
@cross_origin()
def fetch_profile_details():
    """fetch user profile details """
    _access_token = request.headers.get("access_token", "if empty")
    return fetch_user_details(access_token=_access_token, )


@app.route(rule="/get/sf/lead/data", methods=["GET", ])
@cross_origin()
def get_sf_lead_data():
    """fetch lead data """
    _access_token = request.headers.get("access_token", "if empty")
    _instance_url = request.headers.get("instance_url", "if empty")
    return fetch_lead_data(instance_url=_instance_url, access_token=_access_token, )


@app.route(rule="/get/sf/userTeamMember/", methods=["GET", ])
@cross_origin()
def user_team_member_main():
    """fetch user team member """
    _access_token = request.headers.get("access_token", "if empty")
    _instance_url = request.headers.get("instance_url", "if empty")
    return fetch_user_team_member(instance_url=_instance_url, access_token=_access_token, )


#########################################################################################
#
#   Salesforce end
#
#########################################################################################


if __name__ == '__main__':
    from decouple import config
    app.run(debug=config("FLASK_DEBUG", cast=bool, default=False), )
