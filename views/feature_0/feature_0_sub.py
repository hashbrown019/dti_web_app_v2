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