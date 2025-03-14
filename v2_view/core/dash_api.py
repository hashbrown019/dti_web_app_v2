from modules.Connections import mysql,sqlite
import Configurations as c
from flask import session
import json
from modules.Req_Brorn_util import authenication ## NO UTHENITICATION/SESSION HOLDER

rapid_mysql = mysql(*c.DB_CRED)


def farmer_count_per_area():
	return

def get_databases():
	tbl = {}
	res = rapid_mysql.select("SELECT TABLE_SCHEMA , TABLE_NAME ,  COLUMN_NAME FROM   INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'mis_2023';")
	for tables in res:
		# tbl.append(tables['TABLE_NAME'])
		TBLN = str(tables['TABLE_NAME'])
		if TBLN not in tbl : 
			tbl[TBLN] = []

		try:
			tbl[TBLN].append(tables['COLUMN_NAME'].decode("utf-8"))
		except:
			tbl[TBLN].append(tables['COLUMN_NAME'])
		
	return tbl


def get_area_staff():
	# return session["USER_DATA"]
	if(session["USER_DATA"][0]["security_group"] in [1,19]):
		return rapid_mysql.select("SELECT * FROM `users` ;")

	return rapid_mysql.select("SELECT * FROM `users` WHERE `rcu`='{}' AND `status`='active' ;".format(session["USER_DATA"][0]['rcu']) )

def get_security_group():
	return rapid_mysql.select("SELECT `_securitygroup`.*, `users`.`id` as 'by' , `users`.`name` FROM `_securitygroup` INNER JOIN `users` ON `_securitygroup`.`created_by`= `users`.`id` ;" )


# ====================================================
# ====================================================
# ====================================================


def get_personal_forms(user_id):
	res = rapid_mysql.select("SELECT `form_code` FROM `_form_templates_collection` WHERE `user_id`={};".format(user_id))
	collection = []
	for rcode in res:collection.append(rcode["form_code"])
		
	all_forms =  rapid_mysql.select("SELECT `_form_templates`.*, `users`.`id` as 'by' , `users`.`name` FROM `_form_templates` INNER JOIN `users` ON `_form_templates`.`user_id`= `users`.`id`;" )
	return {"all_forms":all_forms,"collection":collection}

def get_public_form(ids):
	sql = "SELECT * FROM `_form_templates` WHERE `form_code`='{}' ;".format(ids)
	print(sql)
	return rapid_mysql.select(sql)

def get_temp_data(req):
	sql = "SELECT * FROM `_form_templates_data` WHERE {} AND`__form_code`='{}';".format(position_data_filter("__form_filledby_id"),req.form['form_id'])
	print(sql)
	res = rapid_mysql.select(sql)
	to_resp = []
	for entry in res:
		entry["__data"] = json.loads(entry["__data"])
		if(int(entry["__form_filledby_id"]) != int(req.form['current_user'])):
			if(is_area_admin(req.form['current_user_group'])):pass
			else: continue
		to_resp.append(entry)
	print(req.form['current_user_group'])
	print(is_area_admin(req.form['current_user_group']))
	return to_resp

def add_to_collection(req):
	rapid_mysql.do("INSERT INTO `_form_templates_collection`(`user_id`, `form_code`) VALUES ('{}','{}');".format(req.form['user_id'],req.form['form_code'] ) )
	return req.form['url_referrer']

def get_get_db_col(req):
	_db_table = req.form["_db_table"]
	_db_col = req.form["_db_col"]
	# res = rapid_mysql.select("SELECT `id`,`{}` as 'col' FROM `{}` WHERE {};".format(_db_col,_db_table,position_data_filter("id")))
	res = rapid_mysql.select("SELECT `id`,`{}` as 'col' FROM `{}`;".format(_db_col,_db_table))
	return res
# ================================================
# ================================================

def fmi_list(sesh):
	return rapid_mysql.select("SELECT * FROM `fmi_basic_info` ;")

# ================================================
# ================================================

def folder_list(sesh):
	return rapid_mysql.select("SELECT * FROM `file_manager_folders` ;")

def file_list(sesh):
	return rapid_mysql.select("SELECT * FROM `file_manager_files` ;")

# ================================================
# ================================================
def is_area_admin(u_g):
	return "admin" in u_g.lower() or "npco" in u_g.lower()

def position_data_filter(row_id):
	_filter = "WHERE 1 "
	JOB = session["USER_DATA"][0]["job"].lower()

	if(JOB in "admin" or JOB in "super admin"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = " 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = " `{}` in ( SELECT `id` from `users` WHERE `rcu`='{}' )".format(row_id,session["USER_DATA"][0]["rcu"])
	return _filter



