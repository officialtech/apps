"""this module is responsible for salesforce opportunity """


import json
from apps.salesforce.constant import opportunity_schema_dict


def oppertunity_schema():
    """return opportunity schema """
    return json.dumps({
        "oppertunity_schema": opportunity_schema_dict,
    })


