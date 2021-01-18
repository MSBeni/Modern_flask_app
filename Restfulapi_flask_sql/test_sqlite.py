import sqlite3

connection = sqlite3.connect("data.db")

cur = connection.cursor()

cur.execute("CREATE TABLE users (id int, username text, password text)")

cur.execute("INSERT INTO users VALUES (?,?,?)", (1, 'user1', '12345'))

users = [
    (2, 'user2', '123'),
    (3, 'user3', '6789')
]
cur.executemany("INSERT INTO users VALUES (?,?,?)", users)

all_users = cur.execute("SELECT * FROM users")

for row in all_users:
    print(row)

connection.commit()

connection.close()
