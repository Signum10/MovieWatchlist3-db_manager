import psycopg2
import json
import pathlib

class DB:
    def __init__(self):
        current_dir = pathlib.Path(__file__).parent.resolve()
        settings_file = current_dir.joinpath('database.json')
        queries_file = current_dir.joinpath('queries.json')

        with open(settings_file) as f:
            db_args = json.load(f)

        with open(queries_file) as f:
            self.queries = json.load(f)

        self.connection = psycopg2.connect(**db_args)
        self.cursor = self.connection.cursor()
        print('Connected to PostgreSQL database')

    def execute_named_query(self, query, vars=None):
        self.cursor.execute(self.queries[query], vars)

        if vars is None:
            return self.cursor.fetchall()
        
        return None

    def commit(self):
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()
        print('Closed connection to PostgreSQL database')
