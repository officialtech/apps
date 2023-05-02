"""contact schema module """

import json
from functools import reduce

from apps.salesforce.constant import contact_schema_dict
from simple_salesforce import Salesforce
from utils.genric import change_case
from apps.salesforce.db_ops import connect


def contact_schema():
    """return json type of contact schema """
    return json.dumps({
        "conatact_schema": contact_schema_dict,
    })


def fetch_sf_contact_schema(instance_url, access_id, user_id, *args, **kwargs, ):
    """fetching sf schema for contact """
    try:
        sf = Salesforce(instance_url=instance_url, session_id=access_id)
        schema = sf.Contact.describe()
    except Exception as ex:
        print(ex)
        
        cnx = connect(engine="mysql")
        cur = cnx.cursor()
        query = f"""SELECT salesforce from `company_integrations` WHERE user_id={user_id}"""
        cur.execute(query)
        salesforce_tuple = cur.fetchall()
        if salesforce_tuple:
            from main_handler import regenerate_tokens
            _response = regenerate_tokens(salesforce_tuple[0][0]) # start work from here
            access_id = _response.get("data").get("refresh_token")
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


