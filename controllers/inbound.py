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
