"""Represents a single User on the default opportunity team of another User """

import json
import requests
from simple_salesforce import Salesforce
from apps.salesforce.db_ops import save_users_data


def fetch_user_team_member(instance_url, access_token, ):
    """fetching user team members data """

    sf = Salesforce(instance_url=instance_url, session_id=access_token, )
    uteamember = sf.query(
        "SELECT Ownerid, owner.name, Userid, User.name, opportunityaccesslevel, teammemberrole  FROM UserTeamMember"
    )

    team_member = [
        {
            "lead_id": lead["Ownerid"],
            "first_name": lead["FirstName"],
            "last_name": lead["LastName"],
            "company": lead["Company"],
            "email": lead["Email"],
        }
        for lead in uteamember['records']
    ]

    return json.dumps({
        "data": team_member,
    })


def fetch_sf_users(instance_url, session_id, ):
    """
    fetch salesforce users data
    first trying fetching using client library
    after that if it's not worked, fetching data
    using rest API
    """

    try:
        sf = Salesforce(instance_url=instance_url, session_id=session_id, )
        users_data = sf.query(
            "SELECT Id, Name, Email, IsActive, UserType from User"
        )

        users = [
            {
                'id': objects['Id'],
                'name': objects['Name'],
                'email': objects['Email'],
                'is_active': objects['IsActive'],
                'user_type': objects['UserType'],
            }
            for objects in users_data['records']
        ]

        # save_users_data(data=users, )

        return json.dumps({
            "users": users,
        })

    except Exception as sfer:
        print(f"exception occured: {sfer}")

        try:
            url = "https://cifoundation.my.salesforce.com/services/data/v57.0/chatter/users"
            payload={}
            headers = {
                'Authorization': f'Bearer {session_id}',
            }
            response = requests.request("GET", url, headers=headers, data=payload, timeout=10)
            print(response.text)
            users_rest_data = [
                {
                    'id': _users['id'],
                    'name': _users['name'],
                    'email': _users['email'],
                    'is_active': _users['isActive'],
                    'user_type': _users['userType'],
                }
                for _users in response.json().get("users")
            ]

            # save_users_data(data=users, )

            return json.dumps({
                "users": users_rest_data,
            })

        except Exception as ex:
            print(f"exception in except block: {ex}")
            pass