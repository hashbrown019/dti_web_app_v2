from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json

from v2_view.core import dash_api
from v2_view.core import dash_script
from v2_view.core import _backend_sub


app = Blueprint("form_a_v2",__name__,template_folder='pages')

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)
# rapid= sqlite("assets\\db\\dti_rapidxi.db")
# rapid= sqlite(c.SQLITE_DB)

rapid_mysql = mysql(*c.DB_CRED)

class _main:
	def __init__(self, arg):
		super(_main, self).__init__()
		self.arg = arg

	def is_on_session(): return ('USER_DATA' in session)
	@app.route("/mis-v4/<module>",methods=["POST","GET"])
	@c.login_auth_web()
	def core_home_page(module):
		if(session["USER_DATA"][0]['security_group']==0): return redirect("/warning?type=user-no-role");
		module = f'chunks{"/"+"-".join(module.split("-")[1:])}/{module}.html'
		# return (f" - Loading Moule : {module}")
		print("Current Module ["+module+"]")
		return render_template(
			f"chunks/core.html",
			module=module,
			URL_ARGS=request.args,
			USER_DATA = session["USER_DATA"][0],
			staff_list=dash_api.get_area_staff(),
			databases=dash_api.get_databases(),
			security_group_ls=dash_api.get_security_group() if "core-system-control" in module else None ,
			personal_forms=dash_api.get_personal_forms(session["USER_DATA"][0]['id']) if "core-personal-forms" in module else None ,
			specific_forms=dash_api.get_personal_forms(session["USER_DATA"][0]['id']) if "tools-trackers-specific" in module else None 
		);


	@app.route("/warning",methods=["GET"])
	def system_page():
		_type = request.args['type']
		sql = 'SELECT * FROM `users` WHERE `rcu` = "{}" AND `security_group` = "26";'.format(session["USER_DATA"][0]['rcu'])
		print(sql)
		res = rapid_mysql.select(sql)
		return render_template("/chunks/system-pages/core-system-pages.html",type=_type, USER_DATA = session["USER_DATA"][0],_admin=res)
	# ==========================================================================================	
	# ==========================================================================================	
	# ==========================================================================================	
	# ==========================================================================================	
	# ==========================================================================================	

	

	# =======================================
	# =======================================
	# ============USER-MANAGEMENT============

	@app.route("/mis-v4/user-management/<task>",methods=["POST","GET"])
	@c.login_auth_web()
	def user_profile_edit(task):
		if(task=='edit'): res = _backend_sub.user_pofile.edit_user_profile(request)
		elif(task=='editpic'):res =  _backend_sub.user_pofile.edit_user_profilepic(request)
		elif(task=='editpass'):res =  _backend_sub.user_pofile.edit_user_profilepass(request)
		# return res
		# return redirect("/logout?urlvisit=/mis-v4/core-user-profile")
		return redirect("/mis-v4/core-system-control")

	@app.route("/api/user_pic/<file_name>")
	@app.route("/mis-v4/user-management/user_pic/<file_name>")
	def get_user_pic(file_name):
		try:
			return send_file(c.RECORDS+"objects/userpics/"+file_name, as_attachment=False,download_name=file_name)
		except Exception as e:
			return send_file(c.RECORDS+"objects/userpics/profilepic.png", as_attachment=False,download_name=file_name)

	# =======================================
	# =======================================
	# ============USER-CONTROL===============

	@app.route("/mis-v4/system-control/<task>",methods=["POST","GET"])
	@c.login_auth_web()
	def add_sec_group(task):
		if(task=='add-security-group'): res = _backend_sub.system_settings.add_user_group(request)
		elif(task=='get-staff-info'): res = _backend_sub.system_settings.get_staff_info(request)
		return res

	# =======================================
	# =======================================
	# =========PERSONAL-FORM=================
	@app.route("/mis-v4/personal-forms/<task>",methods=["POST","GET"])
	@c.login_auth_web()
	def personal_forms(task):
		if(task=='get-template'): res = _backend_sub.personal_forms.get_template(request)
		if(task=='save-temp'): res = _backend_sub.personal_forms.save_template(request)
		if(task=='save-data'): res = redirect(_backend_sub.personal_forms.save_data(request)["__url_referrer"])
		if(task=='get-data'): res = dash_api.get_temp_data(request)
		if(task=='get-db-col'): res = dash_api.get_get_db_col(request)
		if(task=='add-collection'): res = dash_api.add_to_collection(request)
		return res

	@app.route("/public/<module>",methods=["POST","GET"])
	def public_form(module):
		return render_template(
			"/chunks/public-form/core-public-form.html",
			form=module,
			personal_forms=dash_api.get_public_form(module)[0],
			USER_DATA = {"id":"9999999","name":"Guest"}
			# URL_ARGS=request.args,
			)

	# =======================================
	# =========GET-SESSION===================
	@app.route("/mis-v4/get-session",methods=["POST","GET"])
	@c.login_auth_web()
	def test():
		return session["USER_DATA"]
	# @app.route("/form_a_home/<page>",methods=["POST","GET"])
	# @c.login_auth_web()
	# def form_a_home_page(page):
	# 	return render_template(f"__page_content/{page}.html",USER_DATA = session["USER_DATA"][0])

	@app.route("/test")
	def sample():
		return dash_api.get_area_staff()