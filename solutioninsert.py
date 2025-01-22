import os
from psycopg2 import connect, OperationalError, DatabaseError

# Initialize connection to None
conn = None

try:
    # Establish a connection to the database
    conn = connect(
        dbname="postgres",
        user="postgres",
        host="localhost",
        password=os.getenv("DB_PASSWORD"),
    )
    print("Database connection established!")

    # Create a cursor to execute SQL commands
    cursor = conn.cursor()

    # Insert data into the table
    insert_query = """
    INSERT INTO python_users (username, email)
    VALUES (%s, %s)
    RETURNING id;  -- Return the ID of the inserted row
    """
    user_data = ("john_doe", "john.doe@example.com")
    cursor.execute(insert_query, user_data)

    # Fetch the ID of the inserted row
    user_id = cursor.fetchone()[0]
    print(f"Data inserted successfully with ID: {user_id}")

    # Commit the transaction
    conn.commit()

    # Close the cursor
    cursor.close()

except OperationalError as e1:
    print(f"Error connecting to the database: {e1}")
except DatabaseError as e2:
    if conn:
        conn.rollback()  # Rollback transaction in case of errors
    print(f"Database error occurred: {e2}")
finally:
    # Ensure the connection is closed
    if conn:
        conn.close()
        print("Database connection closed.")
