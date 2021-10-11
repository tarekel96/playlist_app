# module defines operations to use with sqlite3 database
import sqlite3
from sqlite3.dbapi2 import OperationalError


class db_operations():
    def __init__(self,conn_path): # constructor with connection path to db
        self.isConnected = False
        while self.isConnected == False:
            try:
                self.connection = sqlite3.connect(conn_path)
                self.cursor = self.connection.cursor()
                print("Connection made..")
                self.isConnected = True
            except OperationalError as e:
                print(f"Error: Unable to connect to {conn_path}.\nPlease re-renter the DB path, include the db file in the path. ")
                conn_path = input("Path: ")
                continue
        self.table_exists(table_name="songs", create_table=True)
    
    # Check if the songs table is made or not
    def table_exists(self, table_name = "songs", create_table = True):
        query = '''
        SELECT count(name) FROM sqlite_master WHERE type='table' AND name=:table_name 
        '''
        dictionary = {"table_name": table_name}
        #get the count of tables with the name
        self.cursor.execute(query, dictionary)
        res = self.cursor.fetchone()[0]
        if res == 0:
            print(f"A table with the name {table_name} does not exist.")
            if create_table == True:
                self.create_table(table_name)
        if res == 1:
            print(f"A table with the name {table_name} exists.")
    
    def create_table(self, table_name = "songs"):
        print(f"Creating {table_name} table...")
        query = f'''
        CREATE TABLE {table_name}(
        songID VARCHAR(22) NOT NULL PRIMARY KEY,
        Name VARCHAR(20),
        Artist VARCHAR(20),
        Album VARCHAR(20),
        releaseDate DATETIME,
        Genre VARCHAR(20),
        Explicit BOOLEAN,
        Duration DOUBLE,
        Energy DOUBLE,
        Danceability DOUBLE,
        Acousticness DOUBLE,
        Liveness DOUBLE,
        Loudness DOUBLE
        ); 
        '''
        dictionary = {"table_name": table_name}
        self.cursor.execute(query, dictionary)
        print(f"{table_name} table successfully made.")

    # function for bulk inserting records
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        self.connection.commit()
        print("query executed..")

    def update_records(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()
        print("update successfully processed...")

    # function to return a single value from table
    def single_record(self,query):
        self.cursor.execute(query)
        # cusor will return a tuple, the index 0 is because we know it should only be one value (count)
        return self.cursor.fetchone()[0]

    # function to return a single row based on the options from the dictionary
    def single_record_options(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchall()[0]
    
        # function to return all rows based on the options from the dictionary
    def get_records_options(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchall()
    
    def get_record_col_names(self, query, dictionary={}):
        self.cursor.execute(query, dictionary)
        # Get col names from description tuples
        return [description[0] for description in self.cursor.description]

    # function to return a single attribute values from table
    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        if None in results:
            results.remove(None)
        return results

    # SELECT with named placeholders
    def name_placeholder_query(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # close connection 
    def destructor(self):
        self.connection.close()


