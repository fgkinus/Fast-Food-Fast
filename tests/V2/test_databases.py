"""test database interaction and initialisation methods"""
import pytest
from werkzeug.exceptions import InternalServerError

from app.V2.Database import Database
from app.V2.queries import connection

print(connection)
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

    def test_query_file_reader(self):
        with pytest.raises(InternalServerError):
            DB.query_file_reader('unknown.sql')

    def test_query_db_with_results(self):
        query = """SELECT * FROM tbl_users"""
        res = DB.query_db_with_results(query)
        assert isinstance(res, list)
        assert isinstance(res[0], dict)

        query = """SELECT * FROM tbl_unknown"""
        with pytest.raises(InternalServerError):
            res = DB.query_db_with_results(query)

    def test_query_db_with_results_no_results(self):
        query = """INSERT INTO tbl_ref_status(description) VALUES ('status') ON CONFLICT (description) DO NOTHING """
        res = DB.query_db_with_results(query)
        assert not isinstance(res, list)


