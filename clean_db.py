import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("DELETE FROM friend_requests")
conn.execute("DELETE FROM friends")

conn.commit()
conn.close()

print("Database cleaned")