"""contact schema module """

import json
from apps.salesforce.constant import contact_schema_dict


def contact_schema():
    """return json type of contact schema """
    return json.dumps({
        "conatact_schema": contact_schema_dict,
    })