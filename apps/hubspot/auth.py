"""Authentication """

from decouple import config
from apps.hubspot.constants import HS_SCOPES


HS_SCOPES = HS_SCOPES.replace(" ", "%20")

AUTH_URI = f"""https://app.hubspot.com/oauth/authorize?client_id={config("CLIENT_ID")}\
&redirect_uri={config("REDIRECT_URI")}\
&scope={HS_SCOPES}"""

