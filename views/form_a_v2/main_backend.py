from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json

from views.form_a_v2 import av2_api as a_v2_api


app = Blueprint("form_a_v2",__name__,template_folder='pages')

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)
# rapid= sqlite("assets\\db\\dti_rapidxi.db")
# rapid= sqlite(c.SQLITE_DB)

rapid_mysql = mysql(*c.DB_CRED)

class _main:
	def __init__(self, arg):
		super(_main, self).__init__()
		self.arg = arg

	def is_on_session(): return ('USER_DATA' in session)

	@app.route("/form_a_home",methods=["POST","GET"])
	@c.login_auth_web()
	def form_a_home_index():
		return render_template("a_v2_index.html",USER_DATA = session["USER_DATA"][0])

	@app.route("/form_a_home/<page>",methods=["POST","GET"])
	@c.login_auth_web()
	def form_a_home_page(page):
		return render_template(f"page_content/{page}.html",USER_DATA = session["USER_DATA"][0])

	@app.route("/hahaha")
	def sample():
		return a_v2_api.position_data_filter()