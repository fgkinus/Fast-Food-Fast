import os

import psycopg2
from dotenv import load_dotenv  # import the environment files

load_dotenv(verbose=True)
URL = os.getenv('DATABASE_URL')
queries = os.path.abspath(os.path.dirname(__file__))
connection = psycopg2.connect(URL)
