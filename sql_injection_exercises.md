## **SQL Injection Exercises**

### **Prerequisites:**

1. A PostgreSQL database with a `users` table:

   ```sql
   CREATE TABLE users (
       username TEXT PRIMARY KEY,
       password TEXT NOT NULL
   );

   INSERT INTO users (username, password)
   VALUES ('admin', 'admin123'), ('user1', 'pass1');
   ```
2. A flask API with a frontend which has two input fields, one for username and one for login. The form should point to /login route. 
---

### **Exercise 1: Simulate SQL Injection**

1. Create a vulnerable login function within your /login route:

   ```python
   def vulnerable_login(username, password):
       conn = psycopg2.connect(
           dbname="test_db",
           user="your_user",
           password="your_password",
           host="localhost"
       )
       cur = conn.cursor()

       query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
       cur.execute(query)
       result = cur.fetchone()

       if result:
           return {"message": "Login successful"}
       else:
           return {"message": "Login failed"}
   ```

2. Test the function for normal usage. Try with correct user and password combinations, then try with incorrect ones.

3. Test out your login with SQL injection. The goal is to gain access without typing in a correct username and password.

4. Fix your security issues.

5. Another common vulnerability is Command Injection or XSS. Command Injection is when the hacker tries to inject code through your unsanitized inputs. They might for example try to enter `os.system('shutdown -s')` in the login field in hopes of turning the host system off. Right now, there are no known vulnerabilities in flask or psycopg2 that allow the user to inject commands, but that may change in the future. Your task is therefore to *validate* the incoming input and making sure the username only consists of alpha-numeric letters.

6. Add a try-except block to your application. If some unknown bug exists in the software a user may expose the stacktrace. This may expose folder names, source code or at worst: environment variables. A try-except makes sure that an error is logged internally and the user is exposed to a generic error like "Oops! Something went wrong, please try again!"
---

### **Exercise 2: Security Review**


1. Review this login flow:

   ```python

    def insecure_login_flow(username, password):
        conn = psycopg2.connect(
            dbname="test_db",
            user="your_user",
            password="your_password",
            host="localhost"
        )
        cur = conn.cursor()

        # Step 1: Check if username exists
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if not user:
            return {"message": "Username not found"}

        # Step 2: Check if password matches
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )
        result = cur.fetchone()

        if result:
            return {"message": "Login successful"}
        else:
            return {"message": "Incorrect password"}

   ```

2. Try to identify **three** security vulnerabilities.
