from flask import Blueprint, render_template, request, session, redirect, jsonify
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os, random
import json

app = Blueprint("feature_0",__name__,template_folder='pages')

rapid_mysql = mysql(*c.DB_CRED)

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)

class _main:
	def is_on_session(): return ('USER_DATA' in session)

	def __init__(self, arg):super(_main, self).__init__();self.arg = arg


	# ===========================V1==========================================
	@app.route("/feature_0",methods=["POST","GET"])
	def feature_0():
		return redirect("/feature_0page#1")



	@app.route("/feature_0page",methods=["POST","GET"])
	def feature_0page():
		_main.settings(request.args)
		# return render_template("SITE_OFF.html") # MAINTENANCE
		Filter.position_data_filter() # initialize restrictions
		if(_main.is_on_session()):
			return render_template("feature_0_home.html",USER_DATA = session["USER_DATA"][0], dash_data_=_main.dashboard_home_sql_driven())
		else:
			return redirect("/login?force_url=1")


	def settings(setngs):
		session["USER_DATA"][0]["office"] = "On Dev"
		for ss in setngs:
			if(ss == "getsesh"):
				return redirect("/settings/getsesh")
			elif(ss == "chjob"):
				print(" * Changing job")
				session["USER_DATA"][0]["job"] = setngs['chjob']
			elif(ss == "chrcu"):
				print(" * Changing job")
				session["USER_DATA"][0]["rcu"] = setngs['chrcu'].replace("_"," ").upper()
		pass

	@app.route("/settings/getsesh",methods=["POST","GET"])
	def getsesh():
		return session["USER_DATA"][0]

# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================
	@app.route("/feature_0/get_uploaded_excel",methods=["POST","GET"])
	def feature_0_get_uploaded_excel():
		_sql = ("SELECT `file_name` as `key`, count(file_name) as `total` FROM `excel_import_form_a` WHERE `user_id`={} GROUP by `file_name`;".format(session["USER_DATA"][0]['id']))
		upld_excel = rapid_mysql.select(_sql)
		return upld_excel

	@app.route("/feature_0/get_farmer_data_a1",methods=["POST","GET"])
	def feature_0_get_farmer_data_a1():
		sql_mobile = '''
			SELECT 
				`f_name`,
				`m_name`,
				`l_name`,
				`ext_name`,
				`farmer_sex`,
				`addr_region`,
				`addr_prov`,
				`addr_city`,
				`farmer_dip_ref`,
				`farmer_head_of_house`,
				`farmer_civil_status`,
				`SOURCE`
			FROM `form_a_farmer_profiles` {} ;'''.format(Filter.position_data_filter())

		sql_excel = '''
			SELECT 
				`frmer_prof_@_basic_Info_@_First_name` as `f_name`,
				`frmer_prof_@_basic_Info_@_Middle_name` as `m_name`,
				`frmer_prof_@_basic_Info_@_Last_name` as `l_name`,
				`frmer_prof_@_basic_Info_@_Extension_name` as `ext_name`,
				`frmer_prof_@_basic_Info_@_Sex` as `farmer_sex`,
				`frmer_prof_@_frmer_addr_@_region` as `addr_region`,
				`frmer_prof_@_frmer_addr_@_province` as `addr_prov`,
				`frmer_prof_@_frmer_addr_@_city_municipality` as `addr_city`,
				`frmer_prof_@_Farming_Basic_Info_@_DIP_name` as `farmer_dip_ref`,
				`frmer_prof_@_hh_Head_Info_@_is_head_og_household` as `farmer_head_of_house`,
				`frmer_prof_@_basic_Info_@_civil_status` as `farmer_civil_status`
			FROM `excel_import_form_a` {} ;'''.format(Filter.position_data_filter())
		all_farmer_small_data = rapid_mysql.select(sql_mobile) + rapid_mysql.select(sql_excel)
		random.shuffle(all_farmer_small_data)
		return "all_farmer_small_data"

	@app.route("/feature_0/dashboard_home",methods=["POST","GET"])
	def dashboard_home_sql_driven():
		FILTER_SUFFIX = Filter.position_data_filter()
		count_excel = rapid_mysql.select("SELECT COUNT(`frmer_prof_@_basic_Info_@_First_name`) as `ex` FROM excel_import_form_a {};".format(FILTER_SUFFIX))
		count_mobile = rapid_mysql.select("SELECT COUNT(`farmer_code`) as `mob` FROM form_a_farmer_profiles {};".format(FILTER_SUFFIX))
		all_farmer_count = count_excel[0]['ex'] + count_mobile[0]['mob'] 

		query = rapid_mysql.select
		dic = Filter.strct_clean

		mobile_sex = dic(query("SELECT `farmer_sex` as `key`, count(farmer_sex) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_sex;".format(FILTER_SUFFIX) ))
		mobile_ip = dic(query("SELECT `farmer_is_ip` as `key`, count(farmer_is_ip) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_is_ip;".format(FILTER_SUFFIX) ))
		mobile_head_hh = dic(query("SELECT `farmer_head_of_house` as `key`, count(farmer_head_of_house) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_head_of_house;".format(FILTER_SUFFIX) ))
		mobile_ip_grp = dic(query("SELECT `farmer_ip` as `key`, count(farmer_ip) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_ip;".format(FILTER_SUFFIX) ))
		mobile_fo = dic(query("SELECT `farmer_fo_name_rapid` as `key`, count(farmer_fo_name_rapid) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_fo_name_rapid;".format(FILTER_SUFFIX) ))
		mobile_dip = dic(query("SELECT `farmer_dip_ref` as `key`, count(farmer_dip_ref) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_dip_ref;".format(FILTER_SUFFIX) ))
		mobile_primary_c = dic(query("SELECT `farmer_primary_crop` as `key`, count(farmer_primary_crop) as `total` FROM form_a_farmer_profiles  {} GROUP by farmer_primary_crop;".format(FILTER_SUFFIX) ))

		mobile_geotag = query("SELECT `farmer_primary_crop`,`farmer_coords_long`,`farmer_coords_lat` FROM `form_a_farmer_profiles` {} AND `farmer_coords_lat` != '' AND `farmer_coords_lat` != ' ';".format(FILTER_SUFFIX))

		excl_sex = dic(query("SELECT `frmer_prof_@_basic_Info_@_Sex` as `key`, count(`frmer_prof_@_basic_Info_@_Sex`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_basic_Info_@_Sex`;".format(FILTER_SUFFIX) ))
		excl_ip = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_farmer_ip` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_farmer_ip`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_farmer_ip`;".format(FILTER_SUFFIX) ))
		excl_head_hh = dic(query("SELECT `frmer_prof_@_hh_Head_Info_@_is_head_og_household` as `key`, count(`frmer_prof_@_hh_Head_Info_@_is_head_og_household`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_hh_Head_Info_@_is_head_og_household`;".format(FILTER_SUFFIX) ))
		excl_ip_grp = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_farmer_ip` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_farmer_ip`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_farmer_ip`;".format(FILTER_SUFFIX) ))
		excl_fo = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_Name_coop` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_Name_coop`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_Name_coop`;".format(FILTER_SUFFIX) ))
		excl_dip = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_DIP_name` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_DIP_name`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_DIP_name`;".format(FILTER_SUFFIX) ))
		excl_primary_c = dic(query("SELECT `frmer_prof_@_Farming_Basic_Info_@_primary_crop` as `key`, count(`frmer_prof_@_Farming_Basic_Info_@_primary_crop`) as `total` FROM `excel_import_form_a`  {} GROUP by `frmer_prof_@_Farming_Basic_Info_@_primary_crop`;".format(FILTER_SUFFIX) ))
		


		if('untagged' not in mobile_dip):mobile_dip['untagged'] = 0
		if('untagged' not in mobile_fo):mobile_fo['untagged'] = 0
		if("" not in mobile_dip):mobile_dip[""] = 0
		if("" not in mobile_fo):mobile_fo[""] = 0

		with_dip = all_farmer_count - (mobile_dip['untagged']+excl_dip[""])
		with_fo = all_farmer_count - (mobile_fo['untagged']+excl_fo[""])



		primary_crop = Populate.primary_crop(mobile_primary_c,excl_primary_c)
		data = {
			"query_suffix" : FILTER_SUFFIX,
			"area_reg" : session["USER_DATA"][0]["office"],
			"all_farmer_count" : all_farmer_count,
			"all_sex_untag" : all_farmer_count + (mobile_sex['male'] + mobile_sex['female'] + excl_sex['male'] + excl_sex['female'] ),
			"all_sex_female" : mobile_sex['female'] + excl_sex['female'],
			"all_sex_male" : mobile_sex['male'] + excl_sex['male'],
			"is_ip_num" : all_farmer_count - (mobile_ip['false']+excl_ip[""]),
			"is_hh_head_num" : all_farmer_count - (mobile_head_hh['false']+excl_head_hh[""]),
			"with_dip": with_dip,
			"with_fo": with_fo,
			"mobile_geotag": mobile_geotag , 
			"ls_arr" : {
				"primary_crop" :{"main": primary_crop,"breakdown":{"excel": excl_primary_c , "mobile" : mobile_primary_c}},
				"ip_gr" :{"excel": excl_ip_grp , "mobile" : mobile_ip_grp},
				"fo" :{"excel": excl_fo , "mobile" : mobile_fo},
				"dip" :{"excel": excl_dip , "mobile" : mobile_dip},
			}
		}
		return data
		# return [all_mob_female[0]['f'],all_mob_male[0]['m']]

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
		print(sorted(new_comd))
		return sorted(new_comd.items(), key=lambda x:x[1], reverse=True)


class Filter:
	def position_data_filter():
		_filter = "WHERE 1 "
		JOB = session["USER_DATA"][0]["job"].lower()

		if(JOB in "admin" or JOB in "super admin"):
			session["USER_DATA"][0]["office"] = "NPCO"
			_filter = "WHERE 1 "
		else:
			session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
			_filter = "WHERE  USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])

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