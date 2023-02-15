from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql
import Configurations as c
from werkzeug.utils import secure_filename
import os

db = mysql(*c.DB_CRED)
db.err_page = 0

app = Blueprint("webrep",__name__,template_folder='pages')
# app = Blueprint("webrep",__name__,url_prefix='/webrep',template_folder='pages')



class _main:
	def is_on_session(): return ('USER_DATA' in session)

	def __init__(self, arg):super(_main, self).__init__();self.arg = arg

	app.errorhandler(404)
	def is_on_session(): return ('USER_DATA' in session)

	# ======================================================================================================
	@app.route("/webrep",methods=["POST","GET"])
	def home():
		return redirect("/hi_there")

	@app.route("/hi_there",methods=["POST","GET"])
	def hi_there():
		return render_template("home/home.html")

	@app.route("/rapid/<_>",methods=["POST","GET"])
	def home_(_):
		if(_!="home/home.html"):
			return _main._404(404)
		return render_template("home/home.html")
	# ===========================================================/

	@app.route("/rapid/<segment>/<page>",methods=["POST","GET"])
	def page_loader(segment,page):
		if(page.lower()=="adminKnowledgeCenter.html".lower()):
			if(_main.is_on_session()):
				return render_template("{}/{}".format(segment,page),users=_main.get_all_user(),is_session =_main.is_on_session(),user_data=session["USER_DATA"][0])
			else:
				return redirect("/login?force_url=1")
		elif(page.lower()=="NewsAndStories.html".lower()):
			if(_main.is_on_session()):
				return render_template(
					"{}/{}".format(segment,page),
					users=_main.get_all_user(),
					is_session =_main.is_on_session(),
					user_data=session["USER_DATA"][0],
					page_data=_main.get_post()
				)
		elif(page.lower()=="home.html".lower()):
			if(_main.is_on_session()):
				return render_template(
					"{}/{}".format(segment,page),
					users=_main.get_all_user(),
					is_session =_main.is_on_session(),
					user_data=session["USER_DATA"][0],
					page_data=_main.get_post()
				)
			else:
				return redirect("/login?force_url=1")

		_main.moderator(segment,page)
		return render_template("{}/{}".format(segment,page),is_session =_main.is_on_session())
	# ==================================================================



	@app.route("/webrep/article/get_post",methods=["POST","GET"])
	def get_post():
		return db.select("SELECT * from `webrep_articles`;")

	@app.route("/webrep/article/post",methods=["POST","GET"])
	def article_post():
		from datetime import date, datetime
		data = dict(request.form)
		key = [];val = []
		data["USER_ID"] = session["USER_DATA"][0]['id']
		for datum in data:
			key.append("`{}`".format(datum))
			val.append("'{}'".format(data[datum]))
		sql = ('''INSERT INTO `webrep_articles` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
		
		files = request.files
		print(files)
		for file in files:
			f = files[file]
			UPLOAD_NAME = secure_filename(f.filename)
			f.save(os.path.join(c.RECORDS+"/objects/webrep/",UPLOAD_NAME ))
		last_row_id = db.do(sql)
		return last_row_id


	@app.route("/webrep/article/get_img/<img>",methods=["POST","GET"])
	def get_img(img):
		print(img)
		img = img.replace('C:fakepath', '').replace(" ","_").replace(")","").replace("(","")
		print(img)
		return send_file(c.RECORDS+"/objects/webrep/"+img)

	# ======================================================================================================

	@app.app_errorhandler(404)
	def _404(err):
		return render_template("error/404.html"), 404

	def get_all_user():
		users = db.select("SELECT * FROM `users`;")
		return users


	def moderator(segment,page):
		pass;
	#sample EDIT

