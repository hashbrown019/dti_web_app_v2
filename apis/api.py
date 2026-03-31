import Configurations as c
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
from modules.Utility import obj_handling as objh
from modules.Req_Brorn_util import rsa_sec as _rsa
import os, json
from controllers.engine_block_to_sql import form_migration
from controllers.engine_excel_to_sql import form_excel_a_handler
from tqdm import tqdm

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

	@app.route("/api/get_user_data/<ids>",methods=["POST","GET"])
	def get_user_data(ids):
		if(ids=="all"):
			sql = "SELECT `id`,`name`,`address`,`email`,`job`,`mobile`,`pcu`,`rcu`,`username`,`until`,`status`, `profilepic` FROM `users` WHERE `status`='active' LIMIT 500;"
			_user = rapid_mysql.select(sql)
		else:
			sql = "SELECT `id`,`name`,`address`,`email`,`job`,`mobile`,`pcu`,`rcu`,`username`,`until`,`status`, `profilepic` FROM `users` WHERE `id`=%s LIMIT 1;"
			_user = rapid_mysql.select(sql, [ids])
		if(data_handlers.is_on_session()):
			return _user
		else:
			return [{"id":"0","name":"no_data"}]

	@app.route("/api/edit_user",methods=["POST","GET"]) # GE
	@c.login_auth_web()
	def edit_user():
		print("  * Edit User Module")
		data = dict(request.form)
		
		user_id = request.form.get('id')
		sql_check = "SELECT * FROM `users` WHERE `id` = %s LIMIT 1;"
		is_exist = len(rapid_mysql.select(sql_check, [user_id]))
		
		if(is_exist==0):
			print(" >> Adding User")
			columns = []
			values_list = []
			params = []
			for datum in data:
				columns.append("`{}`".format(datum))
				values_list.append("%s")
				params.append(data[datum])
			columns.append("`password`")
			values_list.append("%s")
			params.append("dtirapid")
			sql = "INSERT INTO `users` ({}) VALUES ({})".format(", ".join(columns), ", ".join(values_list))
			last_row_id = rapid_mysql.do(sql, params)
		else:
			print(" >> Editing User")
			set_clauses = []
			params = []
			for datum in data:
				set_clauses.append("`{}`=%s".format(datum))
				params.append(data[datum])
			params.append(user_id)
			sql = "UPDATE `users` SET {} WHERE `id`=%s".format(", ".join(set_clauses))
			last_row_id = rapid_mysql.do(sql, params)
		
		return jsonify({"last_row_id":last_row_id})

	@app.route("/api/get_user_priv/<ids>",methods=["POST","GET"]) # GE
	def get_user_priv(ids):
		sql = "SELECT * FROM `__user_privilege` WHERE `user_id`=%s LIMIT 1;"
		_user = rapid_mysql.select(sql, [ids])
		if(data_handlers.is_on_session()):
			return _user
		else:
			return [{"id":"0","name":"no_data"}]

	@app.route("/api/edit_user_priv",methods=["POST","GET"]) # GE
	def edit_user_priv():
		print("  * Edit User Module")
		data = dict(request.form)
		
		user_id = request.form.get('user_id')
		sql_check = "SELECT * FROM `__user_privilege` WHERE `user_id` = %s LIMIT 1;"
		is_exist = len(rapid_mysql.select(sql_check, [user_id]))
		
		if(is_exist==0):
			print(" >> Adding user_Privilege")
			columns = []
			values_list = []
			params = []
			for datum in data:
				columns.append("`{}`".format(datum))
				values_list.append("%s")
				params.append(data[datum])
			sql = "INSERT INTO `__user_privilege` ({}) VALUES ({})".format(", ".join(columns), ", ".join(values_list))
			last_row_id = rapid_mysql.do(sql, params)
		else:
			print(" >> Editing user_Privilege")
			set_clauses = []
			params = []
			for datum in data:
				set_clauses.append("`{}`=%s".format(datum))
				params.append(data[datum])
			params.append(user_id)
			sql = "UPDATE `__user_privilege` SET {} WHERE `user_id`=%s".format(", ".join(set_clauses))
			last_row_id = rapid_mysql.do(sql, params)
		
		return jsonify({"last_row_id":last_row_id})


	@app.route("/api/user_status",methods=["POST","GET"]) # GE
	@c.login_auth_web()
	def user_status():
		print("  * Edit User status")
		data = dict(request.form)
		user_id = request.form.get('id')
		
		set_clauses = []
		params = []
		for datum in data:
			set_clauses.append("`{}`=%s".format(datum))
			params.append(data[datum])
		params.append(user_id)
		sql = "UPDATE `users` SET {} WHERE `id`=%s".format(", ".join(set_clauses))
		
		last_row_id = rapid_mysql.do(sql, params)
		return jsonify({"last_row_id":last_row_id})

	@app.route("/api/user/change_pass",methods=["POST","GET"]) # GE
	@c.login_auth_web()
	def change_pass():
		msg = "on process"
		if(user_management.is_on_session()):
			user_id = request.form.get('id')
			new_pass = request.form.get('newpass')
			sql = "UPDATE `users` SET `password`=%s WHERE `id`=%s"
			print(f"Change password for user {user_id}")
			do_change_pass = rapid_mysql.do(sql, [new_pass, user_id])
			
			return jsonify({"msg":msg})
		else:
			return jsonify({"msg":"ERROR"})



	@app.route("/api/user/get_all_id",methods=["POST","GET"]) # GE
	@c.login_auth_web()
	def all_ranks_users():
		user_rankings = []
		all_users = rapid_mysql.select("SELECT `id`, `name`, `job` FROM `users` WHERE `status` = 'active' ;");
		# for user in all_users :
		# 	user_rankings.append( user_management.count_all(user['id']) )
		# 	# user_rankings[user['name']] = user_management.count_all(user['id'])[0]["over_all_encoded"]

		return jsonify(all_users)


	@app.route("/api/user/all_ranks/<ids>",methods=["POST","GET"]) # GE
	@c.login_auth_web()
	def count_all(ids):
		sql = """
			SELECT
				(SELECT `users`.`id` FROM `users` WHERE `users`.`id` = %s LIMIT 1) as uid,
				(SELECT `users`.`name` FROM `users` WHERE `users`.`id` = %s LIMIT 1) as name,
				(SELECT `users`.`profilepic` FROM `users` WHERE `users`.`id` = %s LIMIT 1) as pic,
				(SELECT `users`.`rcu` FROM `users` WHERE `users`.`id` = %s LIMIT 1) as rcu,
				(SELECT COUNT(*) FROM `excel_import_form_a` WHERE `excel_import_form_a`.`user_id` = %s) + 
				(SELECT COUNT(*) FROM `form_b` WHERE `form_b`.`uploaded_by` = %s) + 
				(SELECT COUNT(*) FROM `form_c` WHERE `form_c`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_bdsp_reg` WHERE `dcf_bdsp_reg`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_capacity_building` WHERE `dcf_capacity_building`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_enablers_activity` WHERE `dcf_enablers_activity`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_implementing_unit` WHERE `dcf_implementing_unit`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_matching_grant` WHERE `dcf_matching_grant`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_negosyo_center` WHERE `dcf_negosyo_center`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_prep_review_aprv_status` WHERE `dcf_prep_review_aprv_status`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_product_development` WHERE `dcf_product_development`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `dcf_trade_promotion` WHERE `dcf_trade_promotion`.`upload_by` = %s) + 
				(SELECT COUNT(*) FROM `webrep_articles` WHERE `webrep_articles`.`USER_ID` = %s) + 
				(SELECT COUNT(*) FROM `webrep_forum_comments` WHERE `webrep_forum_comments`.`comment_by` = %s) + 
				(SELECT COUNT(*) FROM `webrep_uploads` WHERE `webrep_uploads`.`USER_ID` = %s) as over_all_encoded
		"""
		params = [ids] * 16
		return rapid_mysql.select(sql, params)[0]

	@app.route("/api/user/rankings/<user_id>",methods=["POST","GET"]) # GE
	def user_rankings(user_id):
		data = {}
		msg = "on process"
		if(user_management.is_on_session()):
			try:
				data['profiling_a'] = {
					'total' : len(rapid_mysql.select("SELECT `user_id` FROM `excel_import_form_a` LIMIT 1000;")) + len(rapid_mysql.select("SELECT `USER_ID` FROM `form_a_farmer_profiles` LIMIT 1000;")),
					'inputed': len(rapid_mysql.select("SELECT `user_id` FROM `excel_import_form_a` WHERE `user_id` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['prof_b'] = {
					'total' : len(rapid_mysql.select("SELECT `uploaded_by` FROM `form_b` LIMIT 1000;")),
					'inputed': len(rapid_mysql.select("SELECT `uploaded_by` FROM `form_b` WHERE `uploaded_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['prof_c'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `form_c` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `form_c` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf11'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_access_financing` LIMIT 1000;")),
					'inputed': len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_access_financing` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf3'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_bdsp_reg` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_bdsp_reg` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf4'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_capacity_building` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_capacity_building` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf9'] = {
					"total" : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_enablers_activity` LIMIT 1000;")),
					"inputed" : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_enablers_activity` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf2'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_implementing_unit` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_implementing_unit` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf5'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_matching_grant` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_matching_grant` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf10'] ={ 
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_negosyo_center` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_negosyo_center` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf1'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_prep_review_aprv_status` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_prep_review_aprv_status` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf6'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_product_development` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_product_development` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['dcf7'] = {
					'total' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_trade_promotion` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `upload_by` FROM `dcf_trade_promotion` WHERE `upload_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['webrep_articles'] ={
					'total' : len(rapid_mysql.select("SELECT `USER_ID` FROM `webrep_articles` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `USER_ID` FROM `webrep_articles` WHERE `USER_ID` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['webrep_forum_comments'] = {
					'total' : len(rapid_mysql.select("SELECT `comment_by` FROM `webrep_forum_comments` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `comment_by` FROM `webrep_forum_comments` WHERE `comment_by` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			try:
				data['webrep_uploads'] = {
					'total' : len(rapid_mysql.select("SELECT `USER_ID` FROM `webrep_uploads` LIMIT 1000;")),
					'inputed' : len(rapid_mysql.select("SELECT `USER_ID` FROM `webrep_uploads` WHERE `USER_ID` = %s LIMIT 1000;", [user_id]))
				}
			except:pass
			return data
		else:
			return {'msg':'session required','err':404}

	@app.route("/api/user/rankings",methods=["POST","GET"]) # GE
	def user_rankings_all():
		ALL_USER = rapid_mysql.select("SELECT `id`, `name` , `rcu` FROM `users` WHERE `status`='active' LIMIT 500;")
		data = {}
		msg = "on process"
		print("starting")
		if(user_management.is_on_session()):
			for user in ALL_USER:
				user_id = user['id']
				print(user['name'])
				data[user['name'] ] = {}
				total_input_all = 0
				
				try:
					prof_a_count = rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `excel_import_form_a` WHERE `user_id` = %s;", [user_id])
					total_input_all += int(prof_a_count[0]['cnt']) if prof_a_count else 0
				except: pass
				
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `form_b` WHERE `uploaded_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `form_c` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_access_financing` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_bdsp_reg` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_capacity_building` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_enablers_activity` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_implementing_unit` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_matching_grant` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_negosyo_center` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_prep_review_aprv_status` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_product_development` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `dcf_trade_promotion` WHERE `upload_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `webrep_articles` WHERE `USER_ID` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `webrep_forum_comments` WHERE `comment_by` = %s;", [user_id])[0]['cnt']
				except: pass
				try:
					total_input_all += rapid_mysql.select("SELECT COUNT(`id`) as cnt FROM `webrep_uploads` WHERE `USER_ID` = %s;", [user_id])[0]['cnt']
				except: pass
				
				data[user['name']]= total_input_all
			return data
		else:
			return {'msg':'session required','err':404}

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







# data[user['name'] ]['profiling_a'] = int(prof_a_e) + int(prof_a)
# data[user['name'] ]['prof_b'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `form_b` WHERE `uploaded_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['prof_c'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `form_c` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_access_financing'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_access_financing` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_bdsp_reg'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_bdsp_reg` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_capacity_building'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_capacity_building` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_enablers_activity'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_enablers_activity` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_implementing_unit'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_implementing_unit` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_matching_grant'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_matching_grant` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_negosyo_center'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_negosyo_center` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_prep_review_aprv_status'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_prep_review_aprv_status` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_product_development'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_product_development` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['dcf_trade_promotion'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `dcf_trade_promotion` WHERE `upload_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['webrep_articles'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `webrep_articles` WHERE `USER_ID` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['webrep_forum_comments'] = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `webrep_forum_comments` WHERE `comment_by` = '{}';".format(user_id))[0]['count']
# data[user['name'] ]['webrep_uploads'] =