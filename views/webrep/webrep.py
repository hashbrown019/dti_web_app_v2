from flask import Blueprint, render_template, request, session, redirect, jsonify
from flask_session import Session
from modules.Connections import mysql
import Configurations as c

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
		return render_template("home.html")

	@app.route("/rapid/<_>",methods=["POST","GET"])
	def home_(_):
		if(_!="home.html"):
			return _main._404(404)
		return render_template("home.html")
	# ===========================================================/

	@app.route("/rapid/<segment>/<page>",methods=["POST","GET"])
	def page_loader(segment,page):
		if(page.lower()=="knowledgeAdmin.html".lower()):
			if(_main.is_on_session()):
			    return render_template("{}/{}".format(segment,page),users=_main.get_all_user(),is_session =_main.is_on_session(),user_data=session["USER_DATA"][0])
			else:
			    return redirect("/login?force_url=1")
		_main.moderator(segment,page)
		return render_template("{}/{}".format(segment,page),is_session =_main.is_on_session())
	# ==================================================================


	@app.app_errorhandler(404)
	def _404(err):
		return render_template("error/404.html"), 404

	def get_all_user():
		users = db.select("SELECT * FROM `users`;")
		return users


	def moderator(segment,page):
		pass;
	#sample EDIT

