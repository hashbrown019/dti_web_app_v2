from modules.Connections import mysql,sqlite
import Configurations as c
from flask import session
from modules.Req_Brorn_util import file_from_request
import json
# from v2_view.core import _socketIO


rapid_mysql = mysql(*c.DB_CRED)
FILE_REQ = file_from_request(c.FLASK_APP)

# ================================================
# ================================================
# ================================================
# ================================================
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
			sql = ('''INSERT INTO `users` ({}) VALUES ({},'pending');'''.format(", ".join(key),", ".join(val)))
		
		else:
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `users` SET  {}  WHERE `id`='{}';".format(args[1:],req.form['id'])
		last_row_id = rapid_mysql.do(sql)
		return last_row_id
		# return redirect("/logout")


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
		temps = open(temp_src,"r")
		html = temps.read()
		temps.close()
		return html

# ================================================
# ================================================
# ================================================
# ================================================

def position_data_filter():
	_filter = "WHERE 1 "
	JOB = session["USER_DATA"][0]["job"].lower()
	print(session["USER_DATA"][0]['sg_info']['user_group'])
	if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = "WHERE 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = "WHERE USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
	return _filter



