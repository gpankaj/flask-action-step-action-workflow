import sqlite3

connection = sqlite3.connect('data.db')

# cursor runs query and store result.
cursor = connection.cursor()

# create a table in SQL db - below is it's schema
create_table = "CREATE TABLE users (id int, username text, password text)"

# run the query
cursor.execute(create_table)

# lets create a user
user = (1,'jose','asdf')

users = [
    (2,'rolf','asfd'),
    (3,'bob','bob')
]

insert_query = "INSERT INTO users VALUES(?,?,?)"

# cursor will replace ? with values from tuple
#cursor.execute(insert_query,user)
cursor.executemany(insert_query,users)

connection.commit()


select_query = "SELECT * FROM users"


for row in cursor.execute(select_query):
    print (row)

connection.close()

