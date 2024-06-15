import os
from flask import Flask, render_template
import psycopg2
app = Flask(__name__)

def get_connection():
  conn = psycopg2.connect(
    database="workpi",
    host="localhost",
    user="admin",
    password="admin",
    port="5432"
  )
  return conn

@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)