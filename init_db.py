import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (name, content, user) VALUES (?, ?, ?)",
            ('Tennis', 'Hello, I am headed to play tennis at the Settlers Walk courts later today. Is anyone avaible to come?', 'David')
            )

#cur.execute("INSERT INTO posts (name, content) VALUES (?, ?)",
 #           ('Second Post', 'Content for the second post')
  #          )

connection.commit()
connection.close()