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

app = Blueprint("doofen",__name__,template_folder='pages')

_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)

outbound = outb(app,rapid_mysql,session)
inbound = inb(app,rapid_mysql,session)
data_clean = d_c(app,rapid_mysql,session)
# app = Flask(__name__)
	
@app.route("/formb")
def index():
	return redirect("/formb/dashboard")
	
@app.route("/formb/dashboard")
def dashboard():
	return render_template('index.html',USER_DATA=session["USER_DATA"][0])


@app.route("/formb/save_form",methods=["POST","GET"])
def save_form():
	form_data = request.form
	col = ""
	val = ""
	for data_ in form_data:
		col += ",`{}`".format(data_)
		val += ",'{}'".format(form_data[data_])

	sql = "INSERT INTO `form_b` (`uploaded_by`,{}) VALUES ('{}',{})".format(col[1:], session["USER_DATA"][0]["id"], val[1:])
	# print(sql)
	last_row_id = rapid_mysql.do(sql)
	return jsonify({"sql":sql})
	# return jsonify([last_row_id])



@app.route("/formb/get_list_fo",methods=["POST","GET"])
def get_list_fo():
	sql_form = '''
	SELECT 
		`id` as 'db_id',
		`organization_registered_name`,
		`office_business_adrress`,
		`types_of_organization`,
		`registering_agencies`
	FROM `form_b` {} ;'''.format(Filter.position_data_filter())
	resp = rapid_mysql.select(sql_form,False)
	return jsonify(resp)



@app.route("/formb/excel_upload",methods=["POST","GET"])
def excel_upload():

	return "---"


@app.route("/formb/get_ind_fo",methods=["POST","G ET"])
def get_ind_fo():
	ids = request.form['id']
	sql_form = "SELECT * FROM `form_b` WHERE `id`={};".format(ids)
	ind = rapid_mysql.select(sql_form)
	return jsonify(ind)

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

# if __name__ == "__main__":	
# 		app.run(debug=True)

