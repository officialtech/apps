"""all the DB related operations will go here for SF """

from db.connection import MySqlConnection, SqlAlchemyConnection
from utils.genric import read_file


def connect(engine="mysql"):
    """return engine type sql connection object """

    if engine == "sqlalchemy":
        return SqlAlchemyConnection()
    
    return MySqlConnection()



def save_profile(access_token, user_id, name, email, is_active, platform_id, ):
    """save user profile to DB """


    cnx = connect(engine="mysql")
    cur = cnx.cursor()

    query = read_file(file="apps/salesforce/sql/insert_profile", extention="sql")
    query.format(
        access_token=access_token, user_id=user_id,
        name=name, email=email, is_active=is_active,
        platform_id=platform_id,
    )

    cur.execute(query)
    cnx.commit()
    cnx.close()
    return True


def save_users_data(data, ):
    """save users data to DB """
    cnx = connect(engine="mysql")
    cur = cnx.cursor()

    query = read_file(file="apps/salesforce/sql/insert_user", extention="sql")
    data_list = [tuple(_data.values()) for _data in data]

    cur.executemany(query, data_list)
    cnx.commit()
    cnx.close()
    return True


def save_refresh_token(response_data):
    """save user id and refresh token to DB """
    try:
        cnx = connect(engine="mysql")
        cur = cnx.cursor()

        query = f"""INSERT INTO `company_integrations` (salesforce) VALUES ({response_data!r}) """
        cur.execute(query)

        cnx.commit()
        cnx.close()

        return True
    
    except Exception as ex:
        print("Just check above query and change TABLE structure in your DB")
        print(ex)
        return