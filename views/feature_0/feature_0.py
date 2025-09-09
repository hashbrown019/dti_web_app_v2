from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, Response,send_file, url_for
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os, random, json, shutil
from controllers.outbound import outbound as outb
from controllers.inbound import inbound as inb
from controllers.inbound import data_cleaning as  d_c

from views.feature_0.feature_0_sub import _main as sub_main_module
from werkzeug.utils import secure_filename
import requests
from controllers.engine_excel_to_sql import form_excel_a_handler

from multiprocessing import Process
import threading
import time, re

app = Blueprint("feature_0",__name__,template_folder='pages')
_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)

outbound = outb(app,rapid_mysql,session)
inbound = inb(app,rapid_mysql,session)
data_clean = d_c(app,rapid_mysql,session)

# app['sample_decorator'] = sample_decorator
# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)


class _main:
	def __init__(self, arg):
		print(" * main loading done")
		super(_main, self).__init__();
		self.arg = arg


	def is_on_session(): return ('USER_DATA' in session)
	# ===========================V1==========================================
	@app.route("/test/<sample_args>",methods=["POST","GET"])
	@c.login_auth_web()
	def test(sample_args):
		# outbound.app = app
		# outbound.db = rapid_mysql
		# outbound.session = session
		print(f"print from main blueprint : {sample_args}")
		return render_template("test/test.html",USER_DATA = session["USER_DATA"][0], dash_data_=_main.dashboard_home_sql_driven())

	# ===========================V1==========================================
	@app.route("/feature_0",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0():
		# outbound.app = app
		# outbound.db = rapid_mysql
		# outbound.session = session
		return redirect("/feature_home#dashboard")

	@app.route("/feature_home",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0page():
		# return render_template("SITE_OFF.html") # MAINTENANCE
		Filter.position_data_filter() # initialize restrictions
		return render_template("feature_0_home.html",USER_DATA = session["USER_DATA"][0], dash_data_=_main.dashboard_home_sql_driven())


	@app.route("/profiling_form_a/e",methods=["POST","GET"])
	@c.login_auth_web()
	def profiling_form_a():
		# return render_template("SITE_OFF.html") # MAINTENANCE
		Filter.position_data_filter() # initialize restrictions
		return render_template("embed_a.html",page=request.args['page'],USER_DATA = session["USER_DATA"][0], dash_data_=_main.dashboard_home_sql_driven())



	@c.login_auth_web()
	@app.route("/settings",methods=["POST","GET"])
	def settings():
		session["USER_DATA"][0]["office"] = "On Dev"
		setngs = request.args
		CUR_SESH = session["USER_DATA"]

		for ss in setngs:
			if(ss == "getsesh"):
				return redirect("/settings/getsesh")
			elif(ss == "chjob"):
				print(" * Changing job")
				session["USER_DATA"][0]["job"] = setngs['chjob'].replace("_"," ")
			elif(ss == "chrcu"):
				print(" * Changing job")
				session["USER_DATA"][0]["rcu"] = setngs['chrcu'].replace("_"," ").upper()

		session.clear()
		session.clear()
		session["USER_DATA"] = CUR_SESH
		return redirect("/menuv2")

	@app.route("/settings/getsesh",methods=["POST","GET"])
	@c.login_auth_web()
	def getsesh():
		return session["USER_DATA"][0]

	# =============================================================================
	
	@app.route("/notification/web_safe_encode/<strs>",methods=["POST","GET"])
	@c.login_auth_web()
	def web_safe_encode(strs):
		return inbound.web_safe_encode(strs)

	@app.route("/notification/web_safe_decode/<strs>",methods=["POST","GET"])
	@c.login_auth_web()
	def web_safe_decode(strs):
		return inbound.web_safe_decode(strs)

	@app.route("/notification/get_notif",methods=["POST","GET"])
	@c.login_auth_web()
	def get_notif():
		return inbound.get_notif()

	@app.route("/notification/get_notif_unseen",methods=["POST","GET"])
	@c.login_auth_web()
	def get_notif_unseen():
		return inbound.get_notif_unseen()

	@app.route("/notification/set_notif_seen",methods=["POST","GET"])
	@c.login_auth_web()
	def set_notif_seen():
		notif_id = request.form['notif_id']
		return inbound.set_notif_seen(notif_id)

	# ========================================================================

	@app.route("/data_cleaning_excel/get_table_col",methods=["POST","GET"])
	@c.login_auth_web()
	def get_table_col_excel():
		table = "excel_import_form_a"
		print("===== GEtting SQL")
		cols = data_clean.get_table_columns(table)
		print("===== Retruning Data")
		return cols

	@app.route("/data_cleaning/get_table_col",methods=["POST","GET"])
	@c.login_auth_web()
	def get_table_col():
		table = request.form['table']
		print("===== GEtting SQL")
		cols = data_clean.get_table_columns(table)
		print("===== Retruning Data")
		return cols

	@app.route("/data_cleaning/get_table_col_val",methods=["POST","GET"])
	@c.login_auth_web()
	def get_table_col_val():
		table = request.form['table']
		col = request.form['col']
		vals = data_clean.get_table_columns_value(col,table)
		return vals
	
	# ========================================================================
	# ===========================DEPRICATED==================================
	@app.route("/migrations/export_excel_mobile",methods=["POST","GET"])
	@c.login_auth_web()
	def export_excel_mobile():
		mobile_export_selection = request.form['form']
		print(" *  Getting Data ")
		return outbound.export_excel_mobile(mobile_export_selection)

	@app.route("/migrations/export_excel_excel",methods=["POST","GET"])
	@c.login_auth_web()
	def export_excel_excel():
		print(" *  Getting Data ")
		return outbound.export_excel_excel()

	@app.route("/excel_upload",methods=["POST","GET"])
	@c.login_auth_web()
	def excel_upload():
		today = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
		uploader = request.form['uploader']
		excel_ = request.files
		UPLOAD_NAME = "NONE"
		for excel in excel_:
			f = excel_[excel]
			UPLOAD_NAME = uploader+"#"+today+"#"+secure_filename(f.filename)
			f.save(os.path.join(c.RECORDS+"/objects/spreadsheets/queued/",UPLOAD_NAME ))

		# t1 = Process(target=_excel.excel_popu_individual,args=(UPLOAD_NAME,) )
		# t1.start()
		# t1.join()
		# return {"status":"success","msg":"Processing in Progress. Please Wait. Refresh page to view changes","success_files":UPLOAD_NAME}
		uploadstate = _excel.excel_popu_individual(UPLOAD_NAME)
		return uploadstate

	@app.route("/download_excel/<excel_file>",methods=["POST","GET"])
	@c.login_auth_web()
	def download_excel(excel_file):
		# excel_file = request.form['file']
		# print(excel_file)
		def_name = excel_file.split("@@")[2]
		excel_file = excel_file.replace("@@","#")
		return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

	@app.route("/download_excel_from_notif/<excel_file>",methods=["POST","GET"])
	@c.login_auth_web()
	def download_excel_from_notif(excel_file):
		return send_file(c.RECORDS+"/objects/spreadsheets/exports/"+excel_file, as_attachment=True,download_name=excel_file)
	
	@app.route("/delete_excel/",methods=["POST","GET"])
	@c.login_auth_web()
	def delete_excel():
		excel_file = request.form['file']
		# print(excel_file)
		def_name = excel_file.split("@@")[2]
		excel_file = excel_file.replace("@@","#")

		shutil.move(
			c.RECORDS+"/objects/spreadsheets/migrated/{}".format(excel_file),
			c.RECORDS+"/objects/spreadsheets/deleted/{}".format(excel_file)
		)
		rapid_mysql.do("DELETE FROM `excel_import_form_a` WHERE `file_name`='{}' ;".format(excel_file))
		return jsonify({"status":"done"})

	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	# ==============================================================================
	
	@app.route("/feature_0/dashgraph1",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_dashboard1():
		_data = _main.feature_0_get_farmer_data_a1_for_dash()
		g2_data = _main.feature_0_dashboard2(_data)
		PRIV_TYPE = session["USER_DATA"][0]['PRIV_TYPE']
		temp_data1 = {}
		graph_data = []
		is_npco_view = False;
		area_key = ""
		crops_name = {}

		if('NPCO' in PRIV_TYPE):
			is_npco_view = True;area_key = "addr_region";
		else:
			is_npco_view = False;area_key = "addr_prov";

		for i in range(len(_data)):
			area = _data[i][area_key]
			crop = _data[i]['farmer_primary_crop'].lower().replace(" ","")
			crops_name[crop] = crop
			if(area==""):continue
			if(area in temp_data1):
				if(crop in temp_data1[area]):
					temp_data1[area][crop] = temp_data1[area][crop] + 1
				else:
					temp_data1[area][crop] = 1
			else:
				temp_data1[area] = {'area' :area}
				# temp_data1[area] = {}
				temp_data1[area][crop] = 1
		for key in temp_data1:
			graph_data.append(temp_data1[key])
		hectare_sex = _main.get_hectareage()
		return [graph_data,crops_name,g2_data,hectare_sex]


	@app.route("/feature_0/dashgraph2",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_dashboard2(_data):
		PRIV_TYPE = session["USER_DATA"][0]['PRIV_TYPE']
		temp_data2 = {}
		area_key = ""
		is_npco_view = False;

		if('NPCO' in PRIV_TYPE):
			is_npco_view = True;area_key = "addr_region";
		else:
			is_npco_view = False;area_key = "addr_prov";
		
		
		for i in range(len(_data)):
			area = _data[i][area_key]
			crop = _data[i]['farmer_primary_crop'].lower().replace(" ","")
			sex = _data[i]['farmer_sex'].lower()
			is_hh = _data[i]['is_head_hh'].lower()
			if(area in temp_data2):
				if(crop in temp_data2[area]):
					if(sex == 'male'):
						if(is_hh in ['true','yes']):
							temp_data2[area][crop]['male_hh'] = temp_data2[area][crop]['male_hh'] + 1
						else:
							temp_data2[area][crop]['male'] = temp_data2[area][crop]['male'] + 1
					elif(sex == 'female'):
						if(is_hh in ['true','yes']):
							temp_data2[area][crop]['female_hh'] = temp_data2[area][crop]['female_hh'] + 1
						else:
							temp_data2[area][crop]['female'] = temp_data2[area][crop]['female'] + 1
				else:
					temp_data2[area][crop] = {
						"male" :0,
						"male_hh" :0,
						"female" :0,
						"female_hh" :0,
					}
				
			else:
				temp_data2[area] = {}
		return temp_data2

	@app.route("/feature_0/filter_list_farmers",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_filter_list_farmers():
		return jsonify({
			"dash1":_main.feature_0_get_farmer_data_a1(),
			# "dash2":sub_main_module.dash_get_form_a1("all"),
			# "dash3":_main.feature_0_get_farmer_data_a1_for_dash()
			}
		)

	@app.route("/feature_0/get_uploaded_excel",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_get_uploaded_excel():
		_sql = ("SELECT `file_name` as `key`, count(file_name) as `total` FROM `excel_import_form_a` WHERE `user_id`={} GROUP by `file_name`;".format(session["USER_DATA"][0]['id']))
		upld_excel = rapid_mysql.select(_sql)
		return upld_excel

	@app.route("/feature_0/get_farmer_data_a1",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_get_farmer_data_a1():
		sql_mobile = '''
			SELECT 
				`form_a_farmer_profiles`.`id` as 'db_id',
				`users`.`name` as 'inputed_by',
				`form_a_farmer_profiles`.`f_name`,
				`form_a_farmer_profiles`.`m_name`,
				`form_a_farmer_profiles`.`l_name`,
				`form_a_farmer_profiles`.`ext_name`,
				`form_a_farmer_profiles`.`farmer_sex`,
				`form_a_farmer_profiles`.`farmer_primary_crop`,
				`form_a_farmer_profiles`.`farmer_fo_name_rapid`,
				`form_a_farmer_profiles`.`addr_region`,
				`form_a_farmer_profiles`.`addr_prov`,
				`form_a_farmer_profiles`.`addr_city`,
				`form_a_farmer_profiles`.`farmer_dip_ref`,
				`form_a_farmer_profiles`.`farmer_code` as 'reference',
				`form_a_farmer_profiles`.`farmer_name` as 'name_complete'

				-- `farmer_head_of_house`,
				-- `farmer_civil_status`,
			FROM `form_a_farmer_profiles`
			INNER JOIN `users` ON `form_a_farmer_profiles`.`USER_ID` = `users`.`id` {} ;'''.format(Filter.position_data_filter())

		sql_excel = '''
			SELECT 
				`excel_import_form_a`.`id` as 'db_id',
				`users`.`name` as 'inputed_by',
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_First_name` as `f_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Middle_name` as `m_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Last_name` as `l_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Extension_name` as `ext_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Sex` as `farmer_sex`,
				`excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as `farmer_primary_crop`,
				`excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_Name_coop` as `farmer_fo_name_rapid`,
				`excel_import_form_a`.`frmer_prof_@_frmer_addr_@_region` as `addr_region`,
				`excel_import_form_a`.`frmer_prof_@_frmer_addr_@_province` as `addr_prov`,
				`excel_import_form_a`.`frmer_prof_@_frmer_addr_@_city_municipality` as `addr_city`,
				`excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_DIP_name` as `farmer_dip_ref`,
				`excel_import_form_a`.`file_name` as 'reference',
				-- `frmer_prof_@_basic_Info_@_civil_status` as `farmer_civil_status`,
				-- `frmer_prof_@_hh_Head_Info_@_is_head_og_household` as `farmer_head_of_house`
			FROM `excel_import_form_a`
		INNER JOIN `users` ON `excel_import_form_a`.`user_id` = `users`.`id` {} ;'''.format(Filter.position_data_filter())
		# RES = rapid_mysql.select(sql_mobile,False) + rapid_mysql.select(sql_excel,False) # DEPRICATED MOBILE DATA
		RES = rapid_mysql.select(sql_excel,False)
		random.shuffle(RES)
		return RES


	@app.route("/feature_0/get_farmer_data_a1_for_dash",methods=["POST","GET"])  ## FOR CREATING NEW DAsh charts
	@c.login_auth_web()
	def feature_0_get_farmer_data_a1_for_dash():
		sql_mobile = '''
			SELECT 
				`form_a_farmer_profiles`.`id` as 'db_id',
				`users`.`name` as 'inputed_by',
				`form_a_farmer_profiles`.`f_name`,
				`form_a_farmer_profiles`.`m_name`,
				`form_a_farmer_profiles`.`l_name`,
				`form_a_farmer_profiles`.`ext_name`,
				`form_a_farmer_profiles`.`farmer_sex`,
				`form_a_farmer_profiles`.`farmer_primary_crop`,
				`form_a_farmer_profiles`.`farmer_fo_name_rapid`,
				`form_a_farmer_profiles`.`addr_region`,
				`form_a_farmer_profiles`.`addr_prov`,
				`form_a_farmer_profiles`.`addr_city`,
				`form_a_farmer_profiles`.`farmer_dip_ref`,
				`form_a_farmer_profiles`.`farmer_head_of_house` as 'is_head_hh',
				`form_a_farmer_profiles`.`farmer_code` as 'reference',
				`form_a_farmer_profiles`.`farmer_name` as 'name_complete'

				-- `farmer_head_of_house`,
				-- `farmer_civil_status`,
			FROM `form_a_farmer_profiles`
			INNER JOIN `users` ON `form_a_farmer_profiles`.`USER_ID` = `users`.`id` {} ;'''.format(Filter.position_data_filter())

		sql_excel = '''
			SELECT 
				`excel_import_form_a`.`id` as 'db_id',
				`users`.`name` as 'inputed_by',
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_First_name` as `f_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Middle_name` as `m_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Last_name` as `l_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Extension_name` as `ext_name`,
				`excel_import_form_a`.`frmer_prof_@_basic_Info_@_Sex` as `farmer_sex`,
				`excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as `farmer_primary_crop`,
				`excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_Name_coop` as `farmer_fo_name_rapid`,
				`excel_import_form_a`.`frmer_prof_@_frmer_addr_@_region` as `addr_region`,
				`excel_import_form_a`.`frmer_prof_@_frmer_addr_@_province` as `addr_prov`,
				`excel_import_form_a`.`frmer_prof_@_frmer_addr_@_city_municipality` as `addr_city`,
				`excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_DIP_name` as `farmer_dip_ref`,
				`excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_is_head_og_household` as `is_head_hh`,
				`excel_import_form_a`.`file_name` as 'reference',
				-- `frmer_prof_@_basic_Info_@_civil_status` as `farmer_civil_status`,
				-- `frmer_prof_@_hh_Head_Info_@_is_head_og_household` as `farmer_head_of_house`
			FROM `excel_import_form_a`
		INNER JOIN `users` ON `excel_import_form_a`.`user_id` = `users`.`id` {} ;'''.format(Filter.position_data_filter())
		# RES = rapid_mysql.select(sql_mobile,True) + rapid_mysql.select(sql_excel,True) # DEPRICTED MOBILE DATA
		RES = rapid_mysql.select(sql_excel,True)
		random.shuffle(RES)
		return RES

	@app.route("/feature_0/dashboard_home_",methods=["POST","GET"])
	@c.login_auth_web()
	def dashboard_home_sql_driven_():
		return {
			"query_suffix" : "",
			"area_reg" : "",
			"all_farmer_count" : "",
			"all_sex_untag" : "",
			"all_sex_female" : "",
			"all_sex_male" : "",
			"is_ip_num" : "",
			"is_hh_head_num" : "",
			"with_dip": "",
			"with_fo": "",
			"enumerator": {"mobile":[],"excel":[]} ,
			"mobile_geotag": [] ,
			"ls_arr" : {
				"primary_crop" :{"main": [],"breakdown":{"excel": [] , "mobile" : []}},
				"ip_gr" :{"excel": [] , "mobile" : []},
				"fo" :{"excel": [] , "mobile" : []},
				"dip" :{"excel": [] , "mobile" : []},
			}
		}
	@app.route("/feature_0/dashboard_home",methods=["POST","GET"])
	@c.login_auth_web()
	def dashboard_home_sql_driven():
		FILTER_SUFFIX = Filter.position_data_filter()
		count_excel = rapid_mysql.select("SELECT COUNT(`frmer_prof_@_basic_Info_@_First_name`) as `ex` FROM excel_import_form_a {};".format(FILTER_SUFFIX))
		# DEPRICATED MOBILE DATA
		# count_mobile = rapid_mysql.select("SELECT COUNT(`farmer_code`) as `mob` FROM form_a_farmer_profiles {};".format(FILTER_SUFFIX))
		# all_farmer_count = count_excel[0]['ex'] + count_mobile[0]['mob']

		all_farmer_count = count_excel[0]['ex']

		query = rapid_mysql.select
		dic = Filter.strct_clean
		dic_ = Filter.strct_dic

		# DEPRICATED MOBILE DATA
		# mobile_sex = dic(query("SELECT `farmer_sex` as `key`, count(farmer_sex) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_sex;".format(FILTER_SUFFIX) ))
		# mobile_ip = dic(query("SELECT `farmer_is_ip` as `key`, count(farmer_is_ip) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_is_ip;".format(FILTER_SUFFIX) ))
		# mobile_head_hh = dic(query("SELECT `farmer_head_of_house` as `key`, count(farmer_head_of_house) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_head_of_house;".format(FILTER_SUFFIX) ))
		# mobile_ip_grp = dic(query("SELECT `farmer_ip` as `key`, count(farmer_ip) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_ip;".format(FILTER_SUFFIX) ))
		# mobile_fo = dic_(query("SELECT `farmer_fo_name_rapid` as `key`, count(farmer_fo_name_rapid) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_fo_name_rapid;".format(FILTER_SUFFIX) ))
		# mobile_dip = dic_(query("SELECT `farmer_dip_ref` as `key`, count(farmer_dip_ref) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_dip_ref;".format(FILTER_SUFFIX) ))
		# mobile_primary_c = dic(query("SELECT `farmer_primary_crop` as `key`, count(farmer_primary_crop) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_primary_crop;".format(FILTER_SUFFIX) ))

		# mobile_geotag = query("SELECT `farmer_primary_crop`,`farmer_coords_long`,`farmer_coords_lat` FROM `form_a_farmer_profiles` {} AND `farmer_coords_lat` != '' AND `farmer_coords_lat` != ' ';".format(FILTER_SUFFIX))

		excl_sex = dic(query("SELECT `frmer_prof_@_basic_Info_@_Sex` as `key`, count(`frmer_prof_@_basic_Info_@_Sex`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_basic_Info_@_Sex`;".format(FILTER_SUFFIX) ))
		excl_ip = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_farmer_ip` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_farmer_ip`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_farmer_ip`;".format(FILTER_SUFFIX) ))
		excl_head_hh = dic(query("SELECT `frmer_prof_@_hh_Head_Info_@_is_head_og_household` as `key`, count(`frmer_prof_@_hh_Head_Info_@_is_head_og_household`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_hh_Head_Info_@_is_head_og_household`;".format(FILTER_SUFFIX) ))
		excl_ip_grp = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_farmer_ip` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_farmer_ip`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_farmer_ip`;".format(FILTER_SUFFIX) ))
		excl_fo = dic_(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_Name_coop` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_Name_coop`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_Name_coop`;".format(FILTER_SUFFIX) ))
		excl_dip = dic_(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_DIP_name` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_DIP_name`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_DIP_name`;".format(FILTER_SUFFIX) ))
		excl_primary_c = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_primary_crop` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_primary_crop`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_primary_crop`;".format(FILTER_SUFFIX) ))

		# enumerator_mobile = (query(('''
		# 		SELECT 
		# 			users.id as `id`,
		# 			users.name as `key`,
		# 			count(form_a_farmer_profiles.USER_ID) as `total`
		# 		FROM
		# 			form_a_farmer_profiles
		# 		INNER JOIN users ON form_a_farmer_profiles.USER_ID = users.id
		# 		{}
		# 		GROUP by users.name
		# 		ORDER BY count(form_a_farmer_profiles.USER_ID) DESC;
		# ''').format(FILTER_SUFFIX) ))

		enumerator_excel = (query(('''
				SELECT 
					users.id as `id`,
					users.name as `key`,
					count(excel_import_form_a.user_id) as `total`
				FROM
					excel_import_form_a
				JOIN users ON excel_import_form_a.user_id = users.id
				{}
				GROUP by users.name
				ORDER BY count(excel_import_form_a.user_id) DESC;
		''').format(FILTER_SUFFIX) ))

		# DEPRICATED MOBILE DATA
		# if('untagged' not in mobile_dip):mobile_dip['untagged'] = 0;
		# if('untagged' not in mobile_fo):mobile_fo['untagged'] = 0;
		# if("" not in mobile_dip):mobile_dip[""] = 0;
		# if("" not in mobile_fo):mobile_fo[""] = 0;
		# if("male" not in mobile_sex):mobile_sex["male"] = 0;
		# if("female" not in mobile_sex):mobile_sex["female"] = 0;
		# if("false" not in mobile_ip):mobile_ip["false"] = 0;
		# if("true" not in mobile_ip):mobile_ip["true"] = 0;
		# if("" not in mobile_ip):mobile_ip[""] = 0;
		# if("false" not in mobile_head_hh):mobile_head_hh["false"] = 0;
		# if("false" not in mobile_head_hh):mobile_head_hh["false"] = 0;
		# if("" not in mobile_head_hh):mobile_head_hh[""] = 0;

		if('untagged' not in excl_dip):excl_dip['untagged'] = 0;
		if('untagged' not in excl_fo):excl_fo['untagged'] = 0;
		if("" not in excl_dip):excl_dip[""] = 0;
		if("" not in excl_fo):excl_fo[""] = 0;
		if("male" not in excl_sex):excl_sex["male"] = 0;
		if("female" not in excl_sex):excl_sex["female"] = 0;
		if("false" not in excl_ip):excl_ip["false"] = 0;
		if("true" not in excl_ip):excl_ip["true"] = 0;
		if("" not in excl_ip):excl_ip[""] = 0;
		if("false" not in excl_head_hh):excl_head_hh["false"] = 0;
		if("false" not in excl_head_hh):excl_head_hh["false"] = 0;
		if("" not in excl_head_hh):excl_head_hh[""] = 0;


		# DEPRICATED MOBILE DATA
		# with_dip = all_farmer_count - (mobile_dip['untagged']+excl_dip[""])
		# with_fo = all_farmer_count - (mobile_fo['untagged']+excl_fo[""])
		# primary_crop = Populate.primary_crop(mobile_primary_c,excl_primary_c)


		with_dip = all_farmer_count - excl_dip[""]
		with_fo = all_farmer_count - excl_fo[""]

		primary_crop = Populate.primary_crop({},excl_primary_c)
		data = {
			# "hectareage" : _main.get_hectareage(),
			# DEPRICATED MOBILE DATA
			# "all_sex_untag" : all_farmer_count + (mobile_sex['male'] + mobile_sex['female'] + excl_sex['male'] + excl_sex['female'] ),# DEPRICATED MOBILE DATA
			# "all_sex_female" : mobile_sex['female'] + excl_sex['female'],# DEPRICATED MOBILE DATA
			# "all_sex_male" : mobile_sex['male'] + excl_sex['male'],# DEPRICATED MOBILE DATA
			# "is_ip_num" : all_farmer_count - (mobile_ip['false']+excl_ip[""]), # DEPRICATED MOBILE DATA
			# "is_hh_head_num" : all_farmer_count - (mobile_head_hh['false']+excl_head_hh[""]), # DEPRICATED MOBILE DATA
			# "mobile_geotag": mobile_geotag ,
			# "sex" : {"mobile":mobile_sex,"excel":excl_sex},
			# "enumerator": {"mobile":enumerator_mobile,"excel":enumerator_excel} ,
			"query_suffix" : str(FILTER_SUFFIX),
			"area_reg" : session["USER_DATA"][0]["office"],
			"all_farmer_count" : all_farmer_count,
			"all_sex_untag" : all_farmer_count + (excl_sex['male'] + excl_sex['female'] ),
			"all_sex_female" : excl_sex['female'],
			"all_sex_male" : excl_sex['male'],
			"is_ip_num" : all_farmer_count - excl_ip[""],
			"is_hh_head_num" : all_farmer_count - excl_head_hh[""],
			"with_dip": with_dip,
			"with_fo": with_fo,
			"enumerator": {"excel":enumerator_excel} ,
			"sex" : {"excel":excl_sex},
			"ls_arr" : {
				# DEPRICATED MOBILE DATA
				# "primary_crop" :{"main": primary_crop,"breakdown":{"excel": excl_primary_c , "mobile" : mobile_primary_c}},
				# "ip_gr" :{"excel": excl_ip_grp , "mobile" : mobile_ip_grp},
				# "fo" :{"excel": excl_fo , "mobile" : mobile_fo},
				# "dip" :{"excel": excl_dip , "mobile" : mobile_dip},
				"primary_crop" :{"main": primary_crop,"breakdown":{"excel": excl_primary_c}},
				"ip_gr" :{"excel": excl_ip_grp },
				"fo" :{"excel": excl_fo },
				"dip" :{"excel": excl_dip },
			}
		}
		return data
		# return [all_mob_female[0]['f'],all_mob_male[0]['m']]


	@app.route("/feature_0/get_hectareage",methods=["POST","GET"])
	@c.login_auth_web()
	def get_hectareage():
		segre ={
			"male":{"below_to_0_5":{"total":0},"0_5_to_1":{"total":0},"1_to_1_5":{"total":0},"1_5_to_2":{"total":0},"2_to_2_5":{"total":0},"2_5_to_3":{"total":0},"3_to_3_5":{"total":0},"3_to_above":{"total":0},"untagged":{"total":0},},
			"female":{"below_to_0_5":{"total":0},"0_5_to_1":{"total":0},"1_to_1_5":{"total":0},"1_5_to_2":{"total":0},"2_to_2_5":{"total":0},"2_5_to_3":{"total":0},"3_to_3_5":{"total":0},"3_to_above":{"total":0},"untagged":{"total":0},}
		}
		actual = {}
		FILTER_SUFFIX = Filter.position_data_filter()
		query = rapid_mysql.select
		dic = Filter.strct_clean
		hectareage = query('''
			SELECT 
				`farm_info@_Farm_Basic_Info_@_declared_area_Ha` as 'ha',
				`frmer_prof_@_basic_Info_@_Sex` as 'sex',
				`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Primary_Crop_` as 'income_primary',
				`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Secondary_Crop_` as 'income_secondary',
				`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as 'crop'
			FROM `excel_import_form_a`  {} ;'''.format(FILTER_SUFFIX))
		for details in hectareage:
			ha__ = re.sub(r"[a-zA-Z]", '', details['ha'])
			try:
				ha = float(ha__)
				if(ha not in actual):
					actual[ha] = 0
				actual[ha]+=1
				SEX = details["sex"].lower()
				CROP = details["crop"].lower()
				INC_PRIME = details["income_primary"]
				_CC =  {
						"income_primary": 0,
						"income_primary_count":0,
						"income_avg":0,
						"num_farmers": 0,
						"num_farmers_has_inc": 0
					}
				# print(CROP)
				if(ha <= 0.5):
					segre[SEX]["below_to_0_5"]["total"] +=1;
					if(CROP not in segre[SEX]["below_to_0_5"]):
						segre[SEX]["below_to_0_5"][CROP] = _CC
					segre[SEX]["below_to_0_5"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["below_to_0_5"][CROP]["income_primary"]  +=float(INC_PRIME)
						segre[SEX]["below_to_0_5"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["below_to_0_5"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["below_to_0_5"][CROP]["income_primary"]/segre[SEX]["below_to_0_5"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 0.5 and ha <= 1.0):
					segre[SEX]["0_5_to_1"]["total"] +=1;
					if(CROP not in segre[SEX]["0_5_to_1"]):
						segre[SEX]["0_5_to_1"][CROP] = _CC
					segre[SEX]["0_5_to_1"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["0_5_to_1"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["0_5_to_1"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["0_5_to_1"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["0_5_to_1"][CROP]["income_primary"]/segre[SEX]["0_5_to_1"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 1.0 and ha <= 1.5):
					segre[SEX]["1_to_1_5"]["total"] +=1;
					if(CROP not in segre[SEX]["1_to_1_5"]):
						segre[SEX]["1_to_1_5"][CROP] = _CC
					segre[SEX]["1_to_1_5"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["1_to_1_5"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["1_to_1_5"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["1_to_1_5"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["1_to_1_5"][CROP]["income_primary"]/segre[SEX]["1_to_1_5"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 1.5 and ha <= 2.0):
					segre[SEX]["1_5_to_2"]["total"] +=1;
					if(CROP not in segre[SEX]["1_5_to_2"]):
						segre[SEX]["1_5_to_2"][CROP] = _CC
					segre[SEX]["1_5_to_2"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["1_5_to_2"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["1_5_to_2"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["1_5_to_2"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["1_5_to_2"][CROP]["income_primary"]/segre[SEX]["1_5_to_2"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 2.0 and ha <= 2.5):
					segre[SEX]["2_to_2_5"]["total"] +=1;
					if(CROP not in segre[SEX]["2_to_2_5"]):
						segre[SEX]["2_to_2_5"][CROP] = _CC
					segre[SEX]["2_to_2_5"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["2_to_2_5"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["2_to_2_5"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["2_to_2_5"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["2_to_2_5"][CROP]["income_primary"]/segre[SEX]["2_to_2_5"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 2.5 and ha <= 3.0):
					segre[SEX]["2_5_to_3"]["total"] +=1;
					if(CROP not in segre[SEX]["2_5_to_3"]):
						segre[SEX]["2_5_to_3"][CROP] = _CC
					segre[SEX]["2_5_to_3"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["2_5_to_3"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["2_5_to_3"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["2_5_to_3"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["2_5_to_3"][CROP]["income_primary"]/segre[SEX]["2_5_to_3"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 3.0 and ha <= 3.5):
					segre[SEX]["3_to_3_5"]["total"] +=1;
					if(CROP not in segre[SEX]["3_to_3_5"]):
						segre[SEX]["3_to_3_5"][CROP] = _CC
					segre[SEX]["3_to_3_5"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["3_to_3_5"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["3_to_3_5"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["3_to_3_5"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["3_to_3_5"][CROP]["income_primary"]/segre[SEX]["3_to_3_5"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				elif(ha > 3.5):
					segre[SEX]["3_to_3_5"]["total"] +=1;
					if(CROP not in segre[SEX]["3_to_3_5"]):
						segre[SEX]["3_to_3_5"][CROP] = _CC
					segre[SEX]["3_to_3_5"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["3_to_3_5"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["3_to_3_5"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["3_to_3_5"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["3_to_3_5"][CROP]["income_primary"]/segre[SEX]["3_to_3_5"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

				else:
					segre[SEX]["untagged"]["total"] +=1;
					if(CROP not in segre[SEX]["untagged"]):
						segre[SEX]["untagged"][CROP] = _CC
					segre[SEX]["untagged"][CROP]["num_farmers"] += 1
					try:
						segre[SEX]["untagged"][CROP]["income_primary"] += float(INC_PRIME)
						segre[SEX]["untagged"][CROP]["num_farmers_has_inc"] +=1
						segre[SEX]["untagged"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["untagged"][CROP]["income_primary"]/segre[SEX]["untagged"][CROP]["num_farmers_has_inc"])

					except ValueError:
						pass

			except Exception as e:
				pass
		myKeys = list(actual.keys())
		myKeys.sort()
		sorted_dict = {i: actual[i] for i in myKeys}
		# print(sorted_dict)
		# return sorted_dict.update(segre)
		return segre

	@app.route("/feature_0/data_clean_duplicates", methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_data_clean_duplicates():
		_data = _main.feature_0_get_farmer_data_a1()
		unique_name_arr = {}
		all_db_ids = []

		for datum in _data:
			fr_name = f"{datum[2]} {datum[3]} {datum[4]}"
			if len(fr_name.replace(" ","")) <= 1:
				fr_name = datum[14]

			display_name = fr_name
			if datum[5]:
				display_name += " " + datum[5]
			unique_name = re.sub(r"[^\w\s]", "", fr_name.replace(" ","")).lower()

			if unique_name not in unique_name_arr:
				unique_name_arr[unique_name] = []

			entry = {
				"name": display_name,
				"db_id": datum[0],
				"inputed": datum[1],
				"ref_code": datum[13],
				"linked": False,
				"linked_info": ""   # will store e.g. "(Linked to excel_import_form_a)"
			}
			unique_name_arr[unique_name].append(entry)
			all_db_ids.append(str(datum[0]))

		# get link_to_id and db_table in one shot
		linked_map = {}
		if all_db_ids:
			id_list = ",".join(all_db_ids)
			sql = f"""
			SELECT link_to_id, db_table
			FROM __data_link_1
			WHERE link_to_id IN ({id_list})
			"""
			rows = rapid_mysql.select(sql)
			# build map {id: db_table}
			linked_map = {str(r['link_to_id']): r['db_table'] for r in rows}

		# mark linked info
		for group in unique_name_arr.values():
			for entry in group:
				db_id_str = str(entry["db_id"])
				if db_id_str in linked_map:
					entry["linked"] = True
					entry["linked_info"] = f"(Linked to {linked_map[db_id_str]})"

		# keep only duplicates
		new_unique_name_arr = [g for g in unique_name_arr.values() if len(g) >= 2]
		new_new_unique_name_arr = sorted(new_unique_name_arr, key=len, reverse=True)
		return new_new_unique_name_arr



	# ===================================================================
	# =================LINK_DATA=========================================
	# ===================================================================
	# ===================================================================

	@app.route("/feature_0/link_data_dcf_form_a",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_link_data_dcf_form_a():
		return render_template("link_data/link_data_dcf_form_a.html",USER_DATA = session["USER_DATA"][0])

	@app.route("/feature_0/link_data_dcf_form_a_del",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_link_data_dcf_form_a_del():
		ids = request.form['id']
		res = rapid_mysql.do("DELETE FROM `__data_link_1` WHERE `id`='{}' ;".format(ids))
		return jsonify(res)

	@app.route("/feature_0/link_data_dcf_form_a_view/<table>/<data_entry>",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_link_data_dcf_form_a_view(table,data_entry):
		res = "--"
		res_ = rapid_mysql.select("SELECT * FROM `__data_link_1` WHERE `link_from_id`='{}' AND `db_table`='{}'; ".format(data_entry,table))
		return res_


	@app.route("/feature_0/link_data_dcf_form_a_add",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_link_data_dcf_form_a_add():
		data = dict(request.form); key = [];val = [];args=""

		for datum in data:
			key.append("`{}`".format(datum))
			val.append("'{}'".format(data[datum]))
		sql = ('''INSERT INTO `__data_link_1` ({},`remarks`) VALUES ({},'from_form')'''.format(", ".join(key),", ".join(val)))

		last_row_id = rapid_mysql.do(sql)
		return jsonify({"last_row_id":last_row_id})

	# ====================================================================
	# ===================LINK_DATA_END_===================================
	# ====================================================================
	# ====================================================================

class Populate:
	def primary_crop(mobi,excl):
		new_comd = {}
		comodities = rapid_mysql.select("SELECT `name` as `key` FROM `value_chain_comodities`",False)
		for count in range(len(comodities)):
			cmdty_sndrd = comodities[count][0]
			if(cmdty_sndrd not in new_comd):new_comd[cmdty_sndrd] = 0
			if(cmdty_sndrd not in mobi):mobi[cmdty_sndrd] = 0
			if(cmdty_sndrd not in excl):excl[cmdty_sndrd] = 0
			new_comd[cmdty_sndrd] = new_comd[cmdty_sndrd] + mobi[cmdty_sndrd] + excl[cmdty_sndrd]
		# print(sorted(new_comd))
		return sorted(new_comd.items(), key=lambda x:x[1], reverse=True)


class Filter:
	def position_data_filter():
		_filter = "WHERE 1 "
		JOB = session["USER_DATA"][0]["job"].lower()

		if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
			session["USER_DATA"][0]["office"] = "NPCO"
			_filter = "WHERE 1 "
		else:
			session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
			_filter = "WHERE USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
		return _filter

	def strct_dic(dict_):
		new_dict_ = {};
		for data in dict_:new_dict_[data['key']] = data['total']
		return json.loads(json.dumps(new_dict_))

	def strct_clean(dict_):
		new_dict_ = {};
		for data in dict_:new_dict_[data['key']] = data['total']
		return Filter.clean(json.loads(json.dumps(new_dict_)))

	def clean(dict_):
		new_dict_ = {};
		for key in dict_:
			KEY = key.lower().replace(" ","").replace(".","").replace("/","").replace("\\","").replace("-","").replace("*","").replace(",","").replace("(","").replace(")","").replace("&","")
			if(KEY not in new_dict_):
				new_dict_[KEY] = 0
			new_dict_[KEY] = new_dict_[KEY]+dict_[key]
			
		return json.loads(json.dumps(new_dict_))

