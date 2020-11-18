import sqlite3

conn = sqlite3.connect('mytest.db')
# f = open("score2.txt", encoding="utf-8")
# txt = f.read()

c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS persons
                (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name1 TEXT, name2 TEXT)''')

c.execute(''' CREATE TABLE IF NOT EXISTS scores
                (personID INTEGER, task INTEGER, score INTEGER, FOREIGN KEY (personID) REFERENCES persons(ID) ON DELETE CASCADE)''')

with open("score2.txt", "r") as f:

    for line in f.readlines():
        line = line.split()
        firstName = line[2]
        lastName = line[3]
        nameArr = [firstName, lastName]
        score = line[4]
        task = line[1]
        scoresTasks = [task, score]

        #Adds a first and last name into the database
        c.execute('INSERT INTO persons (name1, name2) VALUES (?,?)', nameArr)
        #Deletes existing names :)
        c.execute('DELETE FROM persons WHERE rowid NOT IN (SELECT min(rowid) FROM persons GROUP BY name1, name2)')
 
        #TODO: Add score to scores table
        c.execute('INSERT INTO scores (task, score) VALUES (?,?)', scoresTasks)

    # for row in c.execute('SELECT * FROM persons ORDER BY ID'):
    #     print(row)
    for sRow in c.execute('SELECT * FROM scores ORDER BY personID'):
        print(sRow)

    # for idk in c.execute('SELECT name1,name2,task,score FROM persons JOIN scores ON id=sID'):
    #     print(idk)
conn.commit()

conn.close()