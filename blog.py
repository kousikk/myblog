import sqlite3, os, sys
from flask import render_template

def connectdb(db):
	createTable = True
	if os.path.exists(db):
		createTable = False
	conn = sqlite3.connect(db)
	cursor = conn.cursor()

	if createTable:
		cursor.execute('create table blog(author text, id text, month text, year text, title text, meta text, content text)')

		cursor.execute('insert into blog values(?, ?, ?, ?, ?, ?, ?)',["kousikk", "1", "16 Aug", "2013", "Lorem Ipsum", "Sample", "Hello World!"])
		cursor.execute('insert into blog values(?, ?, ?, ?, ?, ?, ?)',["kousikk", "1", "16 Aug", "2013", "Lorem Ipsum", "Sample", "Hello World!"])
		conn.commit()
	return conn

def readFile(filename):
	f = open(filename)
	ret = f.read()
	f.close()
	return ret

def boilerplate(month, date, title, author, content):
	ret = "\n \
		\t\t<div class=\"container\">\n \
		\t\t\t<div class=\"row bloghead col-md-9\"><br>\n \
		\t\t<div class=\"timestamp col-md-2\">\n \
		\t\t\t<br>\n \
		\t\t\t<center>\n \
		\t\t\t\t<div class=\"month\">" + month + "</div>\n \
		\t\t\t\t<div class=\"date\">" + date + "</div>\n \
		\t\t\t\t<br>\n \
		\t\t\t</center>\n \
		\t\t</div>\n \
		\t\t<div class=\"post-title col-md-10\">\n \
		\t\t\t" + title + "<br>\n \
		\t\t\t<div class=\"post-author\">\n \
		\t\t\t\tby " + author + "\n \
		\t\t\t</div>\n \
		\t\t</div>\n \
		\t</div>\n \
		\t<div class=\"row seperator col-md-9\">\n \
		\t\t<hr class=\"thick\"></hr>\n \
		\t</div>\n \
		\t<div class=\"row post-content col-md-9\">\n \
		\t\t " + content + "<br><br>\n \
		\t</div>\n \
		</div>\n \
		<!-------------------------------------------->\n"

	return ret

def getHR():
	return	"<div class=\"container\">\n \
		\t<div class=\"row bloghead col-md-9\">\n \
		\t\t<hr>\n \
		\t</div>\n \
		</div>\n"
def getClosingTags():
	ret = "\t</div>\n</body>\n</html>\n"
	return ret

def getPrevNext(prev, nxt, pid):
	returnStr = "\t\t<div class=\"container\">\n"
	returnStr += "\t\t\t<div class=\"row bloghead col-md-9\"><center>\n"
	if prev:
		prevlink = "/post/" + str(pid - 1)
		returnStr += "\t\t\t\t<a href=\"" + prevlink + "\">\n \
			\t\t<button class=\"btn btn-4 btn-4b icon-arrow-left \">PREV</button>\n \
			\t</a>\n"
	else:
		returnStr += "\t<button type=\"button\" class=\"btn btn-4 btn-4b icon-arrow-left \" disabled>PREV</button>\n"

	if nxt:
		nextlink = "/post/" + str(pid + 1)
		returnStr += "\t\t\t\t<a href=\"" + nextlink + "\">\n \
			\t\t<button class=\"btn btn-4 btn-4a icon-arrow-right \">NEXT</button>\n \
			\t</a>\n"
	else:
		returnStr += "\t<button type=\"button\" class=\"btn btn-4 btn-4a icon-arrow-right \" disabled>NEXT</button>\n"

	returnStr += "\t\t\t</center></div>\n"
	returnStr += "\t\t</div>\n"
	return returnStr

def getTimelineBoilerPlate(pid, month, year, title, meta):
	href = "/post/" + str(pid)
	returnHTML = "\t\t\t\t\t<li>\n \
			\t\t\t<time class=\"cbp_tmtime\"><span>" + month + "</span> <span>"+year+"</span></time>\n \
		\t\t\t\t<div class=\"cbp_tmicon cbp_tmicon-phone\"></div>\n \
		\t\t\t\t<div class=\"cbp_tmlabel\">\n \
		\t\t\t\t\t<div class=\"post-title\"><a href=\"" + href + "\" target=\"_newtab\">" + title + "</a></div>\n \
		\t\t\t\t\t<hr>\n \
		\t\t\t\t\t<p>" + meta + "</p>\n \
		\t\t\t\t</div>\n \
		\t\t\t</li>\n"
	return returnHTML

def getDisqus():
	returnHTML = "<div class=\"container\">\n \
		<div class=\"row bloghead col-md-9\">\n \
		<div id=\"disqus_thread\"></div>\n \
		<script type=\"text/javascript\">\n \
        	/* * * CONFIGURATION VARIABLES: EDIT BEFORE PASTING INTO YOUR WEBPAGE * * */\n \
        	var disqus_shortname = 'plicense'; // required: replace example with your forum shortname\n \
        	/* * * DON'T EDIT BELOW THIS LINE * * */ \n \
        	(function() {\n \
            	var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;\n \
            	dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';\n \
            	(document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);\n \
 	       	})();\n \
		</script>\n \
		<noscript>Please enable JavaScript to view the <a href=\"http://disqus.com/?ref_noscript\">comments powered by Disqus.</a></noscript>\n \
		<a href=\"http://disqus.com\" class=\"dsq-brlink\">comments powered by <span class=\"logo-disqus\">Disqus</span></a>\n \
		</div>\n \
		</div>"
	return returnHTML
    
#Following functions will be called from router.py
def getArchives(db):
	returnHTML = ""
	try:
		returnHTML = render_template('archives.html')

		conn = connectdb(db)
		cursor = conn.cursor()

		query = 'select t1.id, t1.title, t1.month, t1.year, t1.meta, t1.author from blog t1'

		blogList = cursor.execute(query).fetchall()

		blogList = sorted(blogList, key=lambda ele: ele[0])
		blogList = blogList[::-1]

		returnHTML += "\n\t\t<div class = \"container\">\n \
			<div class = \"main\">\n \
			\t<ul class = \"cbp_tmtimeline post-content\">\n"
		for item in blogList:
			returnHTML += getTimelineBoilerPlate(pid = item[0], month = item[2], year = item[3], title = item[1], meta = item[4])
		
		returnHTML += "\t\t\t\t</ul>\n \
			</div>\n \
		</div> \n "
		returnHTML += getClosingTags()
	except:
		print sys.exc_info()[0]
		returnHTML = render_template('error.html')
	
	return returnHTML

def getPost(db, pid):
	returnHTML = ""
	try:
		returnHTML = render_template('blog.html')

		conn = connectdb(db)
		cursor = conn.cursor()

		query = 'select t1.id, t1.author, t1.month, t1.year, t1.title, \
			t1.meta, t1.content from blog t1 \
			where id = ' + str(pid);

		blogContent = cursor.execute(query).fetchall()

		query = 'select COUNT(id), author from blog group by author'
		post_count = cursor.execute(query).fetchall()[0][0]

		prev = (pid > 1)
		nxt = (pid < post_count)

		m = blogContent[0][2] #month
		d = blogContent[0][3] #year
		t = blogContent[0][4] #title
		a = blogContent[0][1] #author
		c = blogContent[0][6] #content

		returnHTML += boilerplate(month = m, date = d, title = t, author = a, content = c)
		
		returnHTML += getDisqus()
		returnHTML += getHR()
		returnHTML += getPrevNext(prev, nxt, pid)
		returnHTML += getHR()
		returnHTML += getClosingTags()
	except:
		print sys.exc_info()[0]
		returnHTML = render_template('error.html')
	
	return returnHTML

def getBlogData(db, home):
	returnHTML = ""
	try:
		conn = connectdb(db)
		cursor = conn.cursor()

		#Count total no of posts
		query = 'select COUNT(id), author from blog group by author'
		post_count = cursor.execute(query).fetchall()[0][0]
		
		returnHTML = getPost(db, post_count)
	except:
		returnHTML = render_template('error.html')
	
	return returnHTML 
