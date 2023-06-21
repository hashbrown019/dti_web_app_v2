import Configurations as c
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
from modules.Utility import obj_handling as objh
from modules.Req_Brorn_util import rsa_sec as _rsa
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

	@app.route("/api/user_pic/<fname>")
	def get_user_pic(fname):
		return send_file(c.RECORDS+"objects/userpics/"+fname, as_attachment=False,download_name=fname)

class user_management:
	def is_on_session(): return ('USER_DATA' in session)

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
		# data["USER_ID"] = session["USER_DATA"]['id']
		# __f = FILE_REQ.save_file_from_request(request,"upload",c.RECORDS+"/objects/webrep/",False,True)
		# data["upload"] = __f["file_arr_str"]

		sql = "UPDATE `users` SET  {} WHERE `id`='{}';".format(args[1:],request.form['id'])

		last_row_id = rapid_mysql.do(sql)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/api/user/change_pass",methods=["POST","GET"]) # GE
	def change_pass():
		msg = "on process"
		if(user_management.is_on_session()):
			# cur_user = rapid_mysql.select("SELECT * FROM `users` WHERE `id`='{}';".format(request.form['id']))
			sql = "UPDATE `users` SET `password`='{}' WHERE `id`='{}';".format(request.form['newpass'],request.form['id'])
			print(sql)
			do_change_pass = rapid_mysql.do(sql)
			
			return jsonify({"msg":msg})
		else:
			return jsonify({"msg":"ERROR"})

	@app.route("/api/user/rankings/<user_id>",methods=["POST","GET"]) # GE
	def user_rankings(user_id):
		data = {}
		msg = "on process"
		if(user_management.is_on_session()):
			prof_a_e = len(rapid_mysql.select("SELECT `user_id` FROM `excel_import_form_a` WHERE `user_id` = '{}';".format(user_id)))
			prof_a = len(rapid_mysql.select("SELECT `USER_ID` FROM `form_a_farmer_profiles` WHERE `USER_ID` = '{}';".format(user_id)))
			data['profiling_a'] = int(prof_a_e) + int(prof_a)
			data['prof_b'] = len(rapid_mysql.select("SELECT `uploaded_by` FROM `form_b` WHERE `uploaded_by` = '{}';".format(user_id)))
			data['prof_c'] = len(rapid_mysql.select("SELECT `upload_by` FROM `form_c` WHERE `upload_by` = '{}';".format(user_id)))
			data
			data['dcf_access_financing'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_access_financing` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_bdsp_reg'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_bdsp_reg` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_capacity_building'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_capacity_building` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_enablers_activity'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_enablers_activity` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_implementing_unit'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_implementing_unit` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_matching_grant'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_matching_grant` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_negosyo_center'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_negosyo_center` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_prep_review_aprv_status'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_prep_review_aprv_status` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_product_development'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_product_development` WHERE `upload_by` = '{}';".format(user_id)))
			data['dcf_trade_promotion'] = len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_trade_promotion` WHERE `upload_by` = '{}';".format(user_id)))
			data['webrep_articles'] = len(rapid_mysql.select("SELECT `USER_ID` FROM `webrep_articles` WHERE `USER_ID` = '{}';".format(user_id)))
			data['webrep_forum_comments'] = len(rapid_mysql.select("SELECT `comment_by` FROM `webrep_forum_comments` WHERE `comment_by` = '{}';".format(user_id)))
			data['webrep_uploads'] = len(rapid_mysql.select("SELECT `USER_ID` FROM `webrep_uploads` WHERE `USER_ID` = '{}';".format(user_id)))
			
			return data


class security:
	@app.route("/api/sec/gen_key",methods=["POST","GET"]) # GE
	def gen_key():
		return jsonify(
			_rsa.generate_key(
				key_size=512,
				key_name='dtirapid',
				password='dtirapid'
			)
		)
	@app.route("/api/sec/view_key",methods=["POST","GET"]) # GE
	def view_key():
		return jsonify(
			_rsa.view_keys(
				key_name='dtirapid',
				password='dtirapidssss'
			)
		)

	@app.route("/api/sec/encr/<raw_data>/<pubkey>",methods=["POST","GET"]) # GE
	def encr(raw_data,pubkey):
		return encrypt(pubkey,raw_data)

	@app.route("/api/sec/decr/<raw_data>/<privkey>",methods=["POST","GET"]) # GE
	def decr(raw_data,privkey):
		return encrypt(privkey,raw_data)
# def get_all_uploaded_excel_data_heads():
# 	excel_f_a_heads = c.RECORDS+"/settings/db_sql_excel_form_a.head"
# 	reader = open(excel_f_a_heads,"r");excel_f_a_heads = json.loads(reader.read());reader.close()
# 	return excel_f_a_heads

