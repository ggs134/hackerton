#-*-coding:utf-8-*-

# all the import
from flask import Flask, request, redirect, url_for, abort, render_template, flash
from flask import session as login_session
import sys
from flask.ext.pymongo import PyMongo
from bson import ObjectId
from operator import itemgetter


#configuration
DEBUG = True

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
	detail_list = [i for i in mongo.db.snack.find()]
	return render_template('index.html',detail=detail_list)
 
#detail page
@app.route('/snackdetail/<string:snack_name>')
def detail_page(snack_name):
	snack=mongo.db.detail.find_one({"snack_name": snack_name})
	return render_template('single_page.html',snack=snack)

#manufacturer page
@app.route('/manufacturer/<string:manufacturer>')
def manufacturer_search(manufacturer):
	searchResult=[i for i in mongo.db.snack.find({"manufacturer":manufacturer}).limit(10)]
	return render_template('index.html', searchResult=searchResult)

#detail page
@app.route('/snackdetail/<string:snack_name>/<string:palm>')
def detail_page2(snack_name,palm):
	snack=mongo.db.detail.find_one({"snack_name": snack_name})
	palms = mongo.db.wordcount.find_one({})["contents"]
	palms = palms.items()
	sortedList=sorted(palms, key=itemgetter(1), reverse=True)
	return render_template('single_page.html',snack=snack,palm=sortedList)

if __name__=='__main__':
	app.run(host='0.0.0.0')