import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, render_template_string
import psycopg2

load_dotenv()
# Flask setup
app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": os.getenv("DB_PASSWORD"),
    "host": "localhost",
    "port": "5432"
}

# Connect to the database
def get_connection():
    return psycopg2.connect(**DB_CONFIG)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")

# Vulnerable Login Route
@app.route("/login", methods=["POST"])
def login():
    message = ""
    username = request.form['username']
    password = request.form['password']
    # Vulnerable Query (String Interpolation)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print("Executing:", query)
    try:
        conn = get_connection()
        print("connect")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
        if result:
            message = "Login successful! Welcome, " + result[0]
        else:
            message = "Invalid username or password!"
    except Exception as e:
        message = f"Error: {e}"
    return {"msg": message}
    
# Vulnerable Login Route
@app.route("/login_safe", methods=["POST"])
def login_safe():
    message = ""
    username = request.form['username']
    password = request.form['password']
    # Safe query
    query = f"SELECT * FROM users WHERE username = %s AND password = %s"
    print("Executing:", query)
    try:
        conn = get_connection()
        print("connect")
        cursor = conn.cursor()
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        conn.close()
        if result:
            message = "Login successful! Welcome, " + result[0]
        else:
            message = "Invalid username or password!"
    except Exception as e:
        message = f"Error: {e}"
    return {"msg": message}
    

if __name__ == '__main__':
    app.run(debug=True)
