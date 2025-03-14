from modules.Connections import mysql,sqlite
import Configurations as c
from flask import session, send_file
from modules.Req_Brorn_util import file_from_request
from werkzeug.datastructures import MultiDict 
import json, os
from flask import redirect
# from v2_view.core import _socketIO

rapid_mysql = mysql(*c.DB_CRED)
FILE_REQ = file_from_request(c.FLASK_APP)

# ================================================
# ================================================
# ================================================
# ==============USER-PROFILE======================
class user_pofile:
	"""docstring for user_pofile"""
	def __init__(self):
		super(user_pofile, self).__init__()

	def edit_user_profile(req):
		data = dict(req.form)
		key = [];val = [];args=""
		is_exist = len(rapid_mysql.select("SELECT * FROM `users` WHERE `id` ='{}' ;".format(req.form['id'])))
		if(is_exist==0):
			for datum in data:
				# print(datum)
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `users` ({},`status`) VALUES ({},'pending');'''.format(", ".join(key),", ".join(val)))
		else:
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `users` SET  {}  WHERE `id`='{}';".format(args[1:],req.form['id'])
		last_row_id = rapid_mysql.do(sql)
		return last_row_id
		# return redirect("/logout")
		
	def user_registration_submit(req):
		data = dict(req.form)
		key = [];val = [];args="";
		# res_email = len(rapid_mysql.do("SELECT * FROM `users` WHERE `email`='{}';".format(req.form['email']) ))
		# res_name = len(rapid_mysql.do("SELECT * FROM `name` WHERE `email`='{}';".format(req.form['name']) ))
		
		for datum in data:
			# print(datum)
			key.append("`{}`".format(datum))
			val.append("'{}'".format(data[datum]))
		sql = ('''INSERT INTO `users` ({},`status`) VALUES ({},'pending');'''.format(", ".join(key),", ".join(val)))
		_res = rapid_mysql.do(sql)
		return _res

	def edit_user_profilepic(req):
		__f = FILE_REQ.save_file_from_request(req,"profilepic",c.RECORDS+"/objects/userpics/",False,True)
		sql = "UPDATE `users` SET  `profilepic`= '{}' WHERE `id`='{}';".format(__f["file_arr_str"],req.form['id'])
		rapid_mysql.do(sql)
		return __f

	def edit_user_profilepass(req):
		sql = "UPDATE `users` SET  `password`= '{}' WHERE `id`='{}' and `password`='{}';".format(req.form['password'],req.form['id'],req.form['current_pass'])
		last_row=rapid_mysql.do(sql)
		print(last_row)
		return "--"

# ================================================
# ================================================
# ================================================
# ================================================
class system_settings:
	def add_user_group(req):
		data = req.form
		key = [];val = [];args=""
		for datum in data:
			# print(datum)
			_VAL = data[datum]
			if _VAL.lower() in ["true","false"]: _VAL =  _VAL.lower() in ["true"] 
			else: _VAL = f"'{_VAL}'"

			key.append("`{}`".format(datum))
			val.append("{}".format(_VAL) )

		sql = ('''INSERT INTO `_securitygroup` ({}) VALUES ({});'''.format(", ".join(key),", ".join(val)))
		print(rapid_mysql.do(sql))
		return ""

	def get_staff_info(req):
		return rapid_mysql.select("SELECT * FROM `users` WHERE `id`={}".format(req.form['id']) )[0]
		
	def get_user():
		pass

# ================================================
# ================================================
# ================================================
# ================================================
class file_manager:
	def add_modify_folder(req):
		for ids in req.form:
			print(f"{ids} : {req.form[ids]}")
		sql_ress = rapid_mysql.insert_or_add_to_db(req,"file_manager_folders","id")
		print(sql_ress)
		return sql_ress

	def add_file(req):
		_files = json.loads(f"[{req.form['files_arr']}]")
		sql_res = []
		for _f in _files:
			__req = AttrDict({'form':_f})
			print(__req.form)
			sql_ress = rapid_mysql.insert_or_add_to_db(__req,"file_manager_files","id")
			sql_res.append(sql_ress)
		res = FILE_REQ.save_file_from_request(
			req,
			"fileInput",
			pathtosave=c.RECORDS+"objects/mis_drive",
			raise_error=True,
			timestamp=False,
			custom_name="")
		return {"sql_note":sql_res, "file_handling_msg":res}


	def get_file(req):
		file = req.args['file']
		print(file)
		return send_file(c.RECORDS+"/objects/mis_drive/_"+file.replace(' ','_'))
		# img = img.replace('C:fakepath', '').replace(" ","_").replace(")","").replace("(","")

# ================================================
# ================================================
class AttrDict(dict):
	def __init__(self, *args, **kwargs):
		super(AttrDict, self).__init__(*args, **kwargs)
		self.__dict__ = self
# ================================================
# ================================================

class file_handling:
	def download_db_pfa(req,obj):
		_sql = "SELECT * FROM `{}` WHERE {} ;".format(obj,where_rcu_is(req.args['rcu']))
		print(_sql)
		ls_arr = rapid_mysql.select(_sql)
		return ls_arr
# ================================================
# ================================================
# ================================================
# ================================================

class fmi_tracker:
	def update_add(req):
		return rapid_mysql.insert_or_add_to_db(req,"fmi_basic_info","id")

# ================================================
# ================================================
# ================================================
# ================================================

class personal_forms:
	def save_template(req):
		datas = dict(req.form)
		# temp_src = c.RECORDS + "objects/save_templates/"+req.form['form_code']+".html"
		temp_src = c.RECORDS + "../v2_view/core/pages/chunks/__templates__/"+req.form['form_code']+".html"
		temps = open(temp_src,"w")
		temps.write(datas['form_design'].replace("~",'"'))
		temps.close()
		del datas['form_design']
		key = [];val = [];args=""
		for datum in datas:
			_VAL = datas[datum]
			key.append("`{}`".format(datum))
			val.append("'{}'".format(_VAL) )

		sql = ('''INSERT INTO `_form_templates` ({}) VALUES ({});'''.format(", ".join(key),", ".join(val)))
		print(rapid_mysql.do(sql))
		return datas

	def save_data(req):
		datas = dict(req.form)
		datas['__data'] = {}; key_to_rem=[];

		for datum in datas:
			if("__" not in datum):
				datas['__data'][datum] = datas[datum]
				key_to_rem.append(datum)
		for key in key_to_rem: datas.pop(key,None)
		datas['__data']  = json.dumps(datas['__data'] )
		key = [];val = [];args=""
		for datum in datas:
			_VAL = datas[datum]
			key.append("`{}`".format(datum))
			val.append("'{}'".format(_VAL) )
		
		sql = ('''INSERT INTO `_form_templates_data` ({}) VALUES ({});'''.format(", ".join(key),", ".join(val)))
		print(sql)
		print(rapid_mysql.do(sql))
		return datas

	def get_template(req):
		temp_src = c.RECORDS + "../v2_view/core/pages/chunks/__templates__/"+req.form['form_code']+".html"
		temps = open(temp_src,"r",)
		html = temps.read()
		temps.close()
		return "--"
		# return html.encode('cp1252')

	def save_dip_rep(req):
		excel_ = req.files
		UPLOAD_NAME = "{}_DIP_TRACKER.xlsx".format(session["USER_DATA"][0]["id"])
		__f = FILE_REQ.save_file_from_request(req,"demoA",c.RECORDS+"/objects/spreadsheets_dcf",False,False,UPLOAD_NAME)

		return redirect("/mis-v4/core-tools-trackers-specific?panel&m=mg")

# ================================================
# ================================================
# ================================================
# ================================================

def position_data_filter():
	_filter = " 1 "
	JOB = session["USER_DATA"][0]["job"].lower()
	print(session["USER_DATA"][0]['sg_info']['user_group'])
	if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = " 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = " USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
	return _filter

def where_rcu_is(_rcu):
	return " USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(_rcu)

