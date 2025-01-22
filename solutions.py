import os
from psycopg2 import DatabaseError, OperationalError, connect

# Initialize connection to None
conn = None

try:
    conn = connect(
        dbname="postgres",
        user="postgres",
        host="localhost",
        password=os.getenv("DB_PASSWORD"),
    )
    print("Database is connected Bitches!")

    cursor = conn.cursor()
    creat_table_query = """
    CREATE TABLE IF NOT EXISTS python_users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
    cursor.execute(creat_table_query)
    conn.commit()
    print("Table Python Users created")
    cursor.close()
    
except OperationalError as e1:
        print(f"Error connecting to the database: {e1}")
except DatabaseError as e2:
    if conn: # just in case: we dont want a crash system error
    conn.rollback()
    print(e2)
finally:
    if conn:
        conn.close()
        print("connection is closed")