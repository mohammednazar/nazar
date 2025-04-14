
from flask import Flask, request
from flask import Response
import csv
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Ensure DB is always created in the same directory as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'leads.db')

# Create DB and table if not already present
def init_db():
    if not os.path.exists(DB_NAME):
        print("Creating DB...")
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute('''
                CREATE TABLE leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    address TEXT NOT NULL,
                    submitted_at TEXT NOT NULL
                )
            ''')
        print("DB created successfully.")
    else:
        print("DB already exists.")


@app.route('/')
def home():
    return "<h2>Flask Backend is Running</h2><p>Submit form data via /submit</p>"

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not name or not phone or not email or not address:
        return '''
            <h2>Submission Error</h2>
            <p>All fields are required. Please go back and try again.</p>
        ''', 400

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            INSERT INTO leads (name, phone, email, address, submitted_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, email, address, timestamp))

    return '''
        <h2>Thank you!</h2>
        <p>Your information has been submitted successfully.</p>
        <a href="/">Go back</a>
    '''

@app.route('/export', methods=['GET'])
def export_data():
    def generate():
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, phone, email, address, submitted_at FROM leads")
            rows = cursor.fetchall()

            yield 'ID,Name,Phone,Email,Address,Submitted At\n'
            for row in rows:
                yield ','.join('"' + str(field).replace('"', '""') + '"' for field in row) + '\n'

    return Response(generate(), mimetype='text/csv', headers={
        "Content-Disposition": "attachment;filename=leads.csv"
    })


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
