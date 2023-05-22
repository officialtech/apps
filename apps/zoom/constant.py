from decouple import config
from urllib.parse import quote


ZOOM_oAUTH_URL = f"""{config("ZOOM_OAUTH_BASE_URL")}client_id={config("ZOOM_CLIENT_ID_DEV")}&\
response_type=code&redirect_uri={config("ZOOM_REDIRECT_URL_DEV")}&\
scope={quote(config("ZOOM_SCOPES"))}&state=JB"""

