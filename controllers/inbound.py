import Configurations as c
import os, random, json
import pandas as pd
import openpyxl
from datetime import datetime
from urllib.parse import quote, unquote

class inbound(object):
	"""docstring for inbound"""
	def __init__(self, app,db,session):
		super(inbound, self).__init__()
		self.app = app
		self.db = db
		self.session = session
		
	def _test_(self):
		print(" * Testing Inbound | {}".format(self.app_))
		pass

	def push_notif(self,name,type_,content,action,args):
		USER_ID = self.session["USER_DATA"][0]["id"]
		content = quote(content)
		row_id = self.db.do('''
			INSERT INTO 
				`notifications`
				(`name`, `type`, `content`, `status`, `action`, `args`, `USER_ID`)
			VALUES
				('{}','{}','{}','unseen','{}','{}','{}')
		'''.format(name,type_,content,action,args,USER_ID))
		return str(row_id)

	def get_notif(self):
		USER_ID = self.session["USER_DATA"][0]["id"]
		notif = self.db.select("SELECT * FROM `notifications` WHERE `USER_ID`={} ORDER BY `status` DESC;".format(USER_ID))
		return notif

	def get_notif_unseen(self):
		USER_ID = self.session["USER_DATA"][0]["id"]
		notif = self.db.select("SELECT COUNT(`status`) as 'num_notif' FROM `notifications` WHERE `status`='unseen' AND USER_ID={};".format(USER_ID))
		return notif

	def set_notif_seen(self,notif_id):
		USER_ID = self.session["USER_DATA"][0]["id"]
		notif = self.db.do("UPDATE `notifications` SET `status`='seen' WHERE `id`={} AND `USER_ID`={};".format(notif_id,USER_ID))
		return str(notif)

	def web_safe_encode(self,strs):
		return str(quote(strs))

	def web_safe_decode(self,strs):
		return str(unquote(strs))

class data_cleaning:
	def __init__(self, app,db,session):
		super(data_cleaning, self).__init__()
		self.app = app
		self.db = db
		self.session = session
		
	def get_table_columns(self,table):
		print("===== Querying")

		ress = self.db.select("DESCRIBE `{}`;".format(table))
		print("===== LOOPING")

		for count in range(len(ress)-1):
			for ky in ress[count]:
				if(type(ress[count][ky])=="bytearray" or type(ress[count][ky])=="bytes"):
					ress[count][ky] = ress[count][ky].decode("utf-8")
				pass
		print(ress)
		print("===== Passing Data")

		return list(ress)

	def get_table_columns_value(self,col,table):
		FILTER_SUFFIX = Filter.position_data_filter(self)
		return self.db.select("SELECT `{}` as `key`, count({}) as `total` FROM {}  {} GROUP by {};".format(col,col,table,FILTER_SUFFIX,col))


class Filter:
	def position_data_filter(clss_):
		_filter = "WHERE 1 "
		JOB = clss_.session["USER_DATA"][0]["job"].lower()

		if(JOB in "admin" or JOB in "super admin"):
			clss_.session["USER_DATA"][0]["office"] = "NPCO"
			_filter = "WHERE 1 "
		else:
			clss_.session["USER_DATA"][0]["office"] = "Regional ({})".format(clss_.session["USER_DATA"][0]["rcu"])
			_filter = "WHERE  USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(clss_.session["USER_DATA"][0]["rcu"])

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