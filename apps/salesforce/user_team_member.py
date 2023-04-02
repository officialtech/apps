"""Represents a single User on the default opportunity team of another User """

from simple_salesforce import Salesforce



def fetch_user_team_member(instance_url, access_token, ):
    """fetching user team member """

    sf = Salesforce(instance_url=instance_url, session_id=access_token)
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
