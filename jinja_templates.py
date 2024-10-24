import Configurations as c 
from flask import render_template, render_template_string
from datetime import datetime, timedelta
from modules.Connections import mysql
db = mysql(*c.DB_CRED)

class templates:
	"""docstring for ClassName"""
	def __init__(self, app):
		super(templates, self).__init__()
		self.app = app

	def format_timestamp(timestamp):
		now = datetime.now()
		time_difference = now - timestamp
		if time_difference.total_seconds() < 1:
			return "Just now"
		elif time_difference.total_seconds() == 1:
			return "1 second ago"
		elif time_difference.total_seconds() < 60:
			return f"{int(time_difference.total_seconds())} seconds ago"
		elif time_difference.total_seconds() == 60:
			return "1 minute ago"
		elif time_difference.total_seconds() < 3600:
			minutes_ago = int(time_difference.total_seconds() / 60)
			return f"{minutes_ago} minute{'s' if minutes_ago != 1 else ''} ago"
		elif time_difference.total_seconds() == 3600:
			return "1 hour ago"
		elif time_difference.total_seconds() < 86400:
			hours_ago = int(time_difference.total_seconds() / 3600)
			return f"{hours_ago} hour{'s' if hours_ago != 1 else ''} ago"
		else:
			return timestamp.strftime("%Y-%m-%d %H:%M:%S")


	def cpa_status(form_2_recent_cpa,signed, exprd, renew,name):
		# form_2_recent_cpa
		cpa_note = ""
		now = datetime.now()
		status = "Draft"
		msg = "error"

		if(form_2_recent_cpa=="initial"):
			cpa_note = "Initial CPA"
		else:
			res= db.select(f"SELECT * FROM `dcf_implementing_unit` WHERE `id`= '{form_2_recent_cpa}' ;")

			if(len(res)==0):
				return {"status":"Old Version Format","note":"No Date Available (You may update the CPA while on draft)","cpa":"Draft || Initial CPA "}
			else:
				res= db.select(f"SELECT * FROM `dcf_implementing_unit` WHERE `id`= '{form_2_recent_cpa}' ;")[0]
				cpa_note = f"Renewal for RAPID_CPA_{res['id']} : {res['form_2_businessname']}"
			pass


		try:
			date_sign = datetime.strptime(str(signed), '%Y-%m-%d')
			date_exprd = datetime.strptime(str(exprd), '%Y-%m-%d')
			print(date_exprd)
			__date = str(date_exprd - now)
			d_diff = int(__date.split(" ")[0])-1
			msg = __date.split(",")[0]
			if d_diff <= 0:
				status = "Expired"
				msg = f"Expired on :{exprd} | {__date.split(',')[0].replace('-','')} ago"
			elif d_diff <=5:
				status = "To be expire"
				msg = f"{__date.split(',')[0].replace('-','')} left"
			else:
				status = "Active"
				msg = f"{__date.split(',')[0].replace('-','')} remaining"
			pass
		except Exception as e:
			msg = e
			print(f"{name}  === {e}")

		return {"status":status,"note":msg,"cpa":cpa_note}

	def websafe_filename(fname):
		return fname.replace("#","@@")

	def get_cpa(ids):
		res= db.select(f"SELECT * FROM `dcf_implementing_unit` WHERE `id`= '{ids}' ;")[0]
		cpa_note = f"RAPID_CPA_{res['id']} : {res['form_2_businessname']}"
		return cpa_note


	def trancuate_text(text, lngth, elipse="...", word_tranc = "(truncated)"):
		if(len(str(text))-5 < lngth):
			return text
		return f"{str(text)[:lngth]}{elipse}{word_tranc}"

	def get_save_template(file):
		temp_src = c.RECORDS + "objects/save_templates/"+file+".html"
		temps = open(temp_src,"r")
		HTML = temps.read()
		temps.close()
		return render_template_string(HTML)
	# ===========================================================================================================
	# ===========================================================================================================
	# ===========================================================================================================
	# ===========================================================================================================
	# ===========================================================================================================
	def add_jinja_temp(jinja_name, func):
		self.app.jinja_env.filters[jinja_name] = func

	def init(self):
		self.app.jinja_env.filters['format_timestamp'] = templates.format_timestamp
		self.app.jinja_env.filters['websafe_filename'] = templates.websafe_filename
		self.app.jinja_env.filters['cpa_status'] = templates.cpa_status
		self.app.jinja_env.filters['get_cpa'] = templates.get_cpa
		self.app.jinja_env.filters['trancuate_text'] = templates.trancuate_text
		self.app.jinja_env.filters['get_save_template'] = templates.get_save_template
	# Register the custom filter on the Flask application\

	#
	# Plans 
	# 	- Hire a IT (2)
	# 	- Train It in to Months
	#	- Discuss Pending MIS task
	#	- Prepare 2 month Turnover Plan

	# Things to Turn-over
	# 	- Rapid Properties
	# 	- Credentials
	# 		- Server Key
	# 		- Server access
	# 		- Server Permission
	# 	- Source Code
	# 		- Github Repositories
	# 		- Database Credentials
	# 		- Code Documentation
	#

