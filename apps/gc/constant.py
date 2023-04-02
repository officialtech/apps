"""All the constants """

from decouple import config


SCOPES = """https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/calendar.events.readonly https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/userinfo.profile"""

RAW_AUTH_URL = f"""https://accounts.google.com/o/oauth2/v2/auth/oauth?redirect_uri={config('REDIRECT_URL_GOOGLE')}&prompt=consent&response_type=code&client_id={config('CLIENT_ID')}&scope={SCOPES}&access_type=offline"""

AUTH_URL = RAW_AUTH_URL.replace(' ', '%20')

TOKEN_URL = """https://oauth2.googleapis.com/token"""
USER_PROFILE = """https://www.googleapis.com/oauth2/v2/userinfo"""