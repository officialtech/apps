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
from apps.slack.main_handler import get_access_token


app = Flask(__name__)

################################## APIs GC ########################################################

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
        "data": [AUTH_URL, ],
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


################################ APIs GC ^ ##############################################################

########################################## HUBSPOT #######################################################

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

############################################# HUBSPOT ^ ####################################################


##################################### Slack start ########################################

@app.route(rule="/get/slack/url/", methods=["GET", ])
@cross_origin()
def auth_url_slack():
    """get auth url of slack """
    return json.dumps({
        "url": AUTH_URL_SLACK.strip(),
        "status": status.HTTP_200_OK,
        "message": "open url and try to authenticate with Slack",
    })

@app.route(rule="/post/slack/code/", methods=["POST", ])
@cross_origin()
def get_access_token_slack():
    """get access token using code """

    _code = eval(request.data).get("code")
    response = get_access_token(code=_code)
    return response


##################################### Slack end ########################################


if __name__ == '__main__':
    from decouple import config
    app.run(debug=config("FLASK_DEBUG", cast=bool, default=False), )
