from psycopg2 import pool
import os
from contextlib import contextmanager

# Load environment variables or use a configuration module
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize connection pool
connection_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dsn=DATABASE_URL
)

# Context manager to get and release connections
@contextmanager
def get_db_connection():
    connection = connection_pool.getconn()
    try:
        yield connection
    finally:
        connection_pool.putconn(connection)

# Shutdown function to close the pool
def close_connection_pool():
    connection_pool.closeall()
