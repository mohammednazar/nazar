from flask import Flask, request
from flask import Response
import csv
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'leads.db'


# ✅ Create DB and leads table (if not exists)
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                submitted_at TEXT NOT NULL
            )
        ''')


# ✅ Call immediately to create DB/table on app startup
init_db()


@app.route('/')
def home():
    return "<h2>Flask backend is running ✅</h2><p>Submit form data via <code>/submit</code>.</p>"


@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not name or not phone or not email or not address:
        return "<h3>Error: All fields are required.</h3>", 400

    with sqlite3.connect(DB_NAME) as conn:
        conn.execute(
            '''
            INSERT INTO leads (name, phone, email, address, submitted_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, email, address, submitted_at))

    return '''
        <h2>Thank you!</h2>
        <p>Your information has been submitted successfully.</p>
        <a href="/">Back to Home</a>
    '''


@app.route('/debug')
def debug():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
    return f"<h3>Tables in DB:</h3><pre>{tables}</pre>"


@app.route('/export', methods=['GET'])
def export_data():

    def generate():
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, phone, email, address, submitted_at FROM leads"
            )
            rows = cursor.fetchall()

            yield 'ID,Name,Phone,Email,Address,Submitted At\n'
            for row in rows:
                yield ','.join('"' + str(field).replace('"', '""') + '"'
                               for field in row) + '\n'

    return Response(
        generate(),
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=leads.csv"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
