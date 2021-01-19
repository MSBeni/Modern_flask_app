import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        data = cur.execute("SELECT * FROM items WHERE items.name=?", (name,))
        row = data.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def insert_into_table(self):

        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        cur.execute("INSERT INTO items VALUES (?,?)", (self.name, self.price))
        connection.commit()
        connection.close()

    def update_table(self):

        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        cur.execute("UPDATE items SET price=? WHERE items.name=?", (self.price, self.name))
        connection.commit()
        connection.close()
