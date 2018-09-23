import logging
import subprocess

import connection_url
import psycopg2
from flask_restplus import abort
from psycopg2.extras import RealDictCursor

from app.Exceptions import StoredProcedureError
from app.V2.queries import queries, os, URL
from instance.logging import Logging


class Database(object):
    """A class to hold all database methods and classes"""

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        # set up the logger
        self.logger = Logging().get_logger(__name__)

    def init_db(self):
        """initialize the db with all its tables"""
        init_queries = self.query_file_reader('creation_script.sql')
        self.run_queries(init_queries)
        self.run_shell_script('procedures.sql')

        self.logger.info("The database tables have been successfully initialised")
        return self

    def set_cursor(self):
        self.close_cursor()
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        return self.cursor

    def close_cursor(self):
        if isinstance(self.cursor, psycopg2.extensions.cursor):
            self.cursor.close()

    def query_file_reader(self, filename):
        path = os.path.join(queries, filename)
        # try to read the sql file
        try:
            fd = open(path, 'r')
        except FileNotFoundError:
            self.logger.error("could not read query file {0}".format(filename))
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
            if len(command):
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
                    self.logger.info("query successful: {0}".format(query))
                except psycopg2.DatabaseError as er:
                    logging.error("error --{0}-- executing query --{1}--".format(er, query))

    def query_db_with_results(self, query):
        """
        a custom function to run any valid SQL query provided a connection object is provided.
        If a transaction fails , its rolled back and cursors are not blocked.
        The function returns a a result set that is formatted as a dict
        :param query:
        :return result:
        """
        conn = self.conn
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                try:
                    cur.execute(query)
                    self.logger.info("query successful: {0}".format(query))
                except psycopg2.DatabaseError as er:
                    logging.error("error --{0}-- while executing command --{1}--".format(er, query))
                    abort(500, "Sorry, your request could not processed. Please contact the admin for assistance")
                try:
                    result = cur.fetchall()
                    return result
                except:
                    logging.error("could not fetch the result set")

    def execute_procedures(self, procedure, params=()):
        """
        a function to execute stored procedures
        :return result set:
        """
        self.set_cursor()
        try:
            self.cursor.callproc(procedure, params)
            result = self.cursor.fetchall()
            self.logger.info("procedure successfully called:{0}".format(procedure))
            return result
        except StoredProcedureError:
            self.logger.error("procedure call failed : {0}".format(procedure))

    def run_shell_script(self, file):
        """
        run an sql script from the console
        :param file:
        :return None:
        """
        path = os.path.join(queries, file)
        url = connection_url.config(URL)
        self.logger.info("Initialising file execution...")
        script = ['psql', '-h', url['HOST'], '-U', url['USER'], '-d', url['NAME'], '-p', str(url['PORT']), '-f', path]
        self.logger.debug(''.join(script))
        subprocess.call(script, shell=True)
        self.logger.info("The procedures have been setup")
