"""lead schema module """

import json
from apps.salesforce.constant import lead_schema_dict


def lead_schema():
    """return json lead schema """
    return json.dumps({
        "lead_schema": lead_schema_dict,
    })