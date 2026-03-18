from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# Connect to PostgreSQL (Render provides DATABASE_URL)
def get_db_connection():
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    return conn

# Create table
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id SERIAL PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            college TEXT,
            event TEXT
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

create_table()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Handle form submission
@app.route("/register", methods=["POST"])
def register():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    college = request.form["college"]
    event = request.form["event"]

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registrations (name, email, phone, college, event) VALUES (%s, %s, %s, %s, %s)",
        (name, email, phone, college, event)
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")

# View data in browser
@app.route("/data")
def view_data():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM registrations")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("data.html", data=rows)

if __name__ == "__main__":
    app.run()
