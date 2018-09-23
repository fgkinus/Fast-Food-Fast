"""initialise the central  DB to be used"""
from app.V2.Database import Database
from app.V2.queries import connection

DB = Database(conn=connection).init_db()
