"""this module is responsible for make connection to DB """

from urllib.parse import quote_plus 
from decouple import config

import mysql.connector as mysql
from mysql.connector import errorcode

from sqlalchemy import create_engine


credentials = {
  'user': config("DB_USER"),
  'port': config("DB_PORT"),
  'password': config("DB_PASSWORD"),
  'host': config("DB_HOST"),
  'database': config("DB_NAME"),
  'raise_on_warnings': True
}

class MySqlConnection():
    """
    make mysql connection and many sql related operations
    How to use:
        variablename = classname(credentials)
    """

    def __init__(self, credentials=credentials, ):
        """
        constructor method that is called when an object of the class is created
        """
        try:
            self.con = mysql.connect(**credentials)
            print("DB connection establaised... ")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")

            else:
                print(err)


    def __del__(self, ):
        """
        method is called when an object is about to be destroyed
        and its resources are being released
        """
        self.con.close()
        print("Object destroyed!")

        
    def close(self, ):
        """manually closing the connection """
        self.con.close()
        print("Closing connection... ")
        return True
    
    def cursor(self, ):
        print("creating cursor...")
        return self.con.cursor()
        

class SqlAlchemyConnection():
    """
    Establishing Connectivity - the Engine, Every SQLAlchemy
    application that connects to a database needs to use an `Engine`
    """

    def __init__(self, credentials=credentials, ) -> None:
        self.engine = create_engine(
            f"mysql+mysqldb://{credentials.get('user')}:{credentials.get('password')}@{credentials.get('host')}/{credentials.get('database')}",
            pool_recycle=3600,
            echo=True
        )