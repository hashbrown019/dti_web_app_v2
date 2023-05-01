from datetime import date, datetime
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
import time

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
	def feature_0_sub():
		return {"status":"ok"}

	@app.route("/form_a/get_sub_form/<s_form>",methods=["POST","GET"])
	def get_sub_form(s_form):
		page = "form_a/"+s_form+".html"
		print(page)
		return render_template(page)

	@app.route("/form_a/dash_a1/dash_get_form_a1/<area>",methods=["POST","GET"])
	def dash_get_form_a1(area):
		print(area)
		return {"male":_main.dash_get_male(area),"female":_main.dash_get_female(area)}

	@app.route("/form_a/dash_a1/dash_get_male/<area>",methods=["POST","GET"])
	def dash_get_male(area):
		_filter(area)
		m_c_male = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male';".format(_filter(area)) )[0]['count']

		m_c_male_is_pwd = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_is_pwd`='true';".format(_filter(area)) )[0]['count']
		m_c_male_is_ip = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_is_ip`='true';".format(_filter(area)) )[0]['count']
		m_c_male_is_youth = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_age` BETWEEN '15' AND '30';".format(_filter(area)) )[0]['count']
		m_c_male_is_sen_cit = rapid_mysql.select("SELECT COUNT(`farmer_code`)  as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'male' AND `farmer_age` BETWEEN '60' AND '90';".format(_filter(area)) )[0]['count']
		# =============
		ex_c_male = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male';".format(_filter(area)) )[0]['count']

		ex_c_male_is_pwd = ex_c_male - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male' AND `frmer_prof_@_Farming_Basic_Info_@_Farmer_pwd` = '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL MALE IN EXCEL

		ex_c_male_is_ip = ex_c_male - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='male' AND `frmer_prof_@_hh_Head_Info_@_head_hh_ip` = '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL MALE IN EXCEL

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
			'total_mal':ex_c_male + m_c_male,
			'male_is_pwd':m_c_male_is_pwd + ex_c_male_is_pwd,
			'male_is_ip':m_c_male_is_ip + ex_c_male_is_ip,
			'male_is_youth':m_c_male_is_youth + ex_c_male_is_youth,
			'male_is_sen_cit':m_c_male_is_sen_cit + ex_c_male_sen_cit
			}

		
	@app.route("/form_a/dash_a1/dash_get_female/<area>",methods=["POST","GET"])
	def dash_get_female(area):
		m_c_female = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female';".format(_filter(area)) )[0]['count']

		m_c_female_is_pwd = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_is_pwd`='true';".format(_filter(area)) )[0]['count']
		m_c_female_is_ip = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_is_ip`='true';".format(_filter(area)) )[0]['count']
		m_c_female_is_youth = rapid_mysql.select("SELECT COUNT(`farmer_code`) as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_age` BETWEEN '15' AND '30';".format(_filter(area)) )[0]['count']
		m_c_female_is_sen_cit = rapid_mysql.select("SELECT COUNT(`farmer_code`)  as 'count' FROM `form_a_farmer_profiles` WHERE {} `farmer_sex` = 'female' AND `farmer_age` BETWEEN '60' AND '90';".format(_filter(area)) )[0]['count']
		# =============
		ex_c_female = rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female';".format(_filter(area)) )[0]['count']

		ex_c_female_is_pwd = ex_c_female - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female' AND `frmer_prof_@_Farming_Basic_Info_@_Farmer_pwd` = '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL female IN EXCEL

		ex_c_female_is_ip = ex_c_female - rapid_mysql.select("SELECT COUNT(`id`) as 'count' FROM `excel_import_form_a` WHERE {} `frmer_prof_@_basic_Info_@_Sex`='female' AND `frmer_prof_@_hh_Head_Info_@_head_hh_ip` = '';".format(_filter(area)) )[0]['count'] # SUBTRACT TO THE TOTAL female IN EXCEL

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
			'total_female':ex_c_female + m_c_female,
			'female_is_pwd':m_c_female_is_pwd + ex_c_female_is_pwd,
			'female_is_ip':m_c_female_is_ip + ex_c_female_is_ip,
			'female_is_youth':m_c_female_is_youth + ex_c_female_is_youth,
			'female_is_sen_cit':m_c_female_is_sen_cit + ex_c_female_sen_cit
			}


def _filter(area):
	_filter =""
	if(area.lower() == "all"):
		_filter =""
	else:
		_filter = "USER_ID in ( SELECT id from users WHERE rcu='{}' ) AND".format(area)

	return _filter