
import sys
import sqlite3
import json

class Composer():
    def __init__(self, id, name, born, died):
        self.id = id
        self.name = name
        self.born = born
        self.died = died
        self.scores = []

class Score():
    def __init__(self, name, genre, key, incipit, year):
        self.name = name
        self.genre = genre
        self.key = key
        self.incipit = incipit
        self.year = year

class ComposerEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Composer):
            return o.__dict__
        if isinstance(o, Score):
            return o.__dict__
        return ResultEncoder(self, o)



#validate input
if(len(sys.argv) != 2):
    print("Invalid argument count.")
    sys.exit()

conn = sqlite3.connect('scorelib.dat')
c = conn.cursor()
c.execute("""SELECT p.id, p.name, p.born, p.died, s.name, s.genre, s.key, s.incipit, s.year FROM person AS p
                INNER JOIN score_author AS sa
                ON sa.composer = p.id
                INNER JOIN score AS s
                ON s.id = sa.score                 
                WHERE p.name LIKE lower(?)""", ['%' + sys.argv[1] + '%'])
res = c.fetchall()
if(len(res) == 0):
    print("No record found.")
    sys.exit()
finalAuthors = []
for row in res:
    actualAuthor = None
    for aut in finalAuthors:
        if(aut.id == row[0]): 
            actualAuthor = aut
			actualAuthor.scores.append(Score(row[4], row[5], row[6], row[7], row[8]))
    if(actualAuthor == None):
        actualAuthor = Composer(row[0], row[1], row[2], row[3])
		actualAuthor.scores.append(Score(row[4], row[5], row[6], row[7], row[8]))
		finalAuthors.append(actualAuthor)
print(json.dumps(finalAuthors, indent=3, cls=ComposerEncoder))
