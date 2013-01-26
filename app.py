import random, string
import os
from flask import render_template
from flask import Flask
import sqlite3
from flask import request,url_for
from flask import redirect,Response

app = Flask(__name__)

def connect_db():
    	return sqlite3.connect(DATABASE)

def init_db():
	db=sqlite3.connect('url.db')
	orgurl=''
	nwurl=''
	data=(orgurl, nwurl)
	con = sqlite3.connect("url.db")
	cur=con.cursor()
   	cur.execute("CREATE TABLE IF NOT EXISTS url(orgurl text, nwurl text)")
    	cur.execute("INSERT INTO url VALUES(?, ?)", data)
	con.commit()
	con.close()	
	
	
@app.route('/')
def home_page(name=None):
	return render_template('main.html',name=name)
	

@app.route('/html',methods=['POST', 'GET'])
def main():
	orgurl = request.form['orgurl']
	orgurl = 'http://'+orgurl
	con = sqlite3.connect("url.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM url  WHERE orgurl=:name", {"name": orgurl})
	rows = cur.fetchall()
	if rows:
		for row in rows:
			if row[0]==orgurl:
				return ('<body style = "background-color:lightblue;"><h1><i><b>Shortend Url:http://127.0.0.1:5000/%s</i></b></h1>'%(row[1]))




	else:
		nwurl=''
		list=[]
		for i in range(len(orgurl)):
			if i%10==0:
				list.append(orgurl[i])

		nwurl=''.join(list)+random.choice(string.ascii_letters)

		data=(orgurl, nwurl)
		con = sqlite3.connect("url.db")
		cur=con.cursor()
   		cur.execute("CREATE TABLE IF NOT EXISTS url(orgurl text, nwurl text)")
    		cur.execute("INSERT INTO url VALUES(?, ?)", data)
		con.commit()
		con.close()
		return ('<body style = "background-color:lightblue;"><h1><i><b>Shortend Url:http://127.0.0.1:5000/%s</i></b></h1>'%(nwurl))



@app.route('/<username>',methods=['GET','POST'])
def redirection(username):
	nwurl=username
      	con = sqlite3.connect("url.db")
	cur = con.cursor()
	cur.execute("SELECT * FROM url  WHERE nwurl=:name", {"name": nwurl})
      	rows = cur.fetchall()
	if rows:
		for row in rows:
			if row[1]==nwurl:
				return redirect(row[0])
	
	
		
	


		
	



	
if __name__ == '__main__':
    init_db()
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
