import sqlite3

connection = sqlite3.connect("data.db")

cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")

cur.execute("CREATE TABLE IF NOT EXISTS items (name text, price real)")

cur.execute("INSERT INTO items VALUES (?,?)", ('test', 10.99))
#
# users = [
#     ('user2', '123'),
#     ('user3', '6789')
# ]
# cur.executemany("INSERT INTO users VALUES (?,?)", users)
#
all_items = cur.execute("SELECT * FROM items")

for row in all_items:
    print(row)

connection.commit()

connection.close()
