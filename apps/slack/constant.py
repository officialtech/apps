"""all the constants related to slack will go here """

from decouple import config

client_id = config('CLIENT_ID_SLACK')
client_secret = config('CLIENT_SECRET_SLACK')
scope = config('SCOPE_SLACK')
redirect_url = config('REDIRECT_URL_SLACK')
state = config('STATE_SLACK')

AUTH_URL_SLACK = f"""https://slack.com/oauth/authorize?\
client_id={client_id}&\
scope={scope}&\
redirect_uri={redirect_url}&\
state={state}"""
