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

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)
# rapid= sqlite("assets\\db\\dti_rapidxi.db")
# rapid= sqlite(c.SQLITE_DB)

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
