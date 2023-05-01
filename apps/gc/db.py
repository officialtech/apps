"""all the ops related to DB """
import mysql.connector
from decouple import config
from mysql.connector import errorcode


config_setting = {
  'user': config('DB_USER'),
  'password': config('DB_PASSWORD'),
  'host': config('DB_HOST'),
  'database': config('DB_NAME'),
  'port': config("DB_PORT", default=3306),
  'raise_on_warnings': True,
}

def connect():
    """connect to DB """
    cnx = "check error for console"
    try:
        print(config_setting)
        cnx = mysql.connector.connect(**config_setting)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()
    return cnx

    