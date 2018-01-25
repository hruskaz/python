import sys
import sqlite3
import json


class Composer():
    def __init__(self, id, name, born, died):
        self.id = id
        self.name = name
        self.born = born
        self.died = died

class ResultEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Composer):
            return o.__dict__
        return ResultEncoder(self, o)



#validate input
if(len(sys.argv) != 2):
    print("Invalid argument count.")
    sys.exit()
try:
    id = int(sys.argv[1])
except ValueError:
    print("Bad input: Not a number.")
    sys.exit()

conn = sqlite3.connect('scorelib.dat')
c = conn.cursor()
c.execute("""SELECT a.id, a.name, a.born, a.died FROM print AS p
                INNER JOIN edition AS e
                ON p.edition = e.id
                INNER JOIN score AS s
                ON s.id = e.score                
                INNER JOIN score_author AS sa
                ON sa.score = s.id
                INNER JOIN person AS a
                ON sa.composer = a.id                
                WHERE p.id=?""", [sys.argv[1]])
res = c.fetchall()
if(len(res) == 0):
    print("No record found.")
    sys.exit()
finalAuthors = []
for row in res:
    author = Composer(row[0], row[1].decode("utf-8"), row[2], row[3])
    finalAuthors.append(author)
print(json.dumps(finalAuthors, indent=3, cls=ResultEncoder))


