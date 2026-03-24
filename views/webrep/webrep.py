from flask import Blueprint, flash, render_template, request, session, redirect, jsonify, send_file, Response
from flask_session import Session
from modules.Connections import mysql
from modules.Req_Brorn_util import string_websafe as STRS
import Configurations as c
from werkzeug.utils import secure_filename
import os
from modules.Req_Brorn_util import file_from_request

# from PIL import Image
from io import BytesIO
import base64
import json

from datetime import date, datetime
from modules.Req_Brorn_util import file_from_request

from v2_view.core._dashboard import _main as dboard_main

# from docx2pdf import convert
# pip install docx2pdf

db = mysql(*c.DB_CRED)
db.err_page = 0

app = Blueprint("webrep",__name__,template_folder='pages')
# app = Blueprint("webrep",__name__,url_prefix='/webrep',template_folder='pages')

# app.register_blueprint(_dashboard.app)

class _main:
	def is_on_session(): return ('USER_DATA' in session)

	def __init__(self, arg):super(_main, self).__init__();self.arg = arg

	# app.errorhandler(404)
	# def is_on_session(): return ('USER_DATA' in session)

	# ======================================================================================================
	@app.route("/__test",methods=["POST","GET"])
	def __test():
		return render_template(
			"v2_home/home.html",
			page_data=_main.get_post()
		)
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
		# dashboard_data =  json.loads(dboard_main.system_page())
		# dashboard_data =  dboard_main.system_page()
		return render_template(
			"home/home.html",
			page_data=_main.get_post(),
			is_session =_main.is_on_session(),
			dashboard_data=_main.analyticUpdates()
		)
 
	@app.route("/rapid/<_>",methods=["POST","GET"])
	def home_(_):
		if(_!="home/home.html"): 
			return _main._404(404)
		return render_template(
			"home/home.html"
		)

	@app.route("/rapid/get_file_list",methods=["POST","GET"])
	def get_file_list():
		PATH = c.RECORDS+"../static/pdf/MEEGuide"
		directory = os.fsencode(PATH)
		_FILES_MEE = []
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			_FILES_MEE.append("{}".format(str(filename)))

		PATH = c.RECORDS+"../static/pdf/procurement"
		directory = os.fsencode(PATH)
		_FILES_PROC = []
		for file in os.listdir(directory):
			filename = os.fsdecode(file)
			_FILES_PROC.append("{}".format(str(filename)))


		return {"mee":_FILES_MEE,"proc":_FILES_PROC}		


	# ===========================================================/
	# ===========================================================/
	# ===========================================================/
	# ===========================================================/
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
			page.lower()=="printcs.html".lower()  or
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
		return send_file(c.RECORDS+"../static/"+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

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

		FILE_REQ = file_from_request(app)
		__f = FILE_REQ.save_file_from_request(request,"photos",c.RECORDS+"/objects/webrep/",False,True)
		data["photos"] = __f["file_arr_str"]

		is_exist = len(db.select("SELECT * FROM `webrep_case_study` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding Articles")
			for datum in data:
				# print(datum)
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `webrep_case_study` ({},`status`) VALUES ({},'Submitted')'''.format(", ".join(key),", ".join(val)))
		
		else:
			print(" >> Editing Articles")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `webrep_case_study` SET  {}, `status`='Submitted' WHERE `id`='{}';".format(args[1:],request.form['id'])
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
		# im = Image.open(c.RECORDS+"/objects/webrep/"+img)

		# buff = BytesIO()
		# im.save(buff, format="JPEG")
		# img_str = base64.b64encode(buff.getvalue())
		# string = ''.join(map(chr, img_str)) ###### CONVERT BYTES to STRING

		# fff=open("__temp__/_.txt","w")
		# fff.write("data:image/png;base64,{}".format(string))
		# fff.close()
		# return send_file("__temp__/_.txt".format(string))

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

	@app.route("/embed_forum_talks/<f_id>",methods=["POST","GET"])
	def embed_forum_talks(f_id):
		if(_main.is_on_session()):
			forum = db.select("SELECT `webrep_forum_topics`.*, `users`.`name` as 'uploader', `users`.`profilepic`, `users`.`job` FROM `webrep_forum_topics` INNER JOIN `users` ON `webrep_forum_topics`.`created_by`= `users`.`id` WHERE `webrep_forum_topics`.`id`='{}';".format(f_id))
			return render_template(
				'forum/embed_forum.html',
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
			comments = db.select("SELECT `webrep_forum_comments`.*, `users`.`name` as 'commenter', `users`.`id` as 'commenter_id', `users`.`profilepic` as 'profilepic', `users`.`job` FROM `webrep_forum_comments` INNER JOIN `users` ON `webrep_forum_comments`.`comment_by`= `users`.`id` WHERE `webrep_forum_comments`.`topic_id`='{}' ORDER BY `id` DESC;".format(com_id))
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
		print("moderator init")
		pass;
	#sample EDIT

	def analyticUpdates():
    	
		# ======================================================================================================
        # SMALL HOLDER FARMERS
    	# ======================================================================================================
		SHF_Total = db.select("SELECT COUNT(*) AS total FROM excel_import_form_a")
		SHF_Total_Male = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_Sex`='Male'")
		SHF_Total_Female = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_Sex`='Female'")
		SHF_Total_IP = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='IP'")
		SHF_Total_Youth = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='Youth'")
		SHF_Total_PWD = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='PWD'")
		SHF_Total_SC = db.select("SELECT COUNT(*) AS total FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='SC'")

		SHF_byRegion_8 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('8','xiii','region8','region 8')")
		SHF_byRegion_9 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('9','ix','region9','region 9')")
		SHF_byRegion_10 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('10','x','region10','region 10')")
		SHF_byRegion_11 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('11','xi','region11','region 11')")
		SHF_byRegion_12 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('12','xii','region12','region 12')")
		SHF_byRegion_13 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('13','xiii','region13','region 13')")
		SHF_byRegion_barmm = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('BARMM')")
        
		SHF_allRegion = [float(SHF_byRegion_8[0]['percTotal']),float(SHF_byRegion_9[0]['percTotal']),float(SHF_byRegion_10[0]['percTotal']),float(SHF_byRegion_11[0]['percTotal']),float(SHF_byRegion_12[0]['percTotal']),float(SHF_byRegion_13[0]['percTotal']),float(SHF_byRegion_barmm[0]['percTotal'])]

		SHF_byComm_cacao = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cacao%'")
		SHF_byComm_coconut = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coconut%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Copra%'")
		SHF_byComm_coffee = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coffee%'")
		SHF_byComm_pfn = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%BananaCardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Calamansi%'")
		SHF_byComm_untagged = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cacao%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coconut%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Copra%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coffee%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%BananaCardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Calamansi%'")

		SHF_byComm_data = [SHF_byComm_cacao[0]['total'],SHF_byComm_coconut[0]['total'],SHF_byComm_coffee[0]['total'],SHF_byComm_pfn[0]['total'],SHF_byComm_untagged[0]['total']]
		
		SHF_total_HH_head_male = db.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` = 'Male' WHERE dl.db_table='dcf_capacity_building'")
		SHF_total_HH_head_female = db.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` = 'Female' WHERE dl.db_table='dcf_capacity_building'")
		SHF_total_HH_head_untagged = db.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` != 'Male' AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` != 'Female' WHERE dl.db_table='dcf_capacity_building'")
		
		SHF_total_HH_head_data = [SHF_total_HH_head_male[0]['total'],SHF_total_HH_head_female[0]['total'],SHF_total_HH_head_untagged[0]['total']];


		# ======================================================================================================
        # FARMER ORGANIZATION
    	# ======================================================================================================
		FO_Total = db.select("SELECT COUNT(*) AS total FROM form_b")
		FO_Total_Coop = db.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Cooperative'")
		FO_Total_Assoc = db.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Association'")
		FO_Total_Others = db.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Others'")
		FO_Total_Members = db.select("SELECT SUM(organizational_total_overall) AS total FROM form_b")
		FO_Total_Male = db.select("SELECT SUM(organizational_total_male) AS total FROM form_b ")
		FO_Total_Female = db.select("SELECT SUM(organizational_total_female) AS total FROM form_b ")

		FO_byRegion_8 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU8','RCU 8')")
		FO_byRegion_9 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU9','RCU 9')")
		FO_byRegion_10 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU10','RCU 10')")
		FO_byRegion_11 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU11','RCU 11')")
		FO_byRegion_12 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU12','RCU 12')")
		FO_byRegion_13 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU13','RCU 13')")
		FO_byRegion_barmm = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('BARMM')")
        
		FO_allRegion = [float(FO_byRegion_8[0]['percTotal']),float(FO_byRegion_9[0]['percTotal']),float(FO_byRegion_10[0]['percTotal']),float(FO_byRegion_11[0]['percTotal']),float(FO_byRegion_12[0]['percTotal']),float(FO_byRegion_13[0]['percTotal']),float(FO_byRegion_barmm[0]['percTotal'])]
		FO_byOrgType = [FO_Total_Assoc[0]['total'],FO_Total_Coop[0]['total'],FO_Total_Others[0]['total']]
        
		FO_byComm_cacao = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Cacao%'")
		FO_byComm_coconut = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Coconut%' OR `organizational_commodity` LIKE '%Copra%'")
		FO_byComm_coffee = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Coffee%'")
		FO_byComm_pfn = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Banana%' OR `organizational_commodity` LIKE '%Banana Cardava%' OR `organizational_commodity` LIKE '%BananaCardava%' OR `organizational_commodity` LIKE '%Cardava%' OR `organizational_commodity` LIKE '%Calamansi%'")
		FO_byComm_untagged = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` NOT LIKE '%Cacao%' AND `organizational_commodity` NOT LIKE '%Coconut%' AND `organizational_commodity` NOT LIKE '%Copra%' AND `organizational_commodity` NOT LIKE '%Coffee%' AND `organizational_commodity` NOT LIKE '%Banana%' AND `organizational_commodity` NOT LIKE '%Banana Cardava%' AND `organizational_commodity` NOT LIKE '%BananaCardava%' AND `organizational_commodity` NOT LIKE '%Cardava%' AND `organizational_commodity` NOT LIKE '%Calamansi%'")

		FO_byComm_data = [FO_byComm_cacao[0]['total'],FO_byComm_coconut[0]['total'],FO_byComm_coffee[0]['total'],FO_byComm_pfn[0]['total'],FO_byComm_untagged[0]['total']]

		# ======================================================================================================
        # MICRO, SMALL, MEDIUM ENTERPRISES
    	# ======================================================================================================
		MSME_Total = db.select("SELECT COUNT(*) AS total FROM form_c")[0]['total']

		MSME_byRegion_8 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU8','RCU 8')")
		MSME_byRegion_9 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU9','RCU 9')")
		MSME_byRegion_10 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU10','RCU 10')")
		MSME_byRegion_11 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU11','RCU 11')")
		MSME_byRegion_12 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU12','RCU 12')")
		MSME_byRegion_13 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU13','RCU 13')")
		MSME_byRegion_barmm = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('BARMM')")

		MSME_allRegion = [float(MSME_byRegion_8[0]['percTotal']),float(MSME_byRegion_9[0]['percTotal']),float(MSME_byRegion_10[0]['percTotal']),float(MSME_byRegion_11[0]['percTotal']),float(MSME_byRegion_12[0]['percTotal']),float(MSME_byRegion_13[0]['percTotal']),float(MSME_byRegion_barmm[0]['percTotal'])]
        
		MSME_byComm_cacao = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Cacao%'")
		MSME_byComm_coconut = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Coconut%' OR `industry_cluster` LIKE '%Copra%'")
		MSME_byComm_coffee = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Coffee%'")
		MSME_byComm_pfn = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Banana%' OR `industry_cluster` LIKE '%Banana Cardava%' OR `industry_cluster` LIKE '%BananaCardava%' OR `industry_cluster` LIKE '%Cardava%' OR `industry_cluster` LIKE '%Calamansi%'")
		MSME_byComm_untagged = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` NOT LIKE '%Cacao%' AND `industry_cluster` NOT LIKE '%Coconut%' AND `industry_cluster` NOT LIKE '%Copra%' AND `industry_cluster` NOT LIKE '%Coffee%' AND `industry_cluster` NOT LIKE '%Banana%' AND `industry_cluster` NOT LIKE '%Banana Cardava%' AND `industry_cluster` NOT LIKE '%BananaCardava%' AND `industry_cluster` NOT LIKE '%Cardava%' AND `industry_cluster` NOT LIKE '%Calamansi%'")
		MSME_byComm_data = [MSME_byComm_cacao[0]['total'],MSME_byComm_coconut[0]['total'],MSME_byComm_coffee[0]['total'],MSME_byComm_pfn[0]['total'],MSME_byComm_untagged[0]['total']]

		MSME_byType_micro = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Micro','Micro (3M below)')")
		MSME_byType_small = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Small','Small (3-15M)')")
		MSME_byType_medium = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Medium','Medium (15.1M-100M)')")
		MSME_byType_large = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Large','Large (Above 100M)')")
		MSME_byType_data = [MSME_byType_micro[0]['total'],MSME_byType_small[0]['total'],MSME_byType_medium[0]['total'],MSME_byType_large[0]['total']]
	
		background_colors = ["#629DDD","#A4BF7F","#A48BC1","#E2918F","#F4D470","#E8AA78","#A5D7D8","#7173A9","#77838E"]
        
		data = {
                "SHF_Total" : SHF_Total[0]["total"],
                "SHF_Total_Male" : SHF_Total_Male[0]["total"],
                "SHF_Total_Female" : SHF_Total_Female[0]["total"],
                "SHF_Total_IP" : SHF_Total_IP[0]["total"],
                "SHF_Total_PWD" : SHF_Total_PWD[0]["total"],
                "SHF_Total_Youth" : SHF_Total_Youth[0]["total"],
                "SHF_Total_SC" : SHF_Total_SC[0]["total"],
				"SHF_byRegion" : SHF_allRegion,
				"SHF_byComm" : SHF_byComm_data,
				"SHF_byHHHead" : SHF_total_HH_head_data,
				"FO_Total" : FO_Total[0]["total"],
                "FO_Total_Coop" : FO_Total_Coop[0]["total"],
                "FO_Total_Assoc" : FO_Total_Assoc[0]["total"],
                "FO_Total_Members" : FO_Total_Members[0]["total"],
                "FO_Total_Male" : FO_Total_Male[0]["total"],
                "FO_Total_Female" : FO_Total_Female[0]["total"],
				"FO_byRegion" : FO_allRegion,
				"FO_byOrgType" : FO_byOrgType,
				"FO_byComm" : FO_byComm_data,
				"MSME_Total" : MSME_Total,
				"MSME_byRegion" : MSME_allRegion,
				"MSME_byComm" : MSME_byComm_data,
				"MSME_byType" : MSME_byType_data,
			}
		
		return data