import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# create a table in sqldb
create_table = "CREATE TABLE users(id int, username text, password text)"
cursor.execute(create_table)

# insert the values into DB
user = (1,'tom','pass')
insert_query = "INSERT INTO users values (?,?,?)"
cursor.execute(insert_query,user)


# create multiple users
users = [
    (2, 'mary', 'word'),
    (3, 'harry', 'paw')
]
cursor.executemany(insert_query,users)

# retrieve the data
select_query = "Select * from users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()    # to save the data


connection.close()     # to close the connection