"""account schema module """

import json
from apps.salesforce.constant import account_schema_dict


def account_schema():
    """return json account schema """
    return json.dumps({
        "account_schema": account_schema_dict,
    })