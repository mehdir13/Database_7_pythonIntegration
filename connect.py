from dotenv import load_dotenv
from psycopg2 import DatabaseError, OperationalError, connect
import os
load_dotenv()
conn = None
try:
    # Connects to the database
    conn = connect(
        dbname="postgres",
        user="postgres",
        host="localhost",
        # Fetches from the .env-file. It is bad practice to have the db password lying around in a repo.
        password=os.getenv("DB_PASSWORD"),
    )
    print("Database is connected Bitches!")
    # Create a cursor which goes from row to row fetching all values.
    # In large datasets fetching everything without a cursor is not feasible.
    cursor = conn.cursor()
    # Executes an SQL-statement. Could be an INSERT.
    cursor.execute("SELECT * FROM employees;")
    #print(cursor.fetchall()) # We can now fetch all the rows. In larger datasets this may have to be fetched in chunks with .fetchone() or .fetchmany(n)

    # We now run an INSERT command.
    cursor.execute("INSERT INTO categories (category_id, category_name, description) VALUES (9, 'Frozen food', 'Frozen food')")
    # We actually need to commit to make something happen. Otherwise the updates are just queued up but never committed.
    conn.commit()
    cursor.close() # Closes the cursor
except OperationalError as e:
        print(f"Error connecting to the database: {e}")
except DatabaseError as error:
    # Prints and error if we for example enter a duplicate primary key or violate other constraints.
    conn.rollback() # If something goes wrong, all pending commits are cleared from memory.
    print(error)
finally:
    if conn is not None:
        conn.close()

    
"""
1. connect
2. cursor
3. cursor.fetchall()
4. try-except, stänga connection.
5. .env load_dotenv(), python-dotenv, os.getenv
6. commit()
"""
