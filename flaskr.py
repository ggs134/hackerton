#-*-coding:utf-8-*-

# all the import
from flask import Flask, request, redirect, url_for, abort, render_template, flash
from flask import session as login_session
import sys
from flask.ext.pymongo import PyMongo
from bson import ObjectId
#from pymongo.Objectid import ObjectId
# from bson.objectid import Objectid
#from pymongo import MongoClient
#import requests
#import json


#configuration
DEBUG = True
SECRET_KEY = '1234'
USERNAME = 'adminJ'
PASSWORD = 'wjdtnsgud1!'

#create our little application
app=Flask(__name__)
app.config.from_object(__name__)
reload(sys)
sys.setdefaultencoding('utf-8')

# connect to MongoDB database on the same host
app.config['MONGO2_DBNAME'] = 'snack'
mongo = PyMongo(app, config_prefix='MONGO2')

#main page
@app.route('/')
def show_entries():
	detail_list=[i for i in mongo.db.detail.find().limit(5)]
	listlen=len(detail_list)
	return render_template('index.html',detail=detail_list,listlen=listlen)
 
#detail page
@app.route('/snackdetail/<string:snack_name>')
def detail_page(snack_name):
	snack=mongo.db.deail.find_one({"snack_name":snack_name})
	render_template('single_page.html',snack=snack)

#manufacturer page
@app.route('/manufacturer/<string:manufacturer>')
def manufacturer_search(manufacturer):
	searchResult=[i for i in mongo.db.detail.find({}).limit(10)]
	return render_template('index.html', searchResult=searchResult)

# #board2 page
# @app.route('/board2/<int:page_number>')
# def board2(page_number):
# 	#총 글의 갯수를 구함
# 	total_number_writings=int(session.query(func.count('*')).select_from(Board2).scalar())
# 	# 왜 +2를 해야 하지?? 총 페이지 수를 도출
# 	total_page_number=int(total_number_writings/10)+2
# 	if page_number>=total_page_number:
# 		flash('그 페이지는 존재하지 않습니다')
# 		return redirect(url_for('board2', page_number=1))
# 	# count number of writings
# 	# session.query(Entries.id).order_by(desc(Entries.id)).first()
# 	if page_number==None:
# 		page_number=1
# 	writings2=session.query(Board2).order_by(desc(Board2.id)).limit(10).offset((page_number-1)*10).all()
# 	session.close()
# 	return render_template('board2.html', writings2=writings2, page_number=page_number, total_page_number=total_page_number)


# #add new notice
# @app.route('/add', methods=['POST'])
# def add_entry():
# 	newEntry=Entries(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newEntry)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('show_entries'))


# #add new post in board1
# @app.route('/add1', methods=['POST'])
# def add1():
# 	newBoard1=Board1(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newBoard1)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('board1',page_number=1))


# #add new post in board2
# @app.route('/add2', methods=['POST'])
# def add2():
# 	newBoard2=Board2(title=request.form['title'].encode('utf-8'), text=request.form['text'].encode('utf-8'))
# 	session.add(newBoard2)
# 	session.commit()
# 	flash('글이 게시되었어!')
# 	session.close()
# 	return redirect(url_for('board2',page_number=1))


# #admin login page
# @app.route('/login', methods=['GET','POST'])
# def login():
# 	error=None
# 	if request.method=='POST':
# 		if request.form['username'] != app.config['USERNAME']:
# 			error='invalid username'
# 		elif request.form['password'] != app.config['PASSWORD']:
# 			error='invalid password'
# 		else:
# 			login_session['logged_in']=True
# 			flash('로그인 되었습니다.')
# 			return redirect(url_for('show_entries'))
# 	return render_template('login.html', error=error)


# #admin logout
# @app.route('/logout')
# def logout():
# 	login_session.pop('logged_in', None)
# 	flash('로그아웃되었습니다.')
# 	return redirect(url_for('show_entries'))


# @app.teardown_request
# def shutdown_session(exception=None):
# 	DBSession.remove()

if __name__=='__main__':
	app.run(host='0.0.0.0')