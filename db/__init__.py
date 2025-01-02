import sqlite3

conn = sqlite3.connect('players.db', check_same_thread=False)
cur = conn.cursor()

sql = '''CREATE TABLE IF NOT EXISTS players (
             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL, 
             school TEXT NOT NULL, 
             startTime TEXT NOT NULL,
             endTime TEXT NOT NULL,
             ip_address TEXT NOT NULL)'''

# create table
try:
    cur.execute(sql)
except Exception as e:
    print(f"An error occurred: {e}")

conn.commit()
