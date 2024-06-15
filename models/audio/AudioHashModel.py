from db import get_connection
from typing import List, Tuple
class AudioHash:
  def __init__(self):
    pass

  @classmethod
  def create_table(cls):
    conn = get_connection()
    sql = """
    CREATE TABLE IF NOT EXISTS audio_hash (
        id serial PRIMARY KEY,
        key TEXT NOT NULL,
        minhash TEXT NOT NULL,
        name TEXT NOT NULL,
        frame INTEGER NOT NULL  
      )
    """
    conn.cursor().execute(sql)
    conn.commit()
  
  def insertMany(self, data):
    conn = get_connection()
    sql = "INSERT INTO audio_hash (id, key, minhash, name, frame) VALUES (DEFAULT, %s, %s, %s, %s)"
    conn.cursor().executemany(sql, data)
    conn.commit()
    
  def getMinHash(self, band)->List[Tuple[str,str,str,int]]:
    conn = get_connection()
    sql = """
    SELECT key, minhash, name, frame FROM audio_hash WHERE key in (%s)
    """
    cur = conn.cursor()
    cur.execute(sql, (band,))
    minhash = cur.fetchall()
    cur.close()
    conn.close()
    return minhash