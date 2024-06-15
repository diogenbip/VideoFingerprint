from db import get_connection
class VideoHash:
  def __init__(self):
    pass

  @classmethod
  def create_table(cls):
    conn = get_connection()
    sql = """
    CREATE TABLE IF NOT EXISTS video_hash (
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
    sql = "INSERT INTO video_hash (id, key, minhash, name, frame) VALUES (DEFAULT, %s, %s, %s, %s)"
    conn.cursor().executemany(sql, data)
    conn.commit()