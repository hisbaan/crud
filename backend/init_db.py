import sqlite3

connection = sqlite3.connect('items.db')

with open('schema.sql') as schema:
    connection.executescript(schema.read())

cursor = connection.cursor()

cursor.execute(
    "INSERT INTO items (name, quant, tags) VALUES (?, ?, ?)",
    ('apple', 10, 'apple red sweet')
)
cursor.execute(
    "INSERT INTO items (name, quant, tags) VALUES (?, ?, ?)",
    ('apple', 20, 'apple green sour')
)
connection.commit()
connection.close()
