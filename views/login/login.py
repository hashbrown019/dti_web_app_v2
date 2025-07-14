from datetime import date, datetime
import hashlib
import time
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json
from captcha.image import ImageCaptcha
import random, string, re

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

	@staticmethod
	def verify_hash_token(user_agent, timestamp, received_hash, allowed_delay=180):
		print("User Agent:", user_agent)
		print("Timestamp:", timestamp)
		print("Received Hash:", received_hash)

		try:
			timestamp = int(timestamp)
			now = int(time.time() * 1000)
			if now - timestamp > allowed_delay * 1000:
				print("Form expired. Please refresh and try again.")
				return False, "Form expired. Please refresh and try again."

			expected_input = f"{user_agent}|{timestamp}"
			expected_hash = hashlib.sha256(expected_input.encode('utf-8')).hexdigest()
			print("Expected Hash:", expected_hash)

			if expected_hash != received_hash:
				print("Invalid hash token.")
				return False, "Invalid hash token."

			return True, ""
		except Exception as e:
			print("Error:", str(e))
			return False, "Hash verification failed."

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

	@app.route('/captcha')
	def generate_captcha():
		# Generate random text
		captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
		
		# Store the text in session
		session['captcha_text'] = captcha_text

		# Generate CAPTCHA image
		image = ImageCaptcha()
		data = image.generate(captcha_text)
		return send_file(data, mimetype='image/png')

	@app.route("/login_auth", methods=["POST"])
	def login_auth():
		# Verify CAPTCHA
		user_input = request.form.get('captcha_input', '').strip().upper()
		captcha_session = session.get('captcha_text', '')

		if user_input != captcha_session:
			session['captcha_text'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
			return jsonify({"success": False,
				"message": "CAPTCHA is incorrect. Please try again."
			})

		# If CAPTCHA is valid, proceed with hash token verification
		user_agent = request.form.get('user_agent', '')
		timestamp = request.form.get('timestamp', '')
		received_hash = request.form.get('hash_token', '')

		if not user_agent or not timestamp or not received_hash:
			return jsonify({"success": False,
				"message": "Invalid request data."
			})

		valid_token, token_error = _main.verify_hash_token(user_agent, timestamp, received_hash)
		if not valid_token:
			return {"error": token_error}

		# Extract and sanitize login credentials
		username = request.form.get('user_name', '').strip()
		password = request.form.get('password', '').strip()

		# Define validation rules
		validation_rules = {
			'username': {
				'pattern': r'^[a-zA-Z0-9_]{3,20}$',
				'description': 'Username can only contain letters, numbers, and underscores (3-20 characters)'
			},
			'password': {
				'pattern': r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]{5,100}$',
				'description': 'Password must be 5-100 characters long and contain only allowed special characters'
			}
		}

		# Validate username and password
		for field, rule in validation_rules.items():
			value = locals()[field]
			if not re.match(rule['pattern'], value):
				return jsonify({
					"success": False,
					"message": f"Invalid {field}: {rule['description']}"
				})

		# Use parameterized query to prevent SQL injection
		sql = "SELECT * FROM `users` WHERE `username` = %s AND `password` = %s"
		log_res = rapid_mysql.select(sql, [username, password])

		if len(log_res) == 0:
			# Optional: reset CAPTCHA to prevent reuse
			session['captcha_text'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
			return jsonify({
				"success": False,
				"message": "Invalid credentials.",
				"url": "/login"
			})

		user = log_res[0]

		# Determine admin/privilege type
		admin_type = f"_{user['job'].upper().replace(' ', '_')}" if user['job'] in ['Admin', 'Super Admin'] else ""
		if user['pcu'] == 'none':
			priv_type = f"{user['rcu']}CO{admin_type}" if user['rcu'] != 'NPCO' else f"NPCO{admin_type}"
		else:
			priv_type = f"PCU{admin_type}"

		# Store in session
		session["USER_DATA_ADMIN_"] = log_res
		user['password'] = "********"
		user["PRIV_TYPE"] = priv_type
		session["USER_DATA"] = log_res

		# Attach security group info
		try:
			sg = rapid_mysql.select("SELECT * FROM `mis_2023`.`_securitygroup` WHERE `id` = %s", [user['security_group']])[0]
			session['USER_DATA'][0]['sg_info'] = sg
		except Exception as e:
			# If no role/security group found
			return jsonify({
				"success": True,
				"url": "/warning?type=user-no-role",
				"user": session["USER_DATA"]
			})

		# Success login
		return jsonify({
			"success": True,
			"url": "/mis-v4/core-main",
			"user": session["USER_DATA"]
		})
	
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



	