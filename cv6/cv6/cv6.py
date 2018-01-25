
from flask import Flask, request, Response
import json
import sqlite3
import sys

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

def search(author):
    conn = sqlite3.connect('scorelib.dat')
    c = conn.cursor()
    c.execute("""SELECT p.id, p.name, p.born, p.died, s.name, s.genre, s.key, s.incipit, s.year FROM person AS p
                INNER JOIN score_author AS sa
                ON sa.composer = p.id
                INNER JOIN score AS s
                ON s.id = sa.score                 
                WHERE p.name LIKE lower(?)""", ['%' + author + '%'])
    res = c.fetchall()
    if(len(res) == 0):
        return "No record found."
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
    return finalAuthors;

def convertToHtml(authors):
    toRet = ""
    for author in authors:
        toRet += ("<h1>\n\nComposer: %s</h1>" % (author.name))
        for song in author.scores:
            toRet += ("""<ul>
								<li>Score: %s</li>
								<li>Genre: %s</li>
								<li>Year: %s</li>
							 </ul>""" % (song.name,song.genre,song.year))
    return toRet


app = Flask(__name__)

@app.route('/', methods=['GET'])
def processRequest():
   if request.method == 'GET':    
        return """<html>
					<head>
						<title>
							Title
						</title>
					</head>
					<body>
						<form action=\"/result\" method=\"GET\">
							Name:<br>
							<input type=\"text\" name=\"q\"><br>
							<input type=\"radio\" name=\"f\" value=\"html\" checked>HTML<br>
							<input type=\"radio\" name=\"f\" value=\"json\">JSON<br>
							<input type=\"submit\" value=\"SEND\">
						</form>
					</body>
				</html>"""
       
@app.route('/result')
def catch_all():
    author = request.args.get('q')
    format = request.args.get('f')
    if(format == 'json'):
        return json.dumps(search(author), indent=3, cls=ComposerEncoder)
    else:
        return convertToHtml(search(author))

if __name__ == '__main__':
     app.run(port=8000)

