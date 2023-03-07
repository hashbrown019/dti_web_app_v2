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
		print(" * Page Loaded : {}".format(page.lower()))
		if(page.lower()=="adminKnowledgecenter.html".lower()):
			if(_main.is_on_session()):
				return render_template("{}/{}".format(segment,page),users=_main.get_all_user(),is_session =_main.is_on_session(),user_data=session["USER_DATA"][0],upload_file_webrep=_main.get_uploads_docs())
			else:
				return redirect("/login?force_url=1")
		elif(
			page.lower()=="document.html".lower() or 
			page.lower()=="multimedia.html".lower() or 
			page.lower()=="publication.html".lower()
			# page.lower()=="about.html".lower() or 
			# page.lower()=="NewsAndStories.html".lower()or 
			# page.lower()=="adminKnowledgeCenter.html".lower()or 
			# page.lower()=="knowledgecenter.html".lower()or 
			# page.lower()=="scope.html".lower()or 
			# page.lower()=="news.html".lower()or 
			# page.lower()=="articles.html".lower()
			):
			if(_main.is_on_session()):
				return render_template("{}/{}".format(segment,page),users=_main.get_all_user(),is_session =_main.is_on_session(),user_data=session["USER_DATA"][0])
			else:
				return redirect("/login?force_url=1")
		elif(page.lower()=="newsandstories.html".lower() or page.lower()=="home.html".lower()):
			if("USER_DATA" in session):
				UDATA = session["USER_DATA"][0]
			else:
				UDATA = {"USER_DATA":[{}]}
			return render_template(
				"{}/{}".format(segment,page),
				users=_main.get_all_user(),
				is_session =_main.is_on_session(),
				user_data=UDATA,
				page_data=_main.get_post()
			)
		_main.moderator(segment,page)
		return render_template("{}/{}".format(segment,page),is_session =_main.is_on_session())
	# ==================================================================

	@app.route("/webrep/check_pass",methods=["POST","GET"])
	def check_pass():
		print(request.form["pass"]+" == "+session["USER_DATA"][0]["password"])
		if(request.form["pass"]==session["USER_DATA_ADMIN_"][0]["password"]):
			return {"status":"success","dl_path":"/webrep/upload/get_file_download/{}".format(request.form["fileName"])}
		else:
			return {"status":"failed","dl_path":""}

	@app.route("/webrep/upload/get_file_download",methods=["POST","GET"])
	def get_file_download():
		return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

	@app.route("/webrep/article/get_post",methods=["POST","GET"])
	def get_post():
		return db.select("SELECT * from `webrep_articles`;")
		# return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

	@app.route("/webrep/uploads/docs",methods=["POST","GET"])
	def get_uploads_docs():
		return db.select("SELECT * from `webrep_uploads`;")

	@app.route("/webrep/uploads/docs_item",methods=["POST","GET"])
	def get_uploads_docs_item():
		ids = request.form['ids']
		file = db.select("SELECT * from `webrep_uploads`WHERE `id`='{}';".format(ids))
		uploaded_by = db.select("SELECT * from `users`WHERE `id`='{}';".format(file[0]['uploaded_by']))
		file[0]['uploaded_by'] = uploaded_by[0]
		return file

	@app.route("/webrep/upload_file_webrep",methods=["POST","GET"])
	def upload_file_webrep():
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
 
	@app.route("/webrep/upload_file_webrep___",methods=["POST","GET"])
	def upload_file_webrep___():
		from datetime import date, datetime
		from modules.Req_Brorn_util import file_from_request
		FILE_REQ = file_from_request(app)
		data = dict(request.form)
		key = [];val = []
		data["USER_ID"] = session["USER_DATA"][0]['id']
		# __f = FILE_REQ.save_file_from_request("upload",c.RECORDS+"/objects/webrep/")
		__f = FILE_REQ.save_file_from_request(request,"upload",c.RECORDS+"/objects/webrep/",False,True)
		data["upload"] = __f["file_arr_str"]
		for datum in data:
			print(datum)
			key.append("`{}`".format(datum))
			val.append("'{}'".format(data[datum]))
		sql = ('''INSERT INTO `webrep_uploads` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
		
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id,"FILES":__f})
 
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

