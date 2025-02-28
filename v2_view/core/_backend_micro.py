from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json


from v2_view.core import dash_api
from v2_view.core import dash_script
from v2_view.core import _backend_sub


app = Blueprint("_micro",__name__,template_folder='pages')
rapid_mysql = mysql(*c.DB_CRED)

class _main:
	def __init__(self, arg):
		super(_main, self).__init__()
		self.arg = arg

	@app.route("/mis-v4-micro/test",methods=["POST","GET"])
	@c.login_auth_web()
	def micro_index():
		return {"status":"test auth","session":session["USER_DATA"][0]}

	@app.route("/micro_test",methods=["GET"])
	def micro_test():
		return {"status":"test no auth"}

	@app.route("/tracker-dip-main-content", methods=["GET"])
	def tracker_dip_main_content():
		return render_template("tracker-dip-main-content.html")

	@app.route("/view-tracker-dip-main-content")
	def view_tracker_dip_main_content():
		dipData = rapid_mysql.select("SELECT * FROM dcf_prep_review_aprv_status")
		return jsonify(dipData)
	
	@app.route("/micro/tabl-get-data", methods=["GET","POST"])
	def core_tracker_sales():
		ids = request.form['id']
		tbl = request.form['tbl']
		cpa = rapid_mysql.select(f"SELECT * FROM `{tbl}` WHERE `id`={ids};")
		return jsonify(cpa)

	@app.route("/micro/get_formB_data", methods=["GET","POST"])
	def get_formB_data():
		condition = request.form['condition']
		formBData = rapid_mysql.select(f"SELECT * FROM `form_b` {condition};")
		return jsonify(formBData)
	
	@app.route("/micro/insert_sales_tracker", methods=["POST"])
	def insert_sales_tracker():
		try:
			field_mapping = {
				"nameID": "ST_id",
				"nameRCU": "ST_rcu",
				"namePCU": "ST_pcu",
				"nameCOMMODITY": "ST_commodity",
				"nameDIP": "ST_nameofdip",
				"nameFO": "ST_nameof_fo",
				"af-msme": "ST_af_msme",
				"addressFO": "ST_address_fo",
				"productType": "ST_product_type",
				"vs": "ST_vol_supplied",
				"aveP": "ST_ave_price",
				"totalTransaction": "ST_total_transaction",
				"incentives": "ST_incentives_provided"
			}
			columns = []
			values = []
			for form_field, db_column in field_mapping.items():
				if form_field in request.form:
					columns.append(f"`{db_column}`")
					values.append(f"'{request.form[form_field]}'")
			if not columns:
				return jsonify({"status": "error", "message": "No valid data provided"}), 400
			query = f"INSERT INTO `sales_tracker` ({', '.join(columns)}) VALUES ({', '.join(values)})"
			res = rapid_mysql.do(query)  
			return jsonify({"status": "success", "message": "Data inserted successfully", "result": res})
		except Exception as e:
			return jsonify({"status": "error", "message": str(e)}), 500


	@app.route("/sales-tracker-table", methods=["GET"])
	def sales_tracker_table():
		return render_template("sales-tracker-table.html")

	@app.route("/view-sales-tracker-table", methods=["GET","POST"])
	def view_sales_tracker_table():
		stData = rapid_mysql.select("SELECT * FROM sales_tracker")
		return jsonify(stData)