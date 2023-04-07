import psycopg2
import json

class DB:
    def __init__(self, db_settings_json_file):
        with open(db_settings_json_file) as f:
            db_args = json.load(f)

        self.connection = psycopg2.connect(**db_args)
        self.cursor = self.connection.cursor()
        print('Connected to PostgreSQL database')

    def query(self, q):
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print('Closed connection to PostgreSQL database')
