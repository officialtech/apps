"""lead schema module """

import json
from apps.salesforce.constant import lead_schema_dict

from simple_salesforce import Salesforce # client library


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
