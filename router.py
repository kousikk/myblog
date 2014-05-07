from os import path
from flask import Flask, render_template, render_template_string
from blog import getBlogData, getPost, getArchives

app = Flask(__name__)

@app.route('/archives')
def archives():
	global HOME, DATABASE
	HOME = path.expanduser('~') + '/'
	DATABASE = HOME + 'blog.db'

	return render_template_string(getArchives(db = DATABASE))

@app.route('/post/<int(min = 1, max = 100):pid>')
def render(pid):
	global HOME, DATABASE
	HOME = path.expanduser('~') + '/'
	DATABASE = HOME + 'blog.db'
	
	return render_template_string(getPost(db=DATABASE, pid=pid))

@app.route('/')
def homepage():
	global HOME, DATABASE
	HOME = path.expanduser('~') + '/'
	DATABASE = HOME + 'blog.db'
	return render_template_string(getBlogData(DATABASE, HOME))

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True, port = 5000)
