import logging

import psycopg2
from flask_restplus import abort
from psycopg2.extras import RealDictCursor

from app.V2.queries import queries, os
from instance.logging import Logging


class Database(object):
    """A class to hold all database methods and classes"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        # set up the logger
        self.logger = Logging().get_logger("Database")

    def init_db(self):
        """initialize the db with all its tables"""
        init_queries = self.query_file_reader('creation_script.sql')
        self.run_queries(init_queries)
        self.logger.info("The database tables have been successfully initialised")

    def set_cursor(self):
        self.close_cursor()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        return self.cursor

    def close_cursor(self):
        if isinstance(self.cursor, psycopg2.extensions.cursor):
            self.cursor.close()

    @staticmethod
    def query_file_reader(filename):
        path = os.path.join(queries, filename)
        # try to read the sql file
        try:
            fd = open(path, 'r')
        except FileNotFoundError:
            abort(500, "Error reading database files")

        #  now read the file
        sql_file = fd.read()
        fd.close()

        # split all sql commands by ;
        sql_file = sql_file.replace('\n', ' ')
        sql_commands = sql_file.split(';')
        return sql_commands

    def run_queries(self, query):
        # cur = self.set_cursor()
        for command in query:
            self.query_db(query=command)

    def query_db(self, query):
        """
        a custom function to run any valid SQL query provided a connection object is provided.
        If a transaction fails , its rolled back and cursors are not blocked
        :param query:
        :return result:
        """
        conn = self.conn
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute(query)
                    self.logger.debug("query successful: {0}".format(query))
                except psycopg2.DatabaseError as er:
                    logging.debug("error {0} executing query {1}".format(er, query))
