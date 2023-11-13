from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, Response,send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os, random, json, shutil, base64, sys, warnings, csv, xlrd
from controllers.outbound import outbound as outb
from controllers.inbound import inbound as inb
from controllers.inbound import data_cleaning as  d_c
from werkzeug.utils import secure_filename
from controllers.engine_excel_to_sql import form_excel_a_handler

import pandas as pd
from tqdm import tqdm

app = Blueprint("fundtracker",__name__,template_folder='pages')

_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)

outbound = outb(app,rapid_mysql,session)
inbound = inb(app,rapid_mysql,session)
data_clean = d_c(app,rapid_mysql,session)
# app = Flask(__name__)
	
@app.route("/fundtracker")
@app.route("/fundtracker/dashboard")
def dashboard():
	return render_template('ft_index.html',USER_DATA=session["USER_DATA"][0])


@app.route("/fundtracker/submit_entry_ft_main",methods = ["POST"])
def submit_entry_ft_main():
	form_data = request.form
	_key = ""; _val="";args=""

	is_exist = len(rapid_mysql.select("SELECT * FROM `ft_main` WHERE `id` ='{}' ;".format(request.form['id'])))
	if(is_exist==0):
		for key in form_data:
			print(key+" : "+form_data[key])
			_key += ",`"+key+"`"
			_val += ",'"+form_data[key]+"'"
		sql = ("INSERT INTO `{}` ({}) VALUES ({})".format("ft_main",_key[1:],_val[1:]))
	else:
		print("Editing")
		for datum in form_data:
			args += ",`{}`='{}'".format(datum,form_data[datum])
		sql = "UPDATE `ft_main` SET  {} WHERE `id`='{}';".format(args[1:],request.form['id'])
	
	last_row_id = rapid_mysql.do(sql)
	return {"msg":"done","last_row_id":last_row_id}
	# return render_template('ft_index.html',USER_DATA=session["USER_DATA"][0])


@app.route("/fundtracker/get_table_data",methods = ["POST","GET"])
def get_table_data():
	output_ = rapid_mysql.select("SELECT * FROM `ft_per_output`;")
	object_ = rapid_mysql.select("SELECT * FROM `ft_object`;")
	main_ = rapid_mysql.select("SELECT * FROM `ft_main`;")
	return {"output":output_,"object":object_,"main":main_}


@app.route("/fundtracker/get_entries_main",methods = ["POST","GET"])
def get_entries_main():
	resps = rapid_mysql.select('''
			SELECT `ft_main`.`id`,
					`ft_main`.`particulars`,
					`ft_main`.`payee_supplier`,
					`ft_per_output`.`component`,
					`ft_object`.`objectclass`,
					`ft_main`.`ifad_app_ref`,
					`users`.`rcu`,
					`users`.`pcu`
			FROM `ft_main` 
			INNER JOIN `ft_per_output` ON `ft_main`.`output_desc` = `ft_per_output`.`id` 
			INNER JOIN `ft_object` ON `ft_main`.`exp_acc` = `ft_object`.`id` 
			INNER JOIN `users` ON `ft_main`.`input_by` = `users`.`id` 
			{};'''.format(Filter.position_data_filter()),False)
	return resps


@app.route("/fundtracker/get_entries_main_ind",methods = ["POST","GET"])
def get_entries_main_ind():
	ids = request.form['id']
	resps = rapid_mysql.select("SELECT * FROM `ft_main` WHERE `id`='{}';".format(ids))
	return resps

@app.route("/fundtracker/dashboard_data",methods = ["POST","GET"])
def dashboard_data():
	ids = request.form['id']
	resps = rapid_mysql.select("SELECT * FROM `ft_main` WHERE `id`='{}';".format(ids))
	return resps


class Filter:
	def position_data_filter():
		_filter = "WHERE 1 "
		JOB = session["USER_DATA"][0]["job"].lower()

		if(JOB in "admin" or JOB in "super admin"):
			session["USER_DATA"][0]["office"] = "NPCO"
			_filter = "WHERE 1 "
		else:
			session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
			_filter = "WHERE  input_by in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])

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
# if __name__ == "__main__":	
# 		app.run(debug=True)

