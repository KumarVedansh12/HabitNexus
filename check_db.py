# import sqlite3

# conn = sqlite3.connect("database.db")

# print("\nUSERS")
# for row in conn.execute("SELECT * FROM users"):
#     print(row)

# print("\nFRIEND REQUESTS")
# for row in conn.execute("SELECT * FROM friend_requests"):
#     print(row)

# print("\nFRIENDS")
# for row in conn.execute("SELECT * FROM friends"):
#     print(row)

# conn.close()

import sqlite3

conn = sqlite3.connect("database.db")

for row in conn.execute("""
SELECT id, username, profile_image
FROM users
"""):
    print(row)

conn.close()