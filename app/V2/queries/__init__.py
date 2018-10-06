import os

import psycopg2
from dotenv import load_dotenv  # import the environment files
from flask_restplus import abort
from psycopg2._psycopg import Error

load_dotenv(verbose=True)
URL = os.getenv('DATABASE_URL')
queries = os.path.abspath(os.path.dirname(__file__))

try:
    connection = psycopg2.connect(URL)
except Error as e:
    raise e
