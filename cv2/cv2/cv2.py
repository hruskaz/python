import re # regular expressions
import sqlite3

# This is a base class for objects that represent database items.  It
# implements
# the store() method in terms of fetch_id and do_store, which need to be
# implemented in every derived class (see Person below for an example).
class DBItem:
    def __init__(self, conn):
        self.id = None
        self.cursor = conn.cursor()

    def store(self):
        self.fetch_id()
        if (self.id is None):
            self.do_store()
            self.cursor.execute("select last_insert_rowid()")
            self.id = self.cursor.fetchone()[0]

# Example of a class which represents a single row of a single database table.
# This is a very simple example, since it does not contain any references to
# other objects.
class Person(DBItem):
    def __init__(self, conn, string):
        super().__init__(conn)
        self.born = self.died = None
        self.name = re.sub('\([0-9/+-]+\)', '', string).strip()
        # NB.  The code below was part of the exercise (extracting years of
        # birth & death
        # from the string).
        m = re.search("([0-9]+)--([0-9]+)", string)
        if not m is None:
            self.born = int(m.group(1))
            self.died = int(m.group(2))

    # TODO: Update born/died if the name is already present but has null values
    # for
    # those fields.  We assume that names are unique (not entirely true in
    # practice).
    def fetch_id(self):
        self.cursor.execute("select * from person where name = ?", (self.name,))
        res = self.cursor.fetchone()

        # NB.  The below lines had a bug in the original version of
        # scorelib-import.py (which however only becomes relevant when you
        # start implementing the Score class).
        res = self.cursor.fetchone()
        if not res is None: # TODO born/died update should be done inside this if
            self.id = res[0]
            mod = False
            if res[1] is None:
                mod = True
            if res[2] is None:
                mod = True
            if mod:
                self.do_update()

    def do_update(self):
        self.cursor.execute("update person set born = ?, died = ? where name = ?", (self.born, self.died, self.name))

    def do_store(self):
        print("storing '%s'" % self.name)
        # NB.  Part of the exercise was adding the born/died columns to the
        # below query.
        self.cursor.execute("insert into person (name, born, died) values (?, ?, ?)",
                             (self.name, self.born, self.died))


class Score(DBItem):
    def __init__(self, conn, string):
        super().__init__(conn)
        spl = string.split("<->")
        self.genre = spl[0].strip()
        self.key = spl[1].strip()
        self.incipit = spl[2].strip()
        self.year = spl[3].strip()
        self.authors = []
        for c in spl[4].split(';'):
            p = Person(conn, c.strip())
            p.store()
            self.authors.append(p.id)

    def fetch_id(self):
        self.cursor.execute("select * from score where genre=? and key=? and incipit=? and year=?", (self.genre, self.key, self.incipit, self.year))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]

    def do_update(self):
        self.cursor.execute("update score set genre = ?, key = ?, incipit = ?, year = ?", (self.genre, self.key, self.incipit, self.year))

    def do_store(self):
        self.cursor.execute("insert into score (genre, key, incipit, year) values (?, ?, ?, ?)", (self.genre, self.key, self.incipit, self.year))

class Voice(DBItem):
	def __init__(self, conn, string):
		super().__init__(conn)
		spl = string.split(",")
		self.number = spl[0].strip()
		self.score = spl[1].strip()
		self.name = spl[2].strip()

	def fetch_id(self):
		self.cursor.execute("select * from voice where number = ? and score = ? and name = ?", (self.number, self.score, self.name))
		res = self.cursor.fetchone()
		if not res is None:
			self.id = res[0]


	def do_update(self):
		self.cursor.execute("update voice set number=?, score=?, name=?", (self.number, self.score, self.name))

	def do_store(self):
		self.cursor.execute("insert into voice (number, score, name) values (?, ?, ?)", (self.number, self.score, self.name))


class Edition(DBItem):
    def __init__(self, conn, string):
        super().__init__(conn)
        spl = string.split(",")
        self.score = spl[0].strip()
        self.name = spl[1].strip()
        self.year = spl[2].strip()


    def fetch_id(self):
        self.cursor.execute("select id from edition where score = ? and name = ? and year = ?", (self.score, self.name, self.year))
        res = self.cursor.fetchone()
        if not res is None:
            self.id = res[0]
    
    def do_update(self):
        self.cursor.execute("update edition set score = ?, name = ?, year = ?", (self.score, self.name, self.year))

    def do_store(self):
        self.cursor.execute("insert into edition (score, name, year) values (?, ?, ?)", (self.score, self.name, self.year))


class Score_Author(DBItem):
	def __init__(self, conn, string):
		super().__init__(conn)
		spl = string.split(",")
		self.score = spl[0].strip()
		self.composer = spl[1].strip()

	def fetch_id(self):
		self.cursor.execute("select * from score_author where score = ? and composer = ?", (self.score, self.composer))
		res = self.cursor.fetchone()
		if not res is None:
			self.id = res[0]

	def do_update(self):
		self.cursor.execute("update score_author set score=?, composer=?", (self.score, self.composer))

	def do_store(self):
		self.cursor.execute("insert into score_author (score, composer) values (?, ?)", (self.score, self.composer))


class Edition_Author(DBItem):
	def __init__(self, conn, string):
		super().__init__(conn)
		spl = string.split(",")
		self.edition = spl[0].strip()
		self.editor = spl[1].strip()

	def fetch_id(self):
		self.cursor.execute("select * from edition_author where edition = ? and editor = ?", (self.edition, self.editor))
		res = self.cursor.fetchone()
		if not res is None:
			self.id = res[0]

	def do_update(self):
		self.cursor.execute("update edition_author set edition=?, editor=?", (self.edition, self.editor))

	def do_store(self):
		self.cursor.execute("insert into edition_author (edition, editor) values (?, ?)", (self.edition, self.editor))


class Print(DBItem):
	def __init__(self, conn, string):
		super().__init__(conn)
		spl = string.split(",")
		self.num = spl[0].strip()
		self.partiture = self.get_partiture(spl[1].strip())
		self.edition = spl[2].strip()

	def get_partiture(self, string):
		if string == "yes":
			return 'Y'
		if string == "no":
			return 'N'
		return 'P'

	def fetch_id(self):
		self.cursor.execute("select id from print where id=?", (self.num,))
		res = self.cursor.fetchone()
		if not res is None:
			self.id = res[0]

	def do_update(self):
		self.cursor.execute("update print set partiture=?, edition=?", (self.pariture, self.edition))

	def do_store(self):
		self.cursor.execute("insert into print (partiture, edition) values (?, ?)", (self.partiture, self.edition))

# NB.  Everything below this line was part of the exercise.

# Process a single line of input.
def process(k, v):
    if k == 'Composer':
        for c in v.split(';'):
            p = Person(conn, c.strip())
            p.store()

def processScore(scoredata):
    scorestring = str(scoredata['Genre']) + "<->" + str(scoredata['Key']) + "<->" + str(scoredata['Incipit']) + "<->" + str(scoredata['Composition Year']) + "<->" + str(scoredata['Composer'])
    score = Score(conn, scorestring)
    score.store()
    for composer in scoredata['Composer'].split(';'):
        person = Person(conn, composer.strip())
        person.store()
    for author in score.authors:
        scoreautorstring = str(score.id) + ", " + str(author)
        scoreauthor = Score_Author(conn, scoreautorstring)
        scoreauthor.store()
    if('Editor' in scoredata):
        editor = Person(conn, scoredata['Editor'])
        editor.store()
        editionstring = str(score.id) + ", " + str(scoredata['Edition']) + ", " + str(scoredata['Publication Year'])
        edition = Edition(conn, editionstring)
        edition.store()
        editionauthorstring = str(edition.id) + ", " + str(edition.id)
        editionauthor = Edition_Author(conn, editionauthorstring)
        editionauthor.store()
    vrx = re.compile(r"Voice ([0-9]*)")
    for k,v in scoredata.items():
        if vrx.match(k):
            voicestr = str(vrx.match(k).group(1)) + ", " + str(score.id) + ", " + str(v)
            vc = Voice(conn, voicestr)
            vc.store()
    printstring = str(scoredata['Print Number'] + ", " + scoredata['Partiture'] + ", " + scoredata['Edition'])
    print = Print(conn, printstring)
    print.store()


# Database initialisation: sqlite3 scorelib.dat ".read scorelib.sql"
conn = sqlite3.connect('scorelib.dat')
rx = re.compile(r"([^:]*):(.*)")
rxend = re.compile(r"^\s*$")
scoredata = {}
for line in open('scorelib.txt', 'r', encoding='utf-8'):
    if rxend.match(line):
        if(scoredata):
            processScore(scoredata)
        scoredata = {}
        continue

    m = rx.search(line)
    if m is None: continue
    else:
        scoredata[m.group(1)] = m.group(2)

conn.commit()
