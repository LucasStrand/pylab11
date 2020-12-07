import sqlite3

conn = sqlite3.connect('mytest.db')
# f = open("score2.txt", encoding="utf-8")
# txt = f.read()

c = conn.cursor()
c.execute(''' CREATE TABLE IF NOT EXISTS persons
                (ID INTEGER PRIMARY KEY AUTOINCREMENT, name1 TEXT, name2 TEXT, UNIQUE(name1, name2))''')

c.execute(''' CREATE TABLE IF NOT EXISTS scores
                (personID INTEGER, task TEXT, score TEXT, FOREIGN KEY (personID) REFERENCES persons(ID) ON DELETE CASCADE, UNIQUE(personID, task))''')

with open("score2.txt", "r") as f:

    for line in f.readlines():
        line = line.split()
        firstName = line[2]
        lastName = line[3]
        score = line[4]
        task = line[1]

        #Deletes existing names :)
        #c.execute('DELETE FROM persons WHERE rowid NOT IN (SELECT min(rowid) FROM persons GROUP BY name1, name2)')
 
        c.execute("INSERT OR IGNORE INTO persons (name1, name2) VALUES (?,?)", [firstName, lastName])
        c.execute("INSERT OR IGNORE INTO scores VALUES ((SELECT ID FROM persons WHERE name1 = ? AND name2 = ?),?, ?)", [firstName, lastName, task, score])

    #print out the top 10 players
    print("...")
    for i in c.execute("SELECT name1, name2, SUM(score) as s FROM persons JOIN scores ON ID = personID GROUP BY name1, name2 ORDER BY s DESC LIMIT 10"):
       print(i)
    print("...")

    #print out the top 10 most difficult (least yielding) tasks
    # for i in c.execute("SELECT task, SUM(score) as s FROM scores GROUP BY task ORDER BY s ASC LIMIT 10"):
    #    print(i)
    # print("...")

    #print out the tables persons and/or scores
    #for i in c.execute("SELECT * FROM persons"):
    #    print(i)
    #print("...")
    #for i in c.execute("SELECT * FROM scores"):
    #    print(i)


conn.commit()

conn.close()