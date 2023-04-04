"""lead schema module """

import json
from functools import reduce

from simple_salesforce import Salesforce # client library

from apps.salesforce.constant import lead_schema_dict
from utils.genric import change_case


def lead_schema():
    """return json lead schema """
    return json.dumps({
        "lead_schema": lead_schema_dict,
    })


def fetch_lead_data(instance_url, access_token, ):
    """fetching lead data using client library of SF """

    sf = Salesforce(instance_url=instance_url, session_id=access_token)
    # Get all lead data using SOQL query
    leads = sf.query("SELECT Id, FirstName, LastName, Company, Email FROM Lead")
    _leads = [
        {
            "lead_id": lead["Id"],
            "first_name": lead["FirstName"],
            "last_name": lead["LastName"],
            "company": lead["Company"],
            "email": lead["Email"],
        }
        for lead in leads['records']
    ]
    
    return _leads


def fetch_sf_lead_schema(instance_url, access_id, ):
    """fetching sf schema for lead """
    
    sf = Salesforce(instance_url=instance_url, session_id=access_id)
    schema = sf.Lead.describe()
    lead_picklist = []
    lead_schema_list = []
    try:
        for fieldDict in schema.get('fields', []):
            lead_schema_list.append({f"{fieldDict.get('name')}": f"{fieldDict.get('type')}"})
            fieldType = fieldDict.get('type')
            if fieldType in ['picklist']:
                name = fieldDict.get('name')
                empty_string = []
                for fd in fieldDict['picklistValues']:
                    output = fd.get('label')
                    empty_string.append(output)
                temp2 = {change_case(f"{fieldDict.get('name')}"): {'data_type': fieldDict.get('type'), 'value': empty_string}}
                lead_picklist.append(temp2)

    except Exception as e:
        print(f"Lead: Failed due to {e}")

    return json.dumps({
        "picklist": lead_picklist,
        "schema": reduce(lambda x, y: dict(x, **y), lead_schema_list),
    })
