import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# creating a table
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = " CREATE TABLE IF NOT EXISTS homeitems (name text, price real)"
cursor.execute(create_table)

# cursor.execute("INSERT INTO homeitems VALUES ('testvalue',100.99)") # testing the values are getting inserted or not

connection.commit()

connection.close()