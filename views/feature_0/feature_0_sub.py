from datetime import date 
from datetime import datetime as dt 
import datetime as DT 
from dateutil import relativedelta

from flask import Blueprint, render_template, request, session, redirect, jsonify, Response,send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os, random, json, shutil
from controllers.outbound import outbound as outb
from controllers.inbound import inbound as inb
from controllers.inbound import data_cleaning as  d_c
from werkzeug.utils import secure_filename

from controllers.engine_excel_to_sql import form_excel_a_handler

from multiprocessing import Process
import threading
import time, re

from difflib import SequenceMatcher
import pandas as pd
import json

app = Blueprint("feature_0_sub",__name__,template_folder='pages')
_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)

outbound = outb(app,rapid_mysql,session)
inbound = inb(app,rapid_mysql,session)
data_clean = d_c(app,rapid_mysql,session)

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)

class _main:
	def __init__(self, arg):
		print(" * main loading done")
		super(_main, self).__init__();
		self.arg = arg

	def is_on_session(): return ('USER_DATA' in session)
	# ===========================V1==========================================
	@app.route("/feature_0_sub",methods=["POST","GET"])
	@c.login_auth_web()
	def feature_0_sub():
		return {"status":"ok"}

	@app.route("/ffffffaaa",methods=["POST","GET"])
	@c.login_auth_web()
	def ffffffaaa():
		return rapid_mysql.select("SELECT * FROM `excel_import_form_a`",False)

	@app.route("/web_cast",methods=["POST","GET"])
	@c.login_auth_web()
	def web_cast():
		return render_template('web_cast.html')

	@app.route("/form_a/get_sub_form/<s_form>",methods=["POST","GET"])
	def get_sub_form(s_form):
		page = "form_a/"+s_form+".html"
		# print(page)
		return render_template(page)

	@app.route("/form_a/dash_a1/dash_get_form_a1/<area>",methods=["POST","GET"])
	def dash_get_form_a1(area):
		# print(area)
		return {"male":_main.dash_get_male(area),"female":_main.dash_get_female(area),"ha_area":_main.get_hectareage(area),"age_sex_area":_main.birthday_by_sex(area)}

	@app.route("/form_a/dash_a1/dash_get_male/<area>",methods=["POST","GET"])
	def dash_get_male(area):
		_filter(area)
		# m_c_male = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male';".format(_filter(area)) )[0]['count']
		# m_c_male_is_pwd = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_is_pwd`='true';".format(_filter(area)) )[0]['count']
		# m_c_male_is_ip = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_is_ip`='true';".format(_filter(area)) )[0]['count']
		# m_c_male_is_youth = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_age` BETWEEN '15' AND '30';".format(_filter(area)) )[0]['count']
		# m_c_male_is_sen_cit = rapid_mysql.select("SELECT COUNT(`farmer_code`)  as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_age` BETWEEN '60' AND '90';".format(_filter(area)) )[0]['count']
		# m_c_male_is_head_hh = rapid_mysql.select("SELECT COUNT(`farmer_code`)  as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_head_of_house` LIKE '%true%';".format(_filter(area)) )[0]['count']
		# =============
		ex_c_male = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male';".format(_filter(area)) )[0]['count']

		ex_c_male_is_pwd = ex_c_male - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male' AND `frmer_prof_@_Farming_Basic_Info_@_Farmer_pwd` = '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL MALE IN EXCEL

		ex_c_male_is_ip = ex_c_male - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male' AND `frmer_prof_@_Farming_Basic_Info_@_farmer_ip` != '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL MALE IN EXCEL
		ex_c_male_male_is_head_hh = ex_c_male - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male' AND (`frmer_prof_@_hh_Head_Info_@_is_head_og_household` ='' OR `frmer_prof_@_hh_Head_Info_@_is_head_og_household` LIKE 'no%');".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL MALE IN EXCEL

		_ex_mal_bday = rapid_mysql.select("SELECT `frmer_prof_@_basic_Info_@_birthday` as 'bday' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male' AND `frmer_prof_@_basic_Info_@_birthday` LIKE '%-%';".format(_filter(area)) )
		ex_c_male_is_youth = 0
		ex_c_male_sen_cit = 0

		current_year = date.today().year
		for bd in _ex_mal_bday:
			bday = bd['bday'].split("-")
			if(len(bday)==3):
				try:
					age = int(current_year)-int(bday[2])
					if(age <= 100):
						if(age >= 15 and age <=30):
							ex_c_male_is_youth += 1
						if(age >= 60 and age <=90):
							ex_c_male_sen_cit += 1
				except Exception as e:
					print(e)
		return {
			'total_mal':ex_c_male ,
			'male_is_pwd': ex_c_male_is_pwd,
			'male_is_ip': ex_c_male_is_ip,
			'male_is_youth': ex_c_male_is_youth,
			'male_is_sen_cit': ex_c_male_sen_cit,
			'male_is_head_hh': ex_c_male_male_is_head_hh
		}
		# return {
		# 	'total_mal':ex_c_male + m_c_male,
		# 	'male_is_pwd':m_c_male_is_pwd + ex_c_male_is_pwd,
		# 	'male_is_ip':m_c_male_is_ip + ex_c_male_is_ip,
		# 	'male_is_youth':m_c_male_is_youth + ex_c_male_is_youth,
		# 	'male_is_sen_cit':m_c_male_is_sen_cit + ex_c_male_sen_cit,
		# 	'male_is_head_hh':m_c_male_is_head_hh + ex_c_male_male_is_head_hh
		# 	}

	@app.route("/form_a/dash_a1/dash_get_female/<area>",methods=["POST","GET"])
	def dash_get_female(area):
		# m_c_female = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female';".format(_filter(area)) )[0]['count']

		# m_c_female_is_pwd = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_is_pwd`='true';".format(_filter(area)) )[0]['count']
		# m_c_female_is_ip = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_is_ip`='true';".format(_filter(area)) )[0]['count']
		# m_c_female_is_youth = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_age` BETWEEN '15' AND '30';".format(_filter(area)) )[0]['count']
		# m_c_female_is_sen_cit = rapid_mysql.select("SELECT COUNT(`farmer_code`)  as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_age` BETWEEN '60' AND '90';".format(_filter(area)) )[0]['count']
		# m_c_female_is_head_hh = rapid_mysql.select("SELECT COUNT(`farmer_code`)  as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_head_of_house` LIKE '%true%';".format(_filter(area)) )[0]['count']
		
		# =============
		ex_c_female = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female';".format(_filter(area)) )[0]['count']

		ex_c_female_is_pwd = ex_c_female - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female' AND `frmer_prof_@_Farming_Basic_Info_@_Farmer_pwd` = '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL female IN EXCEL

		ex_c_female_is_ip = ex_c_female - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female' AND `frmer_prof_@_Farming_Basic_Info_@_farmer_ip` != '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL female IN EXCEL
		ex_c_female_female_is_head_hh = ex_c_female - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female' AND (`frmer_prof_@_hh_Head_Info_@_is_head_og_household` ='' OR `frmer_prof_@_hh_Head_Info_@_is_head_og_household` LIKE 'no%');".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL MALE IN EXCEL

		_ex_mal_bday = rapid_mysql.select("SELECT `frmer_prof_@_basic_Info_@_birthday` as 'bday' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female' AND `frmer_prof_@_basic_Info_@_birthday` LIKE '%-%';".format(_filter(area)) )
		ex_c_female_is_youth = 0
		ex_c_female_sen_cit = 0

		current_year = date.today().year

		for bd in _ex_mal_bday:
			bday = bd['bday'].split("-")
			if(len(bday)==3):
				try:
					age = int(current_year)-int(bday[2])
					if(age <= 100):
						if(age >= 15 and age <=30):
							ex_c_female_is_youth += 1
						if(age >= 60 and age <=90):
							ex_c_female_sen_cit += 1
				except Exception as e:
					print(e)
		return {
			'total_female':ex_c_female,
			'female_is_pwd': ex_c_female_is_pwd,
			'female_is_ip': ex_c_female_is_ip,
			'female_is_youth': ex_c_female_is_youth,
			'female_is_sen_cit': ex_c_female_sen_cit,
			'female_is_head_hh': ex_c_female_female_is_head_hh
		}
		# return {
		# 	'total_female':ex_c_female + m_c_female,
		# 	'female_is_pwd':m_c_female_is_pwd + ex_c_female_is_pwd,
		# 	'female_is_ip':m_c_female_is_ip + ex_c_female_is_ip,
		# 	'female_is_youth':m_c_female_is_youth + ex_c_female_is_youth,
		# 	'female_is_sen_cit':m_c_female_is_sen_cit + ex_c_female_sen_cit,
		# 	'female_is_head_hh':m_c_female_is_head_hh + ex_c_female_female_is_head_hh
		# }

	@app.route("/form_a/clean_get_val_table/<col>",methods=["POST","GET"])
	def get_val_table(col):
		if(col in c.DATA_CLEAN_FORM_A_REF):
			try:
				sql = "SELECT `id`,`{}` as 'val' FROM `{}`;".format(c.DATA_CLEAN_FORM_A_REF[col]['col'],c.DATA_CLEAN_FORM_A_REF[col]['table'])
				sugg_vals = rapid_mysql.select(sql)
				return sugg_vals
			except Exception as e:
				print(e)
				return [{"id":"NONE","val":"None/Untagged/Error"}]
		else:
			return [{"id":"NONE","val":"None/Untagged/Unexistence"}]

	@app.route("/form_a/clean_set_val_table/<table>/<col>/<oldval>/<newval>",methods=["POST","GET"])
	def clean_set_val_table(table,col,oldval,newval):

		try:
			sql = "UPDATE `{}` SET `{}`='{}' WHERE `{}`='{}';".format(table,col,newval,col,oldval)
			# print(sql)
			row_ch = rapid_mysql.do(sql)
			return {"status":"done","data":row_ch}
		except Exception as e:
			return {"status":"Error","data":e}


	@app.route("/form_a/get_ind_data_val",methods=["POST","GET"])
	@c.login_auth_web()
	def get_ind_data_val():
		data = [];
		identifier_ = "" 
		record_id = request.form['record_id']
		table = request.form['tables'].split(",")
		table_count = len(table)
		print(table_count)

		if(table_count>1):
			identifier_ = "farmer_code"
			record_id = rapid_mysql.select("SELECT `farmer_code` FROM `form_a_farmer_profiles` WHERE `id`='{}' ;".format(record_id))[0]['farmer_code']
		else:
			identifier_ = "id"
			record_id = request.form['record_id']

		_res = {"len":len(table),"tables":table,"data":[]}
		_res[identifier_]=record_id

		for table_index in range(table_count):
			data.append(rapid_mysql.select("SELECT * FROM `{}` WHERE `{}`='{}';".format(table[table_index],identifier_, record_id )))
		_res['data'] = data
		return _res

	@app.route("/form_a/del_profile",methods=["POST","GET"])
	def del_profile():
		if(_main.is_on_session()):
			ids = request.form["id"]
			delid = rapid_mysql.do("DELETE FROM `excel_import_form_a` WHERE `id`='{}'; ".format(ids))
			return {"id":delid}
		else:
			return redirect("/login?force_url=1")
			
	# ===============================================


	@app.route("/data_link/search_farmer_org",methods=["POST","GET"])
	@c.login_auth_web()
	def search_farmer_org():
		search_item = request.form['search_item']
		data_ex = '''
			SELECT 
				`id`,
				`organization_registered_name` as 'fname',
				`id` as 'reference',
				`office_business_adrress` as 'addr_brgy'
			FROM 
				`form_b` 
			WHERE 
				`organization_registered_name` LIKE "%{}%" ;
		'''.format(search_item)
		print(data_ex)
		ind = rapid_mysql.select(data_ex)
		return jsonify(ind)


	
	def similar(a, b):
		return SequenceMatcher(None, a, b).ratio()

	@app.route("/data_link/search_farmer_profile",methods=["POST","G ET"])
	@c.login_auth_web()
	def search_farmer_profile():
		search_item = request.form['search_item'].lower()
		return jsonify(_main.get_search_val(search_item))

	def get_search_val(search_item):
		for k in search_item.split("\n"):
			search_item = (re.sub(r"[^a-zA-Z0-9]+", ' ', k))

		tem_Str = []
		for strs in search_item.split(" "):
			tem_Str.append("'{}'".format(strs))

		search_item =",".join(tem_Str)
		# print(search_item)

		data_ex = '''
			SELECT 
				`id`,
				 CONCAT(`frmer_prof_@_basic_Info_@_First_name`,' ',`frmer_prof_@_basic_Info_@_Middle_name`,' ',`frmer_prof_@_basic_Info_@_Last_name`) as 'fname',
				`file_name` as 'reference',
				`frmer_prof_@_basic_Info_@_birthday` as 'farmer_bday',
				`frmer_prof_@_frmer_addr_@_region` as 'addr_region',
				`frmer_prof_@_frmer_addr_@_province` as 'addr_prov',
				`frmer_prof_@_frmer_addr_@_city_municipality` as 'addr_city',
				`frmer_prof_@_frmer_addr_@_brgy` as 'addr_brgy',
				`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as 'farmer_primary_crop',
				`frmer_prof_@_basic_Info_@_Sex` as 'sex',
				`frmer_prof_@_basic_Info_@_civil_status` as 'civil_status'
			FROM 
				`excel_import_form_a` 
			WHERE 
				`frmer_prof_@_basic_Info_@_First_name` in ({}) OR
				`frmer_prof_@_basic_Info_@_Middle_name` in ({}) OR
				`frmer_prof_@_basic_Info_@_Last_name` in ({});
		'''.format(search_item,search_item,search_item)
		# ind = rapid_mysql.select(data_m) + rapid_mysql.select(data_ex)  # DEPRICATEA MOBILE ENTRIES
		
		ind = rapid_mysql.select(data_ex)
		while len(ind)>10 :
			array_counter = 0
			for items_ in ind:
				if array_counter != 0:
					if(_main.similar(search_item,ind[array_counter]['fname'])>_main.similar(search_item,ind[array_counter-1]['fname'])):
						del ind[array_counter-1]
					else:
						del ind[array_counter]
				array_counter +=1

		array_counter = 0
		for items_ in ind:
			ind[array_counter]["search_acc"] = _main.similar(search_item,ind[array_counter]['fname'])
			# print(f"Search : {search_item} | Result : {items_['fname']} >> {_main.similar(search_item,items_['fname'])}")
			array_counter +=1

		ind = sorted(ind, key=lambda x: x["search_acc"],reverse=True)
		return ind

	@app.route("/data_link/sent_attn/<form_id>/<db_table>",methods=["POST","GET"])
	def search_fromExcel(form_id,db_table):
		if 'file' not in request.files:
			return "No file part"

		file = request.files['file']
		if file.filename == '':
			return "No selected file"
		excel_data_df = pd.read_excel(file)
		thisisjson = excel_data_df.to_json(orient='records')
		thisisjson_dict = json.loads(thisisjson)
		arr_c =0
		for name in thisisjson_dict:
			thisisjson_dict[arr_c]["search_res"] = _main.get_search_val(name["NAME / ORG NAME"])
			arr_c += 1
		_main.add_to_benef_list(thisisjson_dict,form_id,db_table)
		return jsonify(thisisjson_dict)

	@app.route("/data_link/search_from_db",methods=["POST","GET"])
	def search_from_db():
		item = request.form['item']
		return jsonify(_main.get_search_val(item))


	@app.route("/data_link/replace_item_to_sync/<db_table>/<form_id>",methods=["POST","GET"])
	def replace_item_to_sync(db_table,form_id):
		matched_entry = json.loads(request.form["matched_item"])
		print(matched_entry)
		selected_entry = request.form["selected_entry_id"]
		is_exist = rapid_mysql.select(f'''
			SELECT * FROM `__data_link_1` WHERE `link_to_id`='{matched_entry["id"]}' AND `db_table`='{db_table}';
		''')
		if(len(is_exist)>0):
			return {"status":"error","msg":"Record selected was already in the lists. Kindly delete the entry on the list that you think has a duplicate entry on the database otherwise select another profile "}
		else:
			from_entries = rapid_mysql.select(f'''
				SELECT * FROM `__data_link_1` WHERE `id`='{selected_entry}';
			''')[0]
			del from_entries["not_recorded"]
			_SQL = (f'''
				UPDATE `__data_link_1` 
				SET 
					`remarks` = 'Synced',
					`addr_brgy` = '{matched_entry["addr_brgy"]}',
					`addr_city` = '{matched_entry["addr_city"]}',
					`addr_prov` = '{matched_entry["addr_prov"]}',
					`addr_region` = '{matched_entry["addr_region"]}',
					`civil_status` = '{matched_entry["civil_status"]}',
					`db_table` = '{db_table}',
					`farmer_bday` = '{matched_entry["farmer_bday"]}',
					`farmer_primary_crop` = '{matched_entry["farmer_primary_crop"]}',
					`fname` = '{matched_entry["fname"]}',
					`link_from_id` = '{form_id}',
					`link_to_id` = '{matched_entry["id"]}',
					`reference` = '{matched_entry["reference"]}',
					`sex` = '{matched_entry["sex"]}',
					`not_recorded` = {json.dumps(str(from_entries))}
				WHERE
					`id` = '{selected_entry}'
			;''')
			rapid_mysql.do(_SQL)
			return {"status":"success","msg":"Data link was successfull"}

	def add_to_benef_list(_data,form_id,db_table):
		for _datum in _data:
			sql = (f'''
				INSERT INTO `__data_link_1`
				(	
					`addr_brgy`,
					`addr_city`,
					`addr_prov`,
					`addr_region`,
					`civil_status`,
					`db_table`,
					`farmer_primary_crop`,
					`fname`,
					`link_from_id`,
					`sex`
				)
				VALUES
					(
					'{_datum["BARANGAY"]}',
					'{_datum["CITY/MUNICIPALITY"]}',
					'{_datum["PROVINCE"]}',
					'{_datum["REGION"]}',
					'{_datum["SECTORAL( ,Seprated)"]}',
					'{db_table}',
					'{_datum["PRIMARY CROP (If Applicable)"]}',
					'{_datum["NAME / ORG NAME"]}',
					'{form_id}',
					'{_datum["SEX (If Applicable)"]}'
					);
			''')
			rapid_mysql.do(sql)
		pass


	def birthday_by_sex(area):
		query = rapid_mysql.select
		q = '''
			SELECT 
				`frmer_prof_@_basic_Info_@_Sex` as 'sex',
				`frmer_prof_@_basic_Info_@_birthday` as 'bday'
			FROM `excel_import_form_a` {}
			;'''.format(_main.___filter(area) )

		bday = query(q)
		ALL_BDAY = {"female":[],"male":[]}
		tital_num_farmer = 0
		tital_num_farmer_valid = 0
		for inx in range(len(bday)):

			temp_sex = bday[inx]["sex"].lower().replace(" ","")
			temp_bday = bday[inx]["bday"]
			if temp_sex not in ALL_BDAY:continue

			if("-" in temp_sex): 
				if(len(temp_bday.split("-")[0])==4):
					ALL_BDAY[temp_sex].append(temp_bday)
			elif("." in temp_bday ):
				try:
					int_bday = int(str(temp_bday).split(".")[0])
				except Exception as e:
					int_bday = 0
				reference_date = date(1900, 1, 1)
				days_since_epoch = int_bday
				target_date = reference_date + DT.timedelta(days=days_since_epoch)
				formatted_date = target_date.strftime('%Y-%m-%d')
				ALL_BDAY[temp_sex].append(formatted_date)
			tital_num_farmer +=1

		# return ALL_BDAY #=================================================
		# print(DT.date.today())
		all_years = []
		age_range = {
			"youth" : {"male":0,"female":0},
			"75-100":{"male":0,"female":0},"70-74":{"male":0,"female":0},"65-69":{"male":0,"female":0},"60-64":{"male":0,"female":0},"55-59":{"male":0,"female":0},"50-54":{"male":0,"female":0},"45-49":{"male":0,"female":0},"40-44":{"male":0,"female":0},"35-39":{"male":0,"female":0},"30-34":{"male":0,"female":0},"25-29":{"male":0,"female":0},"20-24":{"male":0,"female":0},"15-19":{"male":0,"female":0},"10-14":{"male":0,"female":0},"none":{"male":0,"female":0}
		}
		for _sex in ALL_BDAY:
			for _date in ALL_BDAY[_sex]:
				xdate = _date.split("-")
				if(int(xdate[1])>12):
					# print(_date)
					_date = f"{xdate[0]}-01-01"
				start_date = dt.strptime(_date, "%Y-%m-%d")
				end_date = DT.date.today()
				delta = relativedelta.relativedelta(end_date, start_date)
				# print(delta.years, 'Years,', delta.months, 'months,', delta.days, 'days')
				tital_num_farmer_valid += 1
				YEARS_OLD = delta.years
				age_range[_main.get_age_range(YEARS_OLD)][_sex] += 1
				if(YEARS_OLD >= 15 and YEARS_OLD <= 30 ):
					age_range["youth"][_sex] += 1
		return {"age_range":age_range,"bdays":[],"tital_num_farmer_valid":tital_num_farmer_valid,"tital_num_farmer":tital_num_farmer}

	def get_age_range(AGE_):
		ranges = [(75, 100),(70, 74),(65, 69),(60, 64),(55, 59),(50, 54),(45, 49),(40, 44),(35, 39),(30, 34),(25, 29),(20, 24),(15, 19),(10, 14)]

		def find_range(number, ranges):
			for start, end in ranges:
				if start <= number <= end:
					return (start, end)
			return None
		number = AGE_
		range_found = find_range(number, ranges)
		if range_found:
			return f"{range_found[0]}-{range_found[1]}"
		else:
			return f"none"


	def get_hectareage(area):
		_CC =  {
				"income_primary": 0,
				"income_primary_count":0,
				"income_avg":0,
				"num_farmers": 0,
				"num_farmers_has_inc": 0
			}
		segre ={
			"male":{
				"below_to_0_5": {
					"total": 0,
					"commodity": {}
				},
				"0_5_to_1": {
					"total": 0,
					"commodity": {}
				},
				"1_01_to_1_5": {
					"total": 0,
					"commodity": {}
				},
				"1_6_to_2": {
					"total": 0,
					"commodity": {}
				},
				"2_01_to_2_5": {
					"total": 0,
					"commodity": {}
				},
				"2_6_to_3": {
					"total": 0,
					"commodity": {}
				},
				"3_01_to_3_5": {
					"total": 0,
					"commodity": {}
				},
				# ===
				"3_6_to_4": {
					"total": 0,
					"commodity": {}
				},
				"4_01_to_4_5": {
					"total": 0,
					"commodity": {}
				},
				"4_59_to_5": {
					"total": 0,
					"commodity": {}
				},
				"5_above": {
					"total": 0,
					"commodity": {}
				},
				"untagged": {
					"total": 0,
					"commodity": {}
				}
			},
			"female":{
				"below_to_0_5": {
					"total": 0,
					"commodity": {}
				},
				"0_5_to_1": {
					"total": 0,
					"commodity": {}
				},
				"1_01_to_1_5": {
					"total": 0,
					"commodity": {}
				},
				"1_6_to_2": {
					"total": 0,
					"commodity": {}
				},
				"2_01_to_2_5": {
					"total": 0,
					"commodity": {}
				},
				"2_6_to_3": {
					"total": 0,
					"commodity": {}
				},
				"3_01_to_3_5": {
					"total": 0,
					"commodity": {}
				},
				# ===
				"3_6_to_4": {
					"total": 0,
					"commodity": {}
				},
				"4_01_to_4_5": {
					"total": 0,
					"commodity": {}
				},
				"4_59_to_5": {
					"total": 0,
					"commodity": {}
				},
				"5_above": {
					"total": 0,
					"commodity": {}
				},
				"untagged": {
					"total": 0,
					"commodity": {}
				}
			},
			# ////FEMALE................
		}
		actual = {}
		_CROP = ["coconut","","cacao","coffee","banana","calamansi"]
		query = rapid_mysql.select
		q = '''
			SELECT 
				`farm_info@_Farm_Basic_Info_@_declared_area_Ha` as 'ha',
				`frmer_prof_@_basic_Info_@_Sex` as 'sex',
				`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Primary_Crop_` as 'income_primary',
				`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Secondary_Crop_` as 'income_secondary',
				`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as 'crop'
			FROM `excel_import_form_a` {}
			;'''.format(_main.___filter(area))
		print(q)
		hectareage = query(q)

		_CROP = ["coconut","","cacao","coffee","banana","calamansi"]
		simp = {
			"male": {
				"below_to_0_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"0_5_to_1":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"1_01_to_1_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"1_6_to_2":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"2_01_to_2_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"2_6_to_3":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"3_01_to_3_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},

				"3_6_to_4":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"4_01_to_4_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"4_59_to_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},

				"5_above":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"untagged":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0}
			},
			"female": {
				"below_to_0_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"0_5_to_1":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"1_01_to_1_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"1_6_to_2":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"2_01_to_2_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"2_6_to_3":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"3_01_to_3_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"3_6_to_4":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"4_01_to_4_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"4_59_to_5":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"5_above":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0},
				"untagged":{"total_inc":0,"ave_income":0,"num_farmer_has_inc":0,"num_farmers":0}
			},
		}

		for details in hectareage:
			ha__ = re.sub(r"[a-zA-Z]", '', details['ha'])
			SEX = details["sex"].lower().replace(" ","")
			_CC =  {
					"income_primary": 0,
					"income_primary_count":0,
					"income_avg":0,
					"num_farmers": 0,
					"num_farmers_has_inc": 0
				}
			if(SEX not in segre):print(f"sex[{SEX}]"); continue
			try: INC_PRIME = float(details["income_primary"])
			except Exception as e: INC_PRIME= 0
			try:ha = float(ha__)
			except Exception as e:ha = 0
			
			if(ha not in actual):
				actual[ha] = 0
			actual[ha]+=1
			CROP = ''.join(letter for letter in details["crop"].lower() if letter.isalnum())
			if(CROP not in _CROP):
				CROP = "others"

			if(ha <= 0.5):
				segre[SEX]["below_to_0_5"]["total"] +=1;
				if(CROP not in segre[SEX]["below_to_0_5"]["commodity"]):
					segre[SEX]["below_to_0_5"]["commodity"][CROP] = _CC
				segre[SEX]["below_to_0_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["below_to_0_5"]["commodity"][CROP]["income_primary"]  +=INC_PRIME
				simp[SEX]["below_to_0_5"]["num_farmer_has_inc"] += 1
				segre[SEX]["below_to_0_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["below_to_0_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["below_to_0_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["below_to_0_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["below_to_0_5"]["total_inc"] += INC_PRIME

			elif(ha > 0.5 and ha <= 1.0):
				segre[SEX]["0_5_to_1"]["total"] +=1;
				if(CROP not in segre[SEX]["0_5_to_1"]["commodity"]):
					segre[SEX]["0_5_to_1"]["commodity"][CROP] = _CC
				segre[SEX]["0_5_to_1"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["0_5_to_1"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["0_5_to_1"]["num_farmer_has_inc"] += 1
				segre[SEX]["0_5_to_1"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["0_5_to_1"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["0_5_to_1"]["commodity"][CROP]["income_primary"]/segre[SEX]["0_5_to_1"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["0_5_to_1"]["total_inc"] += INC_PRIME

			elif(ha > 1.01 and ha <= 1.5):
				segre[SEX]["1_01_to_1_5"]["total"] +=1;
				if(CROP not in segre[SEX]["1_01_to_1_5"]["commodity"]):
					segre[SEX]["1_01_to_1_5"]["commodity"][CROP] = _CC
				segre[SEX]["1_01_to_1_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["1_01_to_1_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["1_01_to_1_5"]["num_farmer_has_inc"] += 1
				segre[SEX]["1_01_to_1_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["1_01_to_1_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["1_01_to_1_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["1_01_to_1_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["1_01_to_1_5"]["total_inc"] += INC_PRIME

			elif(ha > 1.6 and ha <= 2.0):
				segre[SEX]["1_6_to_2"]["total"] +=1;
				if(CROP not in segre[SEX]["1_6_to_2"]["commodity"]):
					segre[SEX]["1_6_to_2"]["commodity"][CROP] = _CC
				segre[SEX]["1_6_to_2"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["1_6_to_2"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["1_6_to_2"]["num_farmer_has_inc"] += 1
				segre[SEX]["1_6_to_2"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["1_6_to_2"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["1_6_to_2"]["commodity"][CROP]["income_primary"]/segre[SEX]["1_6_to_2"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["1_6_to_2"]["total_inc"] += INC_PRIME

			elif(ha > 2.01 and ha <= 2.5):
				segre[SEX]["2_01_to_2_5"]["total"] +=1;
				if(CROP not in segre[SEX]["2_01_to_2_5"]["commodity"]):
					segre[SEX]["2_01_to_2_5"]["commodity"][CROP] = _CC
				segre[SEX]["2_01_to_2_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["2_01_to_2_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["2_01_to_2_5"]["num_farmer_has_inc"] += 1
				segre[SEX]["2_01_to_2_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["2_01_to_2_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["2_01_to_2_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["2_01_to_2_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["2_01_to_2_5"]["total_inc"] += INC_PRIME

			elif(ha > 2.06and ha <= 3.0):
				segre[SEX]["2_6_to_3"]["total"] +=1;
				if(CROP not in segre[SEX]["2_6_to_3"]["commodity"]):
					segre[SEX]["2_6_to_3"]["commodity"][CROP] = _CC
				segre[SEX]["2_6_to_3"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["2_6_to_3"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["2_6_to_3"]["num_farmer_has_inc"] += 1
				segre[SEX]["2_6_to_3"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["2_6_to_3"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["2_6_to_3"]["commodity"][CROP]["income_primary"]/segre[SEX]["2_6_to_3"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["2_6_to_3"]["total_inc"] += INC_PRIME

			elif(ha > 3.01 and ha <= 3.5):
				segre[SEX]["3_01_to_3_5"]["total"] +=1;
				if(CROP not in segre[SEX]["3_01_to_3_5"]["commodity"]):
					segre[SEX]["3_01_to_3_5"]["commodity"][CROP] = _CC
				segre[SEX]["3_01_to_3_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["3_01_to_3_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["3_01_to_3_5"]["num_farmer_has_inc"] += 1
				segre[SEX]["3_01_to_3_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["3_01_to_3_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["3_01_to_3_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["3_01_to_3_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["3_01_to_3_5"]["total_inc"] += INC_PRIME

			elif(ha > 3.06 and ha <= 3.5):
				segre[SEX]["3_06_to_3_5"]["total"] +=1;
				if(CROP not in segre[SEX]["3_06_to_3_5"]["commodity"]):
					segre[SEX]["3_06_to_3_5"]["commodity"][CROP] = _CC
				segre[SEX]["3_06_to_3_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["3_06_to_3_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["3.06 to 3.5"]["num_farmer_has_inc"] += 1
				segre[SEX]["3_06_to_3_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["3_06_to_3_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["3_06_to_3_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["3_06_to_3_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["3.06 to 3.5"]["total_inc"] += INC_PRIME
			# =====================
			# =====================

			elif(ha > 3.06 and ha <= 4):
				segre[SEX]["3_6_to_4"]["total"] +=1;
				if(CROP not in segre[SEX]["3_6_to_4"]["commodity"]):
					segre[SEX]["3_6_to_4"]["commodity"][CROP] = _CC
				segre[SEX]["3_6_to_4"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["3_6_to_4"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["3_6_to_4"]["num_farmer_has_inc"] += 1
				segre[SEX]["3_6_to_4"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["3_6_to_4"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["3_6_to_4"]["commodity"][CROP]["income_primary"]/segre[SEX]["3_6_to_4"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["3_6_to_4"]["total_inc"] += INC_PRIME

			elif(ha > 4.01 and ha <= 4.5):
				segre[SEX]["4_01_to_4_5"]["total"] +=1;
				if(CROP not in segre[SEX]["4_01_to_4_5"]["commodity"]):
					segre[SEX]["4_01_to_4_5"]["commodity"][CROP] = _CC
				segre[SEX]["4_01_to_4_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["4_01_to_4_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["4_01_to_4_5"]["num_farmer_has_inc"] += 1
				segre[SEX]["4_01_to_4_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["4_01_to_4_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["4_01_to_4_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["4_01_to_4_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["4_01_to_4_5"]["total_inc"] += INC_PRIME

			elif(ha > 4.59 and ha <= 5):
				segre[SEX]["4_59_to_5"]["total"] +=1;
				if(CROP not in segre[SEX]["4_59_to_5"]["commodity"]):
					segre[SEX]["4_59_to_5"]["commodity"][CROP] = _CC
				segre[SEX]["4_59_to_5"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["4_59_to_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["4_59_to_5"]["num_farmer_has_inc"] += 1
				segre[SEX]["4_59_to_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["4_59_to_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["4_59_to_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["4_59_to_5"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["4_59_to_5"]["total_inc"] += INC_PRIME

			# elif(ha > 4.59 and ha <= 4.5):
			# 	segre[SEX]["4_59_to_5"]["total"] +=1;
			# 	if(CROP not in segre[SEX]["4_59_to_5"]["commodity"]):
			# 		segre[SEX]["4_59_to_5"]["commodity"][CROP] = _CC
			# 	segre[SEX]["4_59_to_5"]["commodity"][CROP]["num_farmers"] += 1
			# 	try:
			# 		segre[SEX]["4_59_to_5"]["commodity"][CROP]["income_primary"] += INC_PRIME
			# 		simp[SEX]["4_59_to_5"]["num_farmer_has_inc"] += 1
			# 		segre[SEX]["4_59_to_5"]["commodity"][CROP]["num_farmers_has_inc"] +=1
			# 		segre[SEX]["4_59_to_5"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["4_59_to_5"]["commodity"][CROP]["income_primary"]/segre[SEX]["4_59_to_5"]["commodity"][CROP]["num_farmers_has_inc"])

			# 	except ValueError:
			# 		pass
			# 	simp[SEX]["4_59_to_5"]["total_inc"] += INC_PRIME



			# =====================
			# =====================
			# =====================
			# =====================
			elif(ha > 5):
				segre[SEX]["5_above"]["total"] +=1;
				if(CROP not in segre[SEX]["5_above"]["commodity"]):
					segre[SEX]["5_above"]["commodity"][CROP] = _CC
				segre[SEX]["5_above"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["5_above"]["commodity"][CROP]["income_primary"] += INC_PRIME
				simp[SEX]["5_above"]["num_farmer_has_inc"] += 1
				segre[SEX]["5_above"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				segre[SEX]["5_above"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["5_above"]["commodity"][CROP]["income_primary"]/segre[SEX]["5_above"]["commodity"][CROP]["num_farmers_has_inc"])
				simp[SEX]["5_above"]["total_inc"] += INC_PRIME

			else:
				segre[SEX]["untagged"]["total"] +=1;
				if(CROP not in segre[SEX]["untagged"]["commodity"]):
					segre[SEX]["untagged"]["commodity"][CROP] = _CC
				segre[SEX]["untagged"]["commodity"][CROP]["num_farmers"] += 1
				segre[SEX]["untagged"]["commodity"][CROP]["income_primary"] += INC_PRIME
				segre[SEX]["untagged"]["commodity"][CROP]["num_farmers_has_inc"] +=1
				simp[SEX]["untagged"]["num_farmer_has_inc"] += 1
				segre[SEX]["untagged"]["commodity"][CROP]["income_avg"] = "{:.2f}".format(segre[SEX]["untagged"]["commodity"][CROP]["income_primary"]/segre[SEX]["untagged"]["commodity"][CROP]["num_farmers_has_inc"])

				simp[SEX]["untagged"]["total_inc"] += INC_PRIME


		myKeys = list(actual.keys())
		myKeys.sort()
		sorted_dict = {i: actual[i] for i in myKeys}
		# print(sorted_dict)
		# return sorted_dict.update(segre)
		for z in simp:
			for zz in simp[z]:
				try:
					simp[z][zz]["ave_income"] = simp[z][zz]["total_inc"] / simp[z][zz]["num_farmer_has_inc"]
				except Exception as e:
					# raise e
					# print(f'''{simp[z][zz]["total_inc"]} / {simp[z][zz]["num_farmer_has_inc"]}''')
					pass
		
		return {"detailed":segre,"simple":simp}

	def ___filter(area):
		_filter =""
		if(area.lower() == "all"):
			return ";"
		else:
			return "WHERE `USER_ID` in ( SELECT `id` from `users` WHERE `rcu`='{}' );".format(area)
		return _filter


def _filter(area):
	_filter =""
	if(area.lower() == "all"):
		_filter =""
	else:
		_filter = "USER_ID in ( SELECT id from users WHERE rcu='{}' ) AND".format(area)
	return _filter



# netbank
# christian
# 900118000017442