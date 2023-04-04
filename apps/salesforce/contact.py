"""contact schema module """

import json
from functools import reduce

from apps.salesforce.constant import contact_schema_dict
from simple_salesforce import Salesforce
from utils.genric import change_case


def contact_schema():
    """return json type of contact schema """
    return json.dumps({
        "conatact_schema": contact_schema_dict,
    })


def fetch_sf_contact_schema(instance_url, access_id, ):
    """fetching sf schema for contact """
    
    sf = Salesforce(instance_url=instance_url, session_id=access_id)
    schema = sf.Contact.describe()
    contact_picklist = []
    contact_schema_list = []
    try:
        for fieldDict in schema.get('fields', []):
            contact_schema_list.append({f"{fieldDict.get('name')}": f"{fieldDict.get('type')}"})
            fieldType = fieldDict.get('type')
            if fieldType in ['picklist']:
                name = fieldDict.get('name')
                empty_string = []
                for fd in fieldDict['picklistValues']:
                    output = fd.get('label')
                    empty_string.append(output)
                temp2 = {change_case(f"{fieldDict.get('name')}"): {'data_type': fieldDict.get('type'), 'value': empty_string}}
                contact_picklist.append(temp2)

    except Exception as e:
        print(f"Contact: Failed due to {e}")

    return json.dumps({
        "picklist": contact_picklist,
        "schema": reduce(lambda x, y: dict(x, **y), contact_schema_list),
    })


