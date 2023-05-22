from decouple import config

MSC_oAUTH_URL = f"""{config("OAUTH_URL_MICROSOFT")}client_id={config("CLIENT_ID_MICROSOFT")}&\
response_type=code&redirect_uri={config("REDIRECT_URL_MICROSOFT")}&\
scope={config("SCOPE_MICROSOFT")}&state=JB"""