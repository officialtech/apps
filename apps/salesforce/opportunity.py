"""this module is responsible for salesforce opportunity """


import json
from functools import reduce
from simple_salesforce import Salesforce

from apps.salesforce.constant import opportunity_schema_dict
from utils.genric import change_case

def oppertunity_schema():
    """return opportunity schema """
    return json.dumps({
        "oppertunity_schema": opportunity_schema_dict,
    })


def fetch_sf_opportunity_schema(instance_url, access_id, ):
    """fetching sf schema for opportunity """
    
    sf = Salesforce(instance_url=instance_url, session_id=access_id)
    schema = sf.Opportunity.describe()
    opportunity_picklist = []
    opportunity_schema_list = []
    try:
        for fieldDict in schema.get('fields', []):
            opportunity_schema_list.append({f"{fieldDict.get('name')}": f"{fieldDict.get('type')}"})
            fieldType = fieldDict.get('type')
            if fieldType in ['picklist']:
                name = fieldDict.get('name')
                empty_string = []
                for fd in fieldDict['picklistValues']:
                    output = fd.get('label')
                    empty_string.append(output)
                temp2 = {change_case(f"{fieldDict.get('name')}"): {'data_type': fieldDict.get('type'), 'value': empty_string}}
                opportunity_picklist.append(temp2)

    except Exception as e:
        print(f"Opportunity: Failed due to {e}")

    return json.dumps({
        "picklist": opportunity_picklist,
        "schema": reduce(lambda x, y: dict(x, **y), opportunity_schema_list),
    })
