import sqlite3
from flask import Flask,render_template,request, url_for, flash, redirect

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/forum/', methods = ['POST', 'GET'])
def forum():
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM POSTS').fetchall()
	postsl = posts
	tags = []
	tagsnum = []
	nposts = []
	for post in postsl:
		if(post['name'] not in tags):
			tags.append(post['name'])
			tagsnum.append(str(postsl.index(post) + 1))
	for tag in tags:
		for npost in posts:
			if npost['name'] == tag:
				nposts.append(npost)
	posts = conn.execute('SELECT * FROM POSTS').fetchall()
	conn.close()
	name = request.args.get('name')
	if request.method == "POST":
		name = str(request.form['uname'])
	return render_template('forum.html', name = name, posts=posts,tags=tags, tagsnum=tagsnum, nposts=nposts)
#To clear all posts, delete the database file and type "python init_db.py"

@app.route('/create/', methods = ['POST', 'GET'])
def create():
	username = request.args.get('name')
	conn = get_db_connection()
	posts = conn.execute('SELECT * FROM POSTS').fetchall()
	postsl = posts
	tags = []
	for post in postsl:
		if(post['name'] not in tags):
			tags.append(post['name'])
	conn.close()
	if request.method == 'POST':
		name = request.form['name']
		content = request.form['content']
		if not content:
			flash('Post content is required!')
		if not name:
			flash('Post Thread is required!')
		else:
			conn = get_db_connection()
			conn.execute('INSERT INTO posts (name, content, user) VALUES (?, ?, ?)', 
									 (name, content, username))
			conn.commit()
			conn.close()
			return redirect('/forum/?language=python&name=' + username)
	return render_template('create.html', name= username, posts=posts, tags=tags)

app.run(host='0.0.0.0', port=81, debug=True)