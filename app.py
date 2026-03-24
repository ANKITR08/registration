from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

# ✅ Connect to PostgreSQL safely
def get_db_connection():
    db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        print("❌ DATABASE_URL not found")
        return None

    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        return conn
    except Exception as e:
        print("DB Connection Error:", e)
        return None


# ✅ Create table ONLY when needed (not at startup crash)
def create_table():
    conn = get_db_connection()

    if conn is None:
        print("⚠️ Skipping table creation (DB not connected)")
        return

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


# ✅ Home page
@app.route("/")
def home():
    create_table()   # moved here (SAFE)
    return render_template("index.html")


# ✅ Register route
@app.route("/register", methods=["POST"])
def register():
    conn = get_db_connection()

    if conn is None:
        return "Database not connected"

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registrations (name, email, phone, college, event) VALUES (%s, %s, %s, %s, %s)",
        (
            request.form["name"],
            request.form["email"],
            request.form["phone"],
            request.form["college"],
            request.form["event"],
        ),
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect("/")


# ✅ View data
@app.route("/data")
def view_data():
    conn = get_db_connection()

    if conn is None:
        return "Database not connected"

    cur = conn.cursor()
    cur.execute("SELECT * FROM registrations")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return render_template("data.html", data=rows)


# ✅ Required for local only (Render uses gunicorn)
if __name__ == "__main__":
    app.run()
