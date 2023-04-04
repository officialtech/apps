"""account schema module """

import json
from functools import reduce

from simple_salesforce import Salesforce

from apps.salesforce.constant import account_schema_dict
from utils.genric import change_case


def account_schema():
    """return json account schema """
    return json.dumps({
        "account_schema": account_schema_dict,
    })


def fetch_sf_account_schema(instance_url, access_id, ):
    """fetching sf schema for account """
    
    sf = Salesforce(instance_url=instance_url, session_id=access_id)
    schema = sf.Account.describe()
    account_picklist = []
    account_schema_list = []
    try:
        for fieldDict in schema.get('fields', []):
            account_schema_list.append({f"{fieldDict.get('name')}": f"{fieldDict.get('type')}"})
            fieldType = fieldDict.get('type')
            if fieldType in ['picklist']:
                name = fieldDict.get('name')
                empty_string = []
                for fd in fieldDict['picklistValues']:
                    output = fd.get('label')
                    empty_string.append(output)
                temp2 = {change_case(f"{fieldDict.get('name')}"): {'data_type': fieldDict.get('type'), 'value': empty_string}}
                account_picklist.append(temp2)

    except Exception as e:
        print(f"Account: Failed due to {e}")

    return json.dumps({
        "picklist": account_picklist,
        "schema": reduce(lambda x, y: dict(x, **y), account_schema_list),
    })
