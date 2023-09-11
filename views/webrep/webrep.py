from flask import Blueprint, flash, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql
from modules.Req_Brorn_util import string_websafe as STRS
import Configurations as c
from werkzeug.utils import secure_filename
import os

from datetime import date, datetime
from modules.Req_Brorn_util import file_from_request

db = mysql(*c.DB_CRED)
db.err_page = 0

app = Blueprint("webrep",__name__,template_folder='pages')
# app = Blueprint("webrep",__name__,url_prefix='/webrep',template_folder='pages')

class _main:
	def is_on_session(): return ('USER_DATA' in session)

	def __init__(self, arg):super(_main, self).__init__();self.arg = arg

	# app.errorhandler(404)
	# def is_on_session(): return ('USER_DATA' in session)

	# ======================================================================================================
	@app.route("/webrep",methods=["POST","GET"])
	def home():
		if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
		print("databse = "+c.DB_CRED[3])
		db = mysql(*c.DB_CRED)
		return redirect("/hi_there?ver=dti_rapidgrowth_"+c.DB_CRED[3])

	@app.route("/hi_there",methods=["POST","GET"])
	def hi_there():
		if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
		return render_template(
			"home/home.html",
			page_data=_main.get_post()
		)
 
	@app.route("/rapid/<_>",methods=["POST","GET"])
	def home_(_):
		if(_!="home/home.html"): 
			return _main._404(404)
		return render_template(
			"home/home.html"
		)
	# ===========================================================/
	# ===========================================================/
	# ===========================================================/
	# ===========================================================/
	# ===========================================================/

	@app.route("/rapid/<segment>/<page>",methods=["POST","GET"])
	def page_loader(segment,page):
		print(" * Page Loaded : {}".format(page.lower()))
		if(page.lower()=="adminKnowledgecenter.html".lower() or
			page.lower()=="superadmin.html".lower()
			):
			sesh_ = [{"id":"none"}]
			if(_main.is_on_session()):
				sesh_ = session["USER_DATA"]
			return render_template(
				"{}/{}".format(segment,page),
				users=_main.get_all_user(),
				is_session =_main.is_on_session(),
				user_data=sesh_[0],
				# user_data=session["USER_DATA"][0],
				upload_file_webrep=_main.get_uploads_docs(),
				module_data = _main.get_module_data(),
				articles = _main.get_uploads_article(),
				case_studies = _main.get_case_studies()
				)
		# if(page.lower()=="adminKnowledgecenter.html".lower() or
		# 	page.lower()=="superadmin.html".lower()
		# 	):
		# 	if(_main.is_on_session()):
		# 		return render_template(
		# 			"{}/{}".format(segment,page),
		# 			users=_main.get_all_user(),
		# 			is_session =_main.is_on_session(),
		# 			user_data=session["USER_DATA"][0],
		# 			upload_file_webrep=_main.get_uploads_docs(),
		# 			module_data = _main.get_module_data(),
		# 			articles = _main.get_uploads_article()
		# 			)
		# 	else:
		# 		return redirect("/login?force_url=1")
		elif(
			page.lower()=="document.html".lower() or 
			page.lower()=="multimedia.html".lower() or 
			page.lower()=="publication.html".lower()  or
			page.lower()=="createCaseStudy.html".lower()  or
			page.lower()=="createPost.html".lower()
			):
			if(_main.is_on_session()):
				return render_template(
					"{}/{}".format(segment,page),
					users=_main.get_all_user(),
					is_session =_main.is_on_session(),
					user_data=session["USER_DATA"][0])
			else:
				return redirect("/login?force_url=1")
		elif(
			page.lower()=="newsandstories.html".lower() or 
			page.lower()=="home.html".lower() or 
			page.lower()=="news.html".lower()or
			page.lower()=="articles.html".lower() or
			page.lower()=="events.html".lower() or
			page.lower()=="stories.html".lower()
			):
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
	# ==================================================================
	# ==================================================================
	# ==================================================================
	# ==================================================================
	# ==================================================================
	# ==================================================================
	# ==================================================================
	# ==================================================================

	@app.route("/webrep/check_pass",methods=["POST","GET"])
	def check_pass():
		print(request.form["pass"]+" == "+session["USER_DATA_ADMIN_"][0]["password"])
		if(request.form["pass"]==session["USER_DATA_ADMIN_"][0]["password"]):
			return {"status":"success","dl_path":"/webrep/upload/get_file_download/{}".format(request.form["fileName"])}
		else:
			return {"status":"failed","dl_path":""}

	@app.route("/webrep/upload/get_file_download",methods=["POST","GET"])
	def get_file_download():
		return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

	@app.route("/webrep/article/get_post",methods=["POST","GET"])
	def get_post():
		return db.select("SELECT * from `webrep_articles` WHERE `removed`='0' ORDER BY `id` DESC;")

	@app.route("/webrep/article/get_post_ind",methods=["POST","GET"])
	def get_post_ind():
		ids = request.form['id']
		return db.select("SELECT * from `webrep_articles` WHERE `id`='{}' ORDER BY `id` DESC;".format(ids))
		# return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

	@app.route("/webrep/case_study/get_post_ind",methods=["POST","GET"])
	def case_study_get_post_ind():
		ids = request.form['id']
		SQL = "SELECT * from `webrep_case_study` WHERE `id`='{}' ORDER BY `id` DESC;".format(ids)
		return db.select(SQL)
		# return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)
	@app.route("/webrep/get_case_studies",methods=["POST","GET"])
	def get_case_studies():
		return db.select("SELECT * from `webrep_case_study`  WHERE `removed`='0' ORDER BY `id` DESC;")

	@app.route("/webrep/uploads/docs",methods=["POST","GET"])
	def get_uploads_docs():
		return db.select("SELECT * from `webrep_uploads`  WHERE `removed`='0' ORDER BY `id` DESC;")


	@app.route("/webrep/uploads/article",methods=["POST","GET"])
	def get_uploads_article():
		return db.select("SELECT * from `webrep_articles`  WHERE `removed`='0' ORDER BY `id` DESC;")

	@app.route("/webrep/uploads/docs_item",methods=["POST","GET"])
	def get_uploads_docs_item():
		ids = request.form['ids']
		file = db.select("SELECT * from `webrep_uploads`WHERE `id`='{}';".format(ids))
		uploaded_by = db.select("SELECT * from `users`WHERE `id`='{}';".format(file[0]['uploaded_by']))
		file[0]['uploaded_by'] = uploaded_by[0]
		return file

	# @app.route("/webrep/upload_file_webrep",methods=["POST","GET"])
	# def upload_file_webrep():
	# 	print("MAONINIININIn")
	# 	from datetime import date, datetime
	# 	data = dict(request.form)
	# 	key = [];val = []
	# 	data["USER_ID"] = session["USER_DATA"][0]['id']

		
	# 	for datum in data:
	# 		key.append("`{}`".format(datum))
	# 		val.append("'{}'".format(STRS.encode_websafe(data[datum])))
	# 	sql = ('''INSERT INTO `webrep_articles` (`status`,{}) VALUES ('pending',{})'''.format(", ".join(key),", ".join(val)))
		
	# 	files = request.files
	# 	print(files)
	# 	for file in files:
	# 		f = files[file]
	# 		UPLOAD_NAME = secure_filename(f.filename)
	# 		f.save(os.path.join(c.RECORDS+"/objects/webrep/",UPLOAD_NAME ))
	# 	last_row_id = db.do(sql)
	# 	return last_row_id

	@app.route("/webrep/upload_file_webrep",methods=["POST","GET"])
	def upload_file_webrep():
		print("  * Article Module")
		from datetime import date, datetime
		from modules.Req_Brorn_util import file_from_request
		FILE_REQ = file_from_request(app)
		data = dict(request.form)
		key = [];val = [];args=""
		data["USER_ID"] = session["USER_DATA"][0]['id']


		__f = FILE_REQ.save_file_from_request(request,"file_name",c.RECORDS+"/objects/webrep/",False,True)
		data["file_name"] = __f["file_arr_str"]

		is_exist = len(db.select("SELECT * FROM `webrep_articles` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding Articles")
			for datum in data:
				# print(datum)
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `webrep_articles` ({},`status`) VALUES ({},'pending')'''.format(", ".join(key),", ".join(val)))
		
		else:
			print(" >> Editing Articles")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `webrep_articles` SET  {}, `status`='pending' WHERE `id`='{}';".format(args[1:],request.form['id'])
			pass
		
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id,"FILES":__f})

	@app.route("/webrep/upload_case_study",methods=["POST","GET"])
	def upload_case_study():
		print("  * Article Module")
		from datetime import date, datetime
		from modules.Req_Brorn_util import file_from_request
		data = dict(request.form)
		key = [];val = [];args=""
		data["USER_ID"] = session["USER_DATA"][0]['id']


		# FILE_REQ = file_from_request(app)
		# __f = FILE_REQ.save_file_from_request(request,"file_name",c.RECORDS+"/objects/webrep/",False,True)
		# data["file_name"] = __f["file_arr_str"]

		is_exist = len(db.select("SELECT * FROM `webrep_case_study` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding Articles")
			for datum in data:
				# print(datum)
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `webrep_case_study` ({},`status`) VALUES ({},'pending')'''.format(", ".join(key),", ".join(val)))
		
		else:
			print(" >> Editing Articles")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `webrep_case_study` SET  {}, `status`='pending' WHERE `id`='{}';".format(args[1:],request.form['id'])
			pass
		
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id})
		# return jsonify({"last_row_id":last_row_id,"FILES":__f})
 
	@app.route("/webrep/upload_file_webrep___",methods=["POST","GET"])
	def upload_file_webrep___():
		print("  * Upload Module")
		FILE_REQ = file_from_request(app)
		data = dict(request.form)
		key = [];val = [];args=""
		data["USER_ID"] = session["USER_DATA"][0]['id']


		__f = FILE_REQ.save_file_from_request(request,"upload",c.RECORDS+"/objects/webrep/",False,True)
		data["upload"] = __f["file_arr_str"]

		is_exist = len(db.select("SELECT * FROM `webrep_uploads` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding Uploads")
			for datum in data:
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `webrep_uploads` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
		
		else:
			print(" >> Editing Uploads")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `webrep_uploads` SET  {}, `status`='pending' WHERE `id`='{}';".format(args[1:],request.form['id'])
			pass
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id,"FILES":__f})
 
	@app.route("/webrep/article/get_img/<img>",methods=["POST","GET"])
	def get_img(img):
		img = img.replace('C:fakepath', '').replace(" ","_").replace(")","").replace("(","")
		return send_file(c.RECORDS+"/objects/webrep/"+img)


	@app.route("/webrep/delete_record/<table>/<ids>",methods=["POST","GET"])
	def delete_record(table,ids):
		__table = {"docs":"webrep_uploads","mul":"webrep_uploads","pub":"webrep_uploads"}
		update_del = db.do("UPDATE `{}` SET `removed`='1' WHERE `id`='{}';".format(__table[table],ids))
		return {"db_info":update_del}

	@app.route("/webrep/status_records/<table>/<ids>",methods=["POST","GET"])
	def status_records(table,ids):
		__table = {"docs":"webrep_uploads","mul":"webrep_uploads","pub":"webrep_uploads"}
		update_del = db.do("UPDATE `{}` SET `status`='revise' WHERE `id`='{}';".format(__table[table],ids))
		return {"db_info":update_del}

	@app.route("/webrep/confirm_records/<table>/<ids>",methods=["POST","GET"])
	def confirm_records(table,ids):
		__table = {"docs":"webrep_uploads","mul":"webrep_uploads","pub":"webrep_uploads"}
		update_del = db.do("UPDATE `{}` SET `status`='posted' WHERE `id`='{}';".format(__table[table],ids))
		return {"db_info":update_del}

	@app.route("/webrep/download_file/<table>/<ids>",methods=["POST","GET"])
	def download_excel(table,ids):
		__table = {"docs":"webrep_uploads","mul":"webrep_uploads","pub":"webrep_uploads"}
		res = db.select("SELECT `upload` FROM `{}` WHERE `id`='{}';".format(__table[table],ids))
		return {"file_to_dl":res[0]['upload']}
		# return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+file, as_attachment=True,download_name=file)

	@app.route("/webrep/articles/delete/<ids>",methods=["POST","GET"])
	def delete_article(ids):
		update_del = db.do("UPDATE `webrep_articles` SET `removed`='1' WHERE `id`='{}';".format(ids))
		return {"db_info":update_del}

	@app.route("/webrep/articles/confirm/<ids>",methods=["POST","GET"])
	def confirm_article(ids):
		update_del = db.do("UPDATE `webrep_articles` SET `status`='posted' WHERE `id`='{}';".format(ids))
		return {"db_info":update_del}

	@app.route("/webrep/articles/revise/<ids>",methods=["POST","GET"])
	def revise_article(ids):
		update_del = db.do("UPDATE `webrep_articles` SET `status`='revise' WHERE `id`='{}';".format(ids))
		return {"db_info":update_del}

	@app.route("/webrep/go_dl_file/<filename>",methods=["POST","GET"])
	def go_dl_file(filename):
		return send_file(c.RECORDS+"/objects/webrep/"+filename , as_attachment=True,download_name=filename )


	def get_module_data():
		_modules = db.select("SELECT * FROM `__modules`;")
		return _modules
	# ======================================================================================================

	@app.route("/forum",methods=["POST","GET"])
	def forum_index():
		if(_main.is_on_session()):
			forums = db.select("SELECT `webrep_forum_topics`.*, `users`.`name` as 'uploader' FROM `webrep_forum_topics` INNER JOIN `users` ON `webrep_forum_topics`.`created_by`= `users`.`id`;")
			return render_template(
				'forum/forum_index.html',
				USER_DATA = session['USER_DATA'][0],
				forum_ls = forums
				)
		else:
			return redirect("/login?force_url=1")


	@app.route("/forum_talks/<f_id>",methods=["POST","GET"])
	def forum_talks(f_id):
		if(_main.is_on_session()):
			forum = db.select("SELECT `webrep_forum_topics`.*, `users`.`name` as 'uploader', `users`.`profilepic`, `users`.`job` FROM `webrep_forum_topics` INNER JOIN `users` ON `webrep_forum_topics`.`created_by`= `users`.`id` WHERE `webrep_forum_topics`.`id`='{}';".format(f_id))
			return render_template(
				'forum/forum_discussion.html',
				USER_DATA = session['USER_DATA'][0],
				forum = forum[0]
				)
		else:
			return redirect("/login?force_url=1")


	@app.route("/forum/save_forum",methods=["POST","GET"])
	def save_forum():
		print("  * save_forum")
		FILE_REQ = file_from_request(app)
		data = dict(request.form)
		key = [];val = [];args=""

		is_exist = len(db.select("SELECT * FROM `webrep_forum_topics` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding Forum")
			for datum in data:
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `webrep_forum_topics` ({},`status`) VALUES ({},'pending')'''.format(", ".join(key),", ".join(val)))
		else:
			print(" >> Editing Forum")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `webrep_forum_topics` SET  {}, `status`='pending' WHERE `id`='{}';".format(args[1:],request.form['id'])
			pass
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/forum/send_comment",methods=["POST","GET"])
	def send_comment():
		print("  * send_comment")
		FILE_REQ = file_from_request(app)
		data = dict(request.form)
		key = [];val = [];args=""

		is_exist = len(db.select("SELECT * FROM `webrep_forum_comments` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding Forum")
			for datum in data:
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `webrep_forum_comments` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
		else:
			print(" >> Editing Forum")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `webrep_forum_comments` SET  {}, `edit`='1' WHERE `id`='{}';".format(args[1:],request.form['id'])
			pass
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/forum/send_comment_like/<com_id>",methods=["POST","GET"])
	def send_comment_like(com_id):
		sql = "UPDATE `webrep_forum_comments` SET `likes` = `likes` + 1 WHERE `id`='{}';".format(com_id)
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/forum/delete_comment/<com_id>",methods=["POST","GET"])
	def delete_comment(com_id):
		sql = "UPDATE `webrep_forum_comments` SET `removed`='1' WHERE `id`='{}';".format(com_id)
		last_row_id = db.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/forum/get_comment/<com_id>",methods=["POST","GET"])
	def get_comment(com_id):
		if(_main.is_on_session()):
			comments = db.select("SELECT `webrep_forum_comments`.*, `users`.`name` as 'commenter', `users`.`profilepic` as 'profilepic', `users`.`job` FROM `webrep_forum_comments` INNER JOIN `users` ON `webrep_forum_comments`.`comment_by`= `users`.`id` WHERE `webrep_forum_comments`.`topic_id`='{}';".format(com_id))
			return [comments,_main.get_topic_people(com_id)]
		else:
			return redirect("/login?force_url=1")

	@app.route("/forum/get_topic_people/<com_id>",methods=["POST","GET"])
	def get_topic_people(com_id):
		if(_main.is_on_session()):
			comments = db.select("SELECT `webrep_forum_comments`.`id` as 'first_comment_id', `users`.`name` as 'commenter' FROM `webrep_forum_comments` INNER JOIN `users` ON `webrep_forum_comments`.`comment_by` = `users`.`id` WHERE `webrep_forum_comments`.`topic_id` = '{}' GROUP BY `users`.`name`;".format(com_id))
			return comments
		else:
			return redirect("/login?force_url=1")

	@app.app_errorhandler(404)
	def _404(err):
		return render_template("error/404.html"), 404

	@app.route("/webrep/get_user_all",methods=["POST","GET"])
	def get_all_user():
		users = db.select("SELECT * FROM `users`;")
		if(_main.is_on_session()):
			return users
		else:
			return _main._404(404)

	@app.route("/we_will_be_back_later")
	def we_will_be_back_later():
		return render_template("error/maintenance.html")

	def moderator(segment,page):
		pass;
	#sample EDIT

