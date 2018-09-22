"""test database interaction and initialisation methods"""
import pytest
from werkzeug.exceptions import InternalServerError

from app.V2.Database import Database
from app.V2.queries import connection

DB = Database(connection)


class TestDatabases(object):
    """Test cases for the database"""

    def test_query_file_reader(self):
        """test method for reading the script files"""
        file_name = 'creation_script.sql'
        queries = DB.query_file_reader(filename=file_name)
        assert isinstance(queries, list)
        with pytest.raises(InternalServerError, message="Error reading database files"):
            queries = DB.query_file_reader("unknown.sql")

    def test_db_initialisation(self):
        DB.init_db()
        query = "select table_name from information_schema.tables where table_schema = 'public'"
        result = DB.query_db_with_results(query)
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert 'table_name' in result[0]
