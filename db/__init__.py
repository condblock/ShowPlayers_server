import sqlite3

conn = sqlite3.connect('players.db', check_same_thread=False)
cur = conn.cursor()

sql = '''CREATE TABLE players (id integer not null primary key autoincrement,
                               name text not null, 
                               school text not null, 
                               startTime text not null)'''

# create table
try:
    cur.execute(sql)
except:
    pass