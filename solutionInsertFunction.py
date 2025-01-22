import os
from psycopg2 import connect, DatabaseError, OperationalError

def insert_user(username, email):
    conn = None
    try:
        conn = connect(
            dbname="postgres",
            user="postgres",
            host="localhost",
            password=os.getenv("DB_PASSWORD"),
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO python_users (username, email)
        VALUES (%s, %s);
        """
 #Parameterized Query (%s):
 # Prevents SQL injection by separating query logic from user input.
 
        cursor.execute(insert_query, (username, email))
        conn.commit()
        print("User added successfully.")
        cursor.close()

    except OperationalError as e1:
        print(f"Error connecting to the database: {e1}")
    except DatabaseError as e2:
        if conn:
            conn.rollback()  # Rollback in case of database errors
        print(f"Database error occurred: {e2}")
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

insert_user("jane_doe", "jane.doe@example.com")




import os
from psycopg2 import connect, DatabaseError, OperationalError

def get_all_users():
    """
    Retrieves all users from the python_users table and prints each user record.
    """
    conn = None
    try:
        # Establish connection to the database
        conn = connect(
            dbname="postgres",
            user="postgres",
            host="localhost",
            password=os.getenv("DB_PASSWORD", "default_password"),  # Fallback for dev
        )
        cursor = conn.cursor()

        # Query to fetch all users
        fetch_query = "SELECT * FROM python_users;"
        cursor.execute(fetch_query)

        # Retrieve all rows from the result
        users = cursor.fetchall()

        # Check if there are users and print each record
        if users:
            print("User Records:")
            for user in users:
                print(user)
        else:
            print("No users found in the database.")

        # Close the cursor
        cursor.close()

    except OperationalError as e1:
        print(f"Error connecting to the database: {e1}")
    except DatabaseError as e2:
        if conn:
            conn.rollback()  # Rollback in case of database errors
        print(f"Database error occurred: {e2}")
    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

# Example usage
get_all_users()
