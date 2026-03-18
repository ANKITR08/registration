from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="yourpassword",
    database="portfolio_db"
)

cursor = conn.cursor()

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data['name']
    email = data['email']
    message = data['message']

    query = "INSERT INTO users (name, email, message) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, message))
    conn.commit()

    return jsonify({"message": "Data saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

