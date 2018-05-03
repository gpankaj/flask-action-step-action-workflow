import sqlite3

connection = sqlite3.connect('data.db')

# cursor runs query and store result.
cursor = connection.cursor()

# create a table in SQL db - below is it's schema
create_users_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"



create_steps_table = "CREATE TABLE IF NOT EXISTS steps (id INTEGER PRIMARY KEY, name text, initial text, public text, active text, action text," \
                     "message_user text, error_message text, next_step text)"
                        #creator text, created_on date)"



create_actions_table = "CREATE TABLE IF NOT EXISTS actions (id INTEGER PRIMARY KEY, action_script text, public text, active text, " \
                     "error_message text, success_message text)"

# run the query
cursor.execute(create_users_table)
cursor.execute(create_steps_table)
cursor.execute(create_actions_table)

cursor.close()
connection.close()