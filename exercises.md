### **Exercise 1: Connect to PostgreSQL**

1. Install `psycopg2` if you haven't:

   ```bash
   pip install psycopg2
   ```

2. Create a Python script that connects to a PostgreSQL database:
   - Print "Connection successful" if the connection works.

---

### **Exercise 2: Create a Table**

Create a table `users` with the following schema using Python:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### **Exercise 3: Insert Data**
1. Create a function `insert_user(username, email)` that:

   - Connects to the database.
   - Inserts a new user.
   - Prints "User added successfully."

2. Test the function with:
   ```python
   insert_user("john_doe", "john@example.com")
   insert_user("jane_doe", "jane@example.com")
   ```

---

### **Exercise 4: Query Data**

1. Write a function `get_all_users()` that:
   - Retrieves all users from the `users` table.
   - Prints each user record.

---

### **Exercise 5: Use Environment Variables**


1. Use the `dotenv` package:

   ```bash
   pip install python-dotenv
   ```

2. Create a `.env` file with:

   ```
   DB_NAME=your_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   ```

3. Modify the connection function to use environment variables.

---


### **Exercise 6: Error Handling**
**Goal:** Add exception handling.
Update all previous functions to:
   - Catch database connection or query execution errors.
   - Print appropriate error messages.


### **Exercise 7: Convertings tasks.json into postgres**
Try to convert all the endpoints in your todolist-assignment into using postgres instead. You will have to create the necessary tables by yourself.

For this exercise it is fine to open and close a new connection on each request. If you want to eliminate that overhead you can look into connection pooling. https://en.wikipedia.org/wiki/Connection_pool

Advanced example with connection pooling.
```python
from flask import Flask, g # g is a global storage that can be used in the entire request in Flask.
from psycopg2 import pool


app = Flask(__name__)

# Initialize the connection pool globally
db_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    dbname="todo_db",
    user="your_username",
    password="your_password",
    host="localhost",
    port="5432"
)

# Open a connection from the pool
# Before each request a new connection is now accesible via g.db
@app.before_request
def get_db_connection():
    g.db = db_pool.getconn()

# Release the connection back to the pool
# This is executed after the response has been sent to the user.
# This will be executed even if there was an exception with the request.
@app.teardown_request
def release_db_connection(exception):
    if hasattr(g, 'db'):
        db_pool.putconn(g.db)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with g.db.cursor() as cur:
        cur.execute("SELECT * FROM tasks")
        tasks = cur.fetchall()
    return {"tasks": tasks}


```


