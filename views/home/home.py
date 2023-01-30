from flask import Blueprint, render_template, request, session, redirect, jsonify
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json
from controllers.file_handler import file_handler, form_a1_handler, form_a2_handler, form_a3_handler, form_a4_handler, form_a5_handler, form_a6_handler

app = Blueprint("home",__name__,template_folder='pages')

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)
rapid= sqlite("assets\\db\\dti_rapidxi.db")


form_a1 = form_a1_handler(__name__)
form_a2 = form_a2_handler(__name__)
form_a3 = form_a3_handler(__name__)
form_a4 = form_a4_handler(__name__)
form_a5 = form_a5_handler(__name__)
form_a6 = form_a6_handler(__name__)

class _main:
	def is_on_session(): return ('USER_DATA' in session)

	def __init__(self, arg):super(_main, self).__init__();self.arg = arg


	# ===========================V1===========================================================================

	@app.route("/home",methods=["POST","GET"])
	def home():
		return redirect("/homepage#1")


	@app.route("/homepage",methods=["POST","GET"])
	def homepage():
		# return render_template("SITE_OFF.html") # MAINTENANCE
		if(_main.is_on_session()):
			return render_template("home/home.html",USER_DATA = session["USER_DATA"][0])
		else:
			return redirect("/login?force_url=1")


	# ==========================V2===========================================================================

	@app.route("/home_v2",methods=["POST","GET"])
	def home_v2():
		return redirect("/homepage_v2#1")


	@app.route("/homepage_v2",methods=["POST","GET"])
	def homepage_v2():
		# return render_template("SITE_OFF.html") # MAINTENANCE
		if(_main.is_on_session()):
			return render_template("home_v2.html",USER_DATA = session["USER_DATA"][0])
		else:
			return redirect("/login?force_url=1")


	# =====================================================================================================



	@app.route("/get_sub_form_a_template",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_sub_form_a_template():
		page = request.form['subform_temp']
		return render_template("home/form_a/{}.html".format(page));
		# sample commit


	# =====================================================================================================post_harv_photo
	# =====================================================================================================farmer_img_base64
	# =====================================================================================================

	@app.route("/api/block_sql/a1",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_all_file_farmer_profile():
		return jsonify(form_a1.get_all_file_farmer_profile())

	@app.route("/api/block_sql/a2",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_all_file_farmer_farmland():
		return jsonify(form_a2.get_all_file_farmer_farmland())

	@app.route("/api/block_sql/a3",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_all_file_farmer_hh_profile():
		return jsonify(form_a3.get_all_file_farmer_hh_profile())

	@app.route("/api/block_sql/a4",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_all_file_farmer_prod_cost():
		return jsonify(form_a4.get_all_file_farmer_prod_cost())

	@app.route("/api/block_sql/a5",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_all_file_farmer_workers_laborers():
		return jsonify(form_a5.get_all_file_farmer_workers_laborers())

	@app.route("/api/block_sql/a6",methods=["POST","GET"]) # GETS the Fulll data of Farmer
	def get_all_file_farmer_post_harvest():
		return jsonify(form_a6.get_all_file_farmer_post_harvest())