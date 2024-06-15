
import psycopg2

def get_connection():
  conn = psycopg2.connect(
    database="workpi",
    host="localhost",
    user="admin",
    password="admin",
    port="5432"
  )
  return conn