import os

import psycopg2

URL = os.getenv('DATABASE_URL')
queries = os.path.abspath(os.path.dirname(__file__))
connection = psycopg2.connect(dsn=URL, user='postgres')
