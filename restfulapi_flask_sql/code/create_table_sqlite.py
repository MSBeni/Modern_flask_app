import sqlite3

connection = sqlite3.connect("data.db")

cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)")

# cur.execute("INSERT INTO users VALUES (?,?)", ('user1', '12345'))
#
# users = [
#     ('user2', '123'),
#     ('user3', '6789')
# ]
# cur.executemany("INSERT INTO users VALUES (?,?)", users)
#
# all_users = cur.execute("SELECT * FROM users")
#
# for row in all_users:
#     print(row)

connection.commit()

connection.close()
