import os, json, random, shutil
from tqdm import tqdm
import Configurations as c
from modules.Connections import mysql,sqlite
from controllers.value_cleaner import file_handler as cleaner

import base64
import sys
import pandas as pd
from tqdm import tqdm
import warnings
import csv
import xlrd ####### IMPORTANT pip install xlrd==1.2.0

warnings.filterwarnings('ignore')

rapid_sqlite = sqlite(c.SQLITE_DB)
rapid_mysql = mysql(*c.DB_CRED)
# rapid_mysql.err_page = 0


class form_excel_a_handler:
	def __init__(self,args):
		super(form_excel_a_handler, self).__init__()
		self.args = args

	def get_all_uploaded_excel_data_f_a(self):
		return self.excel_popu_a()

	def excel_popu_a(self):
		dir_path = c.RECORDS+"/objects/spreadsheets/queued/"
		FROM_EXCEL_RPOFILES = {}
		# FROM_EXCEL_RPOFILES = []
		loads_ = tqdm(os.listdir(dir_path))
		counter = 0
		for path in loads_:
			PATH__ = os.path.join(dir_path, path)
			loads_.desc = path
			if os.path.isfile(PATH__):
				if PATH__.find("._DELETED_FILE_")<0:	
					file_name =  PATH__ 
					sheet =  "VC FORM A" 
					try:
						resp = self.push_mysql(self.readRows(file_name, sheet),path)
						if(resp["err"]):
							return resp["msg"]
							# return resp["msg"]["sql"]
						counter = counter + 1
					except Exception as e:
						if("No sheet named <'VC FORM A'>" in str(e)):
							print("\nERROR in XLRD Parser (ignoring file [{}]) || {}".format(path,e))
						else:
							raise e
			# if(counter >= 3):
			# 	break
		return FROM_EXCEL_RPOFILES


	def push_mysql(self, rows, user_id):
		excel_a_heads = get_all_uploaded_excel_data_heads()
		err = False
		RESP = ""
		CONN = rapid_mysql.db_ready() 

		for row_num in range(len(rows)):
			counter = 0
			# print(rows)
			fields = "" ; vals = ""
			for val__ in rows[row_num]:
				fields = fields + ",\n`"+ excel_a_heads[counter] +"`"
				vals = vals + ',\n"'+ str(val__).replace("\\"," ").replace("'"," ").replace('''"'''," ") +'"'
				counter = counter + 1
			sql = ('''INSERT INTO `excel_import_form_a` (`user_id`,{}) VALUES('{}',{}) ;'''.format(fields[1:],user_id,vals[1:]))
			resp = rapid_mysql.do_(sql,CONN)
			try:
				if("response" in resp):
					err = True;RESP = resp;break
			except Exception as e: print( str(e))
		resp.commit()
		return {"err":err,"msg":RESP}

	def readRows(self, file, s_index):
		wb = xlrd.open_workbook(file)  
		# sheet = wb.sheet_by_index(s_index)
		sheet = wb.sheet_by_name(s_index)
		data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
		counter = 0
		return data[3:]

# ======================

def get_all_uploaded_excel_data_heads():
	excel_f_a_heads = c.RECORDS+"/settings/db_sql_excel_form_a.head"
	reader = open(excel_f_a_heads,"r");excel_f_a_heads = json.loads(reader.read());reader.close()
	return excel_f_a_heads

	# ============================================================