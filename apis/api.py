import Configurations as c
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
from modules.Utility import obj_handling as objh
import os, json
from controllers.engine_block_to_sql import form_migration
from controllers.engine_excel_to_sql import form_excel_a_handler

app = Blueprint("api",__name__)

form_mig_block = form_migration(__name__)
form_mig_excel = form_excel_a_handler(__name__)


class data_handlers:
	def is_on_session(): return ('USER_DATA' in session)

	def __init__(self, arg):super(data_handlers, self).__init__();self.arg = arg


	# ==========================================================
	@app.route("/api/block_sql/all",methods=["POST","GET"]) # GE
	def block_sql():
		return form_mig_block.get_all()


	@app.route("/api/excel_sql/all",methods=["POST","GET"]) # GE
	def excel_sql():
		content = form_mig_excel.get_all_uploaded_excel_data_f_a()
		return "Done"
		# return objh.txt_file_dl("skkrt.sql",content)
		# return objh.obj_file_dl("skkrt.objdmp",content)
