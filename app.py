from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from dotenv import load_dotenv
from models import init_db

load_dotenv()

app = Flask(__name__)
DB_NAME = "database.db"

# Initialize the database immediately (Flask 3+ compatible)
with app.app_context():
    init_db(DB_NAME)

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    conn.close()

    total_income = sum(t[2] for t in transactions if t[3] == 'income')
    total_expense = sum(t[2] for t in transactions if t[3] == 'expense')
    balance = total_income - total_expense

    return render_template('index.html', transactions=transactions, balance=balance,
                           total_income=total_income, total_expense=total_expense)

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        name = request.form['name']
        if not name:
            return "Missing 'name' field in form", 400
        amount = float(request.form['amount'])
        t_type = request.form['type']
        date = request.form['date']

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions (name, amount, type, date) VALUES (?, ?, ?, ?)",
                       (name, amount, t_type, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_transaction.html')
if __name__ == '__main__':
    app.run(debug=True)