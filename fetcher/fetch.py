import os, glob, shutil, sqlite3
from git import Repo
from subprocess import Popen, PIPE

global home
home = os.path.expanduser('~')

def checkAndClone():
	if os.path.exists(home + "/posts"):
		shutil.rmtree(home + "/posts")
	Repo.clone_from("https://github.com/kousikk/posts", home + "/posts")

def parseMarkDown():
	blogList = glob.glob(home + "/posts/*.md")

	titles = []
	htmlContent = []
	
	for name in blogList:
		if name.split('/')[4] != "README.md":
			tname = name.replace(" ", "\ ")
			process = Popen("python -m markdown " + tname, bufsize = 102400, stdout=PIPE, shell = True, close_fds = True)
			htmlContent.append(process.stdout.read())
			titles.append(name.split('/')[4][:-3])
	return htmlContent, titles

def sqlConnect():
	global db
	db = home + '/blog.db'
	if os.path.exists(db):
		os.remove(db)
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	cursor.execute('create table blog(author text, id text, month text, year text, title text, meta text, content text)')
	conn.commit()
	return conn

def populate(conn, title, content):
	cursor = conn.cursor()
	content = content.split('\n')
	id = str(content[1])
	author = str(content[2])
	month = str(content[3])
	year = str(content[4])
	meta = str(content[5])
	postbody = ""
	for i in range(7, len(content)):
		postbody += content[i]
		if len(content[i]) == 0:
				postbody += "<br>"
		postbody += "\n"
		
	cursor.execute('insert into blog values(?, ?, ?, ?, ?, ?, ?)',[author, id, month, year, title, meta, postbody])
	conn.commit()


print "Cloning Repository... Any directory of the name \"posts\" in your home directory will be deleted"
checkAndClone()
print "Clone successful"

print "Parsing markdown files..."
htmlContent, titles = parseMarkDown()
print "Parsing complete"

print "Injecting blog posts into database"
conn = sqlConnect()

i = 0
for blogentry in htmlContent:
	populate(conn, titles[i], htmlContent[i])
	i += 1

print "Successfully completed injecting"
