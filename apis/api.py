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
		print(ids)
		if(ids=="all"):
			sql = "SELECT `id`,`name`,`address`,`email`,`job`,`mobile`,`pcu`,`rcu`,`username`,`until`,`status` FROM `users`;"
		else:
			sql = "SELECT `id`,`name`,`address`,`email`,`job`,`mobile`,`pcu`,`rcu`,`username`,`until`,`status` FROM `users` WHERE `id`='{}';".format(ids)
		_user = rapid_mysql.select(sql)
		if(data_handlers.is_on_session()):
			return _user
		else:
			return [{"id":"0","name":"no_data"}]

# def get_all_uploaded_excel_data_heads():
# 	excel_f_a_heads = c.RECORDS+"/settings/db_sql_excel_form_a.head"
# 	reader = open(excel_f_a_heads,"r");excel_f_a_heads = json.loads(reader.read());reader.close()
# 	return excel_f_a_heads

