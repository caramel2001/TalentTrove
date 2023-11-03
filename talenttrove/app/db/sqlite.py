# write a class to create a Sqlite DB 
# and insert data into it
import sqlite3
from talenttrove.app.config.config import settings
from pathlib import Path
class Database:
    def __init__(self, db_name=settings["DB_PATH"]):
        self.db_name = db_name
        self.create_db_file()
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        # columns is a list of tuples, where each tuple is (column_name, column_type)
        # e.g. columns = [('id', 'INTEGER PRIMARY KEY'), ('name', 'TEXT')]
        # create a table with the given name and columns
        # if the table already exists, this will fail
        pass

    def create_db_file(self):
        # create a new database file
        # if the DB file already exists, then dont create
        if not Path(self.db_name).exists():
            print('x')
            Path(self.db_name).touch()
