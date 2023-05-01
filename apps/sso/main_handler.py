
from decouple import config
from apps.gc.generic import get_request_google, user_profile
from apps.gc.constant import TOKEN_URL

GOOGLE_SSO_SCOPES = """https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid""".replace(" ", "%20")

SSO_AUTH_URL = f"""https://accounts.google.com/o/oauth2/v2/auth/oauth?redirect_uri={config('GOOGLE_SSO_REDIRECT_URL')}&prompt=consent&response_type=code&client_id={config('GOOGLE_SSO_CLIENT_ID')}&scope={GOOGLE_SSO_SCOPES}&access_type=offline"""


def sso_code_handler(request):
    """code handler is used to generate auth tokens and save those token to DB """

    print("Headers: ", request.headers, "Args: ", request.args, "Body: ", request.data)
    code = request.headers.get("code")
    payload = {
        "code": code,
        "client_id": config('GOOGLE_SSO_CLIENT_ID'),
        "client_secret": config('GOOGLE_SSO_CLIENT_SECRET'),
        "redirect_uri": config('GOOGLE_SSO_REDIRECT_URL'),
        "grant_type": "authorization_code",
    }
    response, status = get_request_google(url=TOKEN_URL, payload=payload)
    profile = user_profile(access_token=response.get("access_token"))
    response["user_id"] = profile.get("id")
    response["email"] = profile.get("email")
    response["status"] = status
    return response



##########################################################################################
#
#   GOOGLE ADMIN WORKSPACE SSO
#
##########################################################################################

SSO_URL = """https://accounts.google.com/o/saml2/idp?idpid=C02qk8qs1"""
ENTITY_ID = """https://accounts.google.com/o/saml2?idpid=C02qk8qs1"""
SHA256FINGERPRINT = """4B:C5:56:EE:43:97:05:B1:91:4E:B3:2F:14:F3:F4:80:B1:BF:80:71:66:ED:8A:0A:8E:AB:FA:AD:2E:1F:58:33"""
