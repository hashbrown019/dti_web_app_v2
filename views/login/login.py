from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json

app = Blueprint("login",__name__,template_folder='pages')

# rapid = mysql(c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE)
# rapid= sqlite("assets\\db\\dti_rapidxi.db")
# rapid= sqlite(c.SQLITE_DB)

rapid_mysql = mysql(*c.DB_CRED)

class _main:
	def __init__(self, arg):
		super(_main, self).__init__()
		self.arg = arg

	def is_on_session(): return ('USER_DATA' in session)

	@app.route("/logintest",methods=["POST","GET"])
	def logintest():
		return render_template("loginv4.html")

	@app.route("/login",methods=["POST","GET"])
	def login():
		_attemp =""
		if("urlvisit" in request.args):
			_attemp = "&urlvisit="+request.args['urlvisit']
		# return render_template("SITE_OFF.html") # MAINTENANCE
		if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
		return redirect("/login_v2023?ver=dti_rapidgrowth_"+c.DB_CRED[3]+_attemp)

	@app.route("/login_dev_test",methods=["POST","GET"])
	@app.route("/dev_test",methods=["POST","GET"])
	def login_dev_test():
		return render_template("login.html")

	@app.route("/login_v2023",methods=["POST","GET"])
	def login_v2023():
		# return render_template("SITE_OFF.html") # MAINTENANCE
		# return render_template("login_v2.html")
		if(_main.is_on_session()):
			return redirect("/mis-v4/core-main")
		else:
			return _main.nlog()

	@app.route("/newlogin",methods=["POST","GET"])
	def newlogin():
		# return render_template("SITE_OFF.html") # MAINTENANCE
		return render_template("login.html")

	@app.route("/nlog",methods=["POST","GET"])
	def nlog():
		return render_template("loginv4.html",DB_STAT=c.DB_CRED[3])
		# return render_template("SITE_OFF.html") # MAINTENANCE
		# return render_template("loginv3.html",DB_STAT=c.DB_CRED[3])
		# return render_template("loginv2.html",DB_STAT=c.DB_CRED[3])

	@app.route("/login_auth",methods=["POST"])
	def login_auth():
		username = request.form['user_name']
		password = request.form['password']
		log_res = rapid_mysql.select("SELECT * from `users` WHERE `username` = '{}' AND `password`='{}';".format(username,password))
		admin_type = "";
		priv_type = "";
		if(len(log_res)!=0):
			if(log_res[0]['job'] in ['Admin','Super Admin']):
				admin_type = "_{}".format(log_res[0]['job'].upper().replace(" ","_"))
			if(log_res[0]['pcu']=='none'):
				if(log_res[0]['rcu']=='NPCO'):
					priv_type = "NPCO{}".format(admin_type)
				else:
					priv_type = "RCU{}".format(admin_type)
			else:
				priv_type = "PCU{}".format(admin_type)
				
			session["USER_DATA_ADMIN_"] = log_res
			log_res[0]['password'] = "********";
			log_res[0]["PRIV_TYPE"] = priv_type
			session["USER_DATA"] = log_res
			sg = rapid_mysql.select("SELECT * FROM `mis_2023`.`_securitygroup` WHERE `id`={};".format(log_res[0]['security_group']))[0]
			session['USER_DATA'][0]['sg_info'] = sg 
			if(log_res[0]['security_group']==0):
				return jsonify({"success":True,"url":"/warning?type=user-no-role","user":session["USER_DATA"]});
			else:
				return jsonify({"success":True,"url":"/mis-v4/core-main","user":session["USER_DATA"]});
		else:
			return jsonify({"success":False,"url":"/mis-v4/core-main"});

	@app.route("/logout")
	def logout():
		session.clear()
		if 'urlvisit' in request.args:
			return redirect("/login_v2023?ver=dti_rapidgrowth_mis_2023&urlvisit="+request.args['urlvisit'])
		return redirect("/webrep")
		# return jsonify(session )

	@app.route("/get_session")
	def get_session():
		return jsonify(session )

	@app.route("/check_username",methods=["POST"])
	def check_username():
		res = {"success":False,"data":"none"}
		username = request.form['user_name']
		log_res = rapid_mysql.select("SELECT * from `users` WHERE `username` = '{}';".format(username))
		if(len(log_res)!=0):
			res["success"] = True
			res["data"] = log_res[0]['name']
			res["profilepic"] = log_res[0]['profilepic']
			res["job"] = log_res[0]['job']
			
			return jsonify(res);
		else:
			return jsonify(res);
		

	@app.route("/login/check_pass",methods=["POST","GET"])
	def check_pass_all():
		sql = "SELECT * FROM `users` WHERE `username`='{}' AND `password`='{}' ;".format(session["USER_DATA_ADMIN_"][0]["username"],request.form["pass"])
		resp = len(rapid_mysql.select(sql))
		status = "success" if(resp != 0) else "failed"
		if("action" in request.form):action = request.form['action']
		else: action = "none"

		return {"status":status,"action":action}


	@app.route("/login/download_file/<file_>",methods=["POST","GET"])
	def download_file(file_):
		# today = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
		# def_name = "{}_{}".format(today,file_)
		def_name = file_
		return send_file(c.RECORDS+"/downloadables/"+file_, as_attachment=True,download_name=def_name)



	