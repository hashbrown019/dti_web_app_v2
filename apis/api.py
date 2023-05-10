import Configurations as c
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
from modules.Utility import obj_handling as objh
import os, json
from controllers.engine_block_to_sql import form_migration
from controllers.engine_excel_to_sql import form_excel_a_handler

app = Blueprint("api",__name__)

form_mig_block = form_migration(__name__)
form_mig_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)


class data_handlers:
	def is_on_session(): return ('USER_DATA' in session)
	def __init__(self, arg):super(data_handlers, self).__init__();self.arg = arg


	# ==========================================================
	@app.route("/api/block_sql/all",methods=["POST","GET"]) # GE
	def block_sql():
		return form_mig_block.get_all()


	@app.route("/api/excel_sql/all",methods=["POST","GET"]) # GE
	def excel_sql():
		# content = form_mig_excel.get_all_uploaded_excel_data_f_a("all","all","all")
		content = form_mig_excel.get_all_uploaded_excel_data_f_a()
		return jsonify(content)
		# return objh.txt_file_dl("skkrt.sql",content)
		# return objh.obj_file_dl("skkrt.objdmp",content)

class user_management:
	def is_on_session(): return ('USER_DATA' in session)
	def __init__(self, arg):super(data_handlers, self).__init__();self.arg = arg

	@app.route("/api/get_user_data/<ids>",methods=["POST","GET"]) # GE
	def get_user_data(ids):
		# print(ids)
		if(ids=="all"):
			sql = "SELECT `id`,`name`,`address`,`email`,`job`,`mobile`,`pcu`,`rcu`,`username`,`until`,`status` FROM `users`;"
		else:
			sql = "SELECT `id`,`name`,`address`,`email`,`job`,`mobile`,`pcu`,`rcu`,`username`,`until`,`status` FROM `users` WHERE `id`='{}';".format(ids)
		_user = rapid_mysql.select(sql)
		if(data_handlers.is_on_session()):
			return _user
		else:
			return [{"id":"0","name":"no_data"}]

	@app.route("/api/edit_user",methods=["POST","GET"]) # GE
	def edit_user():
		print("  * Edit User Module")
		data = dict(request.form)
		key = [];val = [];args=""
		is_exist = len(rapid_mysql.select("SELECT * FROM `users` WHERE `id` ='{}' ;".format(request.form['id'])))
		if(is_exist==0):
			print(" >> Adding User")
			for datum in data:
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `users` ({},`password`) VALUES ({},"dtirapid")'''.format(", ".join(key),", ".join(val)))
		else:
			print(" >> Editing User")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `users` SET  {} WHERE `id`='{}';".format(args[1:],request.form['id'])
			pass
		last_row_id = rapid_mysql.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/api/get_user_priv/<ids>",methods=["POST","GET"]) # GE
	def get_user_priv(ids):
		sql = "SELECT * FROM `__user_privilege` WHERE `user_id`='{}';".format(ids)
		_user = rapid_mysql.select(sql)
		if(data_handlers.is_on_session()):
			return _user
		else:
			return [{"id":"0","name":"no_data"}]

	@app.route("/api/edit_user_priv",methods=["POST","GET"]) # GE
	def edit_user_priv():
		print("  * Edit User Module")
		data = dict(request.form)
		key = [];val = [];args=""
		is_exist = len(rapid_mysql.select("SELECT * FROM `__user_privilege` WHERE `user_id` ='{}' ;".format(request.form['user_id'])))
		if(is_exist==0):
			print(" >> Adding user_Privilege")
			for datum in data:
				key.append("`{}`".format(datum))
				val.append("'{}'".format(data[datum]))
			sql = ('''INSERT INTO `__user_privilege` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
		else:
			print(" >> Editing user_Privilege")
			for datum in data:
				args += ",`{}`='{}'".format(datum,data[datum])
			sql = "UPDATE `__user_privilege` SET  {} WHERE `user_id`='{}';".format(args[1:],request.form['user_id'])
			pass
		last_row_id = rapid_mysql.do(sql)
		return jsonify({"last_row_id":last_row_id})


	@app.route("/api/user_status",methods=["POST","GET"]) # GE
	def user_status():
		print("  * Edit User status")
		# FILE_REQ = file_from_request(app)
		data = dict(request.form)
		# print(data)
		key = [];val = [];args=""
		# data["USER_ID"] = session["USER_DATA"][0]['id']
		# __f = FILE_REQ.save_file_from_request(request,"upload",c.RECORDS+"/objects/webrep/",False,True)
		# data["upload"] = __f["file_arr_str"]

		sql = "UPDATE `users` SET  {} WHERE `id`='{}';".format(args[1:],request.form['id'])

		last_row_id = rapid_mysql.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/api/user/change_pass",methods=["POST","GET"]) # GE
	def change_pass():
		msg = "on process"
		if(user_management.is_on_session()):
			# cur_user = rapid_mysql.select("SELECT * FROM `users` WHERE `id`='{}';".format(request.form['id']))[0]
			sql = "UPDATE `users` SET `password`='{}' WHERE `id`='{}';".format(request.form['newpass'],request.form['id'])
			print(sql)
			do_change_pass = rapid_mysql.do(sql)
			
			return jsonify({"msg":msg})
		else:
			return jsonify({"msg":"ERROR"})

# def get_all_uploaded_excel_data_heads():
# 	excel_f_a_heads = c.RECORDS+"/settings/db_sql_excel_form_a.head"
# 	reader = open(excel_f_a_heads,"r");excel_f_a_heads = json.loads(reader.read());reader.close()
# 	return excel_f_a_heads

