from modules.Connections import mysql,sqlite
import Configurations as c
from flask import session
import json
from modules.Req_Brorn_util import authenication ## NO UTHENITICATION/SESSION HOLDER

rapid_mysql = mysql(*c.DB_CRED)


def get_profiling_form_a(req):
	profiles = rapid_mysql.select(f'''
		SELECT 
			`id`,
			`frmer_prof_@_basic_Info_@_First_name` as 'fname',
			`frmer_prof_@_basic_Info_@_Middle_name` as 'mname',
			`frmer_prof_@_basic_Info_@_Last_name` as 'lname',
			`frmer_prof_@_basic_Info_@_Extension_name` as 'xname',
			`frmer_prof_@_basic_Info_@_Sex` as 'sex',
			`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as 'primary_crop',
			`frmer_prof_@_Farming_Basic_Info_@_Name_coop` as 'fo',
			`frmer_prof_@_Farming_Basic_Info_@_DIP_name` as 'dip',
			`frmer_prof_@_frmer_addr_@_region` as 'region',
			`frmer_prof_@_frmer_addr_@_province` as 'prov',
			`frmer_prof_@_frmer_addr_@_city_municipality` as 'city',
			`file_name` as 'ref'
		FROM
			`excel_import_form_a`
		WHERE
			{position_data_filter()}
		;
	''')
	return profiles

def get_pfa_profile(req):
	pfa_id =  req.args['fields']
	return rapid_mysql.select(f"SELECT * FROM `excel_import_form_a` WHERE `id`={pfa_id};")[0]

# ==========================================
# ==========================================
# ==========================================
# ==========================================
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

