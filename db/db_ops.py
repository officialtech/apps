
import pandas as pd

def insert_on_duplicate(self, table, conn, keys, data_iter):
    """
    :Title: Function to update the fields if duplicate key finds
    :param table: Contains target table_name to push the data.
    :param conn: Database connection to execute queries.
    :param keys: fields of table for the data is going to insert
    :param data_iter: data values of fields that need to be stored.
    :return: None
    """
    insert_stmt = insert(table.table).values(list(data_iter))
    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(insert_stmt.inserted)
    conn.execute(on_duplicate_key_stmt)


def store_to_database(self, table: str, data: pd.DataFrame) -> None:
    """store to DB """
    print(table)
    list(data.columns)
    print("SQL ALCHEMY CONNECTION: ", self.db_con)
    try:

        data.to_sql(table, con=self.db_con, if_exists='append', chunksize=4096, index=False, method=self.insert_on_duplicate)
        return "successfully", 200
    except Exception as e:
        print(e)
        return "failed", 401

