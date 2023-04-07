"""Authentication """

from decouple import config
from apps.hubspot.constants import HS_SCOPES


HS_SCOPES = HS_SCOPES.replace(" ", "%20")

# old
# AUTH_URI = f"""https://app.hubspot.com/oauth/authorize?client_id={config("CLIENT_ID")}\
# &redirect_uri={config("REDIRECT_URI")}\
# &scope={HS_SCOPES}"""

# new
AUTH_URI = """https://app.hubspot.com/oauth/authorize?client_id=5c5d80a6-a551-4081-8a42-91ee10a86993&redirect_uri=https://saaswinlvl.bu-book.com/hubspot&scope=oauth%20crm.objects.contacts.read%20crm.schemas.contacts.read"""

