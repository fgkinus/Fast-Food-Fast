import os

import psycopg2

URL = os.getenv('DATABASE_URL')
queries = os.path.abspath(os.path.dirname(__file__))
print(URL)
connection = psycopg2.connect(URL)
