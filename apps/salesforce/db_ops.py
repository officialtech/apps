"""all the DB related operations will go here for SF """

from db.connection import MySqlConnection, SqlAlchemyConnection
from utils.genric import read_file


def connect(engine="sql"):
    """return engine type sql connection object """

    if engine == "sqlalchemy":
        return SqlAlchemyConnection()
    
    return MySqlConnection()



def save_profile():
    """save user profile to DB """
    pass


def save_users_data(data, ):
    """save users data to DB """
    cnx = connect(engine="sqlalchemy")
    # cur = cnx.cursor()

    query = read_file(file="apps/salesforce/sql/insert_user", extention="sql")
    data_list = [tuple(_data.values()) for _data in data]

    # cur.executemany(query, data_list)
    # cnx.commit()
    # cnx.close()
    return True