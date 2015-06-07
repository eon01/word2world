#!/usr/bin/env python
#This is a fast prototyped fast application developped for fun.


import random
import sqlite3
import os, re
from flask import Flask, render_template, redirect, request

#Todo:
# Secure against CSRF
# Add try/catch blocks where it should be added

app = Flask(__name__)

app.config['SECRET_KEY'] = '';

colors = ['#58749e', '#79589e', '#589e86', '#5d9e58', '#7f589e']
fonts = ["Times New Roman", "Verdana", "Comic sans MS", "WildWest", "Bedrock", "arial,helvetica", "Lucida Calligraphy,Comic Sans MS,Lucida Console", "new century schoolbook"]
sizes = [ '100%', '120%', '140%', '160%', '180%'  ]



@app.route('/')
def index():
        global h
	h = []
	con = sqlite3.connect('words.db')
	c = con.cursor()
	c.execute('SELECT word FROM wt')
	#get a list of unique elements from another list elements.
	words = list(set(list(c.fetchall())))

	c.close()
	for word in words:

		color = random.choice(colors)
		font = random.choice(fonts)
		size = random.choice(sizes)

		h.append("<p style='\
		display:inline;\
		color:%s;\
		font-family:%s;\
		font-size: %s;\
		'>&nbsp;%s&nbsp</p>" % (color, font, size, ''.join(word) ))

	return render_template('index.html', h=h)


@app.route('/save',methods=['POST'])
def save():

	match_object = request.form['word2'].isalpha()
	size = len(request.form['word2'])
        #Todo : try and catch for sqlite3 operations
	if (match_object) and (size > 0) and (size < 35):
		word = request.form['word2']
		con = sqlite3.connect('words.db') # Warning: This file is created in the current directory
		con.execute("CREATE TABLE IF NOT EXISTS wt (id INTEGER PRIMARY KEY, word char(100) NOT NULL)")
		c = con.cursor()
		c.execute("INSERT INTO wt (word) VALUES (?)", (word, ))
		con.commit()
		con.close()
		#return redirect("/", code=302, word=word)
		return render_template('index.html', word=word, h='')
	else:
		return render_template('index.html', word='', h='')



#
#
#
if __name__ == '__main__':
    # Bind to PORT 5000.
	port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
