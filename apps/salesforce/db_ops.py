"""all the DB related operations will go here for SF """

from db.connection import MySqlConnection


def connect():
    """return sql object """
    return MySqlConnection()



def save_profile():
    """save user profile to DB """
    pass