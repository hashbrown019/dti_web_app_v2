from ast import pattern
import random
import string
from modules.Connections import mysql,sqlite
import Configurations as c
from flask import jsonify, request, session, send_file, redirect
from modules.Req_Brorn_util import file_from_request
from werkzeug.datastructures import MultiDict 
import json, os
import re
import hashlib, time
import re
# from v2_view.core import _socketIO

rapid_mysql = mysql(*c.DB_CRED)
FILE_REQ = file_from_request(c.FLASK_APP)

# ================================================
# ================================================
# ================================================
# ==============USER-PROFILE======================
class user_pofile:
	"""docstring for user_pofile"""
	def __init__(self):
		super(user_pofile, self).__init__()

	@staticmethod
	def validate_input(field_name, field_value):

		field_value = field_value.strip()

		if not field_value:
			return False, "", f"{field_name} cannot be empty"

		validation_rules = {
			'name': {
				'pattern': r'^[a-zA-Z0-9\s\-\.]{2,50}$',
				'description': 'Name can only contain letters, numbers, spaces, hyphens, and dots (2-50 characters)'
			},
			'username': {
				'pattern': r'^[a-zA-Z0-9_]{3,20}$',
				'description': 'Username can only contain letters, numbers, and underscores (3-20 characters)'
			},
			'email': {
				'pattern': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
				'description': 'Please enter a valid email address (e.g., name@domain.com)'
			},
			'password': {
				'pattern': r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]{5,100}$',
				'description': 'Password must be 5-100 characters long and contain only allowed special characters'
			},
			'phone': {
				'pattern': r'^[0-9+\-\s()]{10,15}$',
				'description': 'Phone number can only contain digits, +, -, spaces, and parentheses (10-15 characters)'
			},
			'mobile': {
				'pattern': r'^[0-9+\-\s()]{10,15}$',
				'description': 'Mobile number can only contain digits, +, -, spaces, and parentheses (10-15 characters)'
			},
			'address': {
				'pattern': r'^[a-zA-Z0-9\s\-\.,#]{5,200}$',
				'description': 'Address can contain letters, numbers, spaces, hyphens, dots, commas, and # (5-200 characters)'
			},
			'job': {
				'pattern': r'^[a-zA-Z0-9\s&\-\.]{2,50}$',
				'description': 'Job title can contain letters, numbers, spaces, hyphens, dots, and ampersands (2-50 characters)'
			},
			'pcu': {
				'pattern': r'^[a-zA-Z0-9\s\-\.]{2,50}$',
				'description': 'PCU can only contain letters, numbers, spaces, hyphens, and dots (2-50 characters)'
			},
			'rcu': {
				'pattern': r'^[a-zA-Z0-9\s\-\.]{2,50}$',
				'description': 'RCU can only contain letters, numbers, spaces, hyphens, and dots (2-50 characters)'
			}
		}
		print(f"Validating {field_name}: {field_value}")

		# Dangerous pattern check
		dangerous_patterns = [
			r'https?:\/\/',                                   # Block http://, https://
			r'ftp:\/\/',                                      # Block ftp links
			r'(\/|\\){2,}',                                   # Block repeated slashes
			r'\.\.',                                          # Block path traversal
			r'\b(select|insert|update|delete|drop|create|alter|union)\b',  # SQL keywords
			r'\b(exec|eval|system|shell)\b',                  # Code execution
			r'\b(script|javascript|vbscript)\b',              # Script injection
			r'\.(php|asp|aspx|jsp|exe|sh|bat|cmd)\b',         # Dangerous file extensions
			r'[<>]', r'[{}]', r'[\[\]]',                      # Code-related brackets
			r'[|&;`]',                                        # Shell/meta characters
			r'[\r\n]',                                        # Email header injection attempt
		]

		safe_fields_allowing_amp = {'job'}  # You can expand this as needed

		for pattern in dangerous_patterns:
			if pattern == r'[|&;`]':
				if field_name in safe_fields_allowing_amp:
					continue  # Allow these characters in safe fields
			if re.search(pattern, field_value, re.IGNORECASE):
				return False, "", f"{field_name} contains invalid or dangerous input (matched: {pattern})"

		# Apply field-specific validation
		if field_name in validation_rules:
			rule = validation_rules[field_name]
			if not re.match(rule['pattern'], field_value):
				return False, "", f"{field_name}: {rule['description']}"

		# Fallback length safety
		if len(field_value) > 200:
			return False, "", f"{field_name} is too long (maximum 200 characters)"

		return True, field_value, ""
	
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

	def user_registration_submit(req):
		try:
			data = dict(req.form)
			
			# Verify CAPTCHA first
			user_input = request.form.get('captcha_input', '').strip().upper()
			captcha_session = session.get('captcha_text', '')

			if user_input != captcha_session:
				session['captcha_text'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
				return {"error": "CAPTCHA is incorrect. Please try again."}

			# If CAPTCHA is valid, proceed with hash token verification
			user_agent = req.form.get('user_agent', '')
			timestamp = req.form.get('timestamp', '')
			received_hash = req.form.get('hash_token', '')
			valid_token, token_error = user_pofile.verify_hash_token(user_agent, timestamp, received_hash)
			if not valid_token:
				return {"error": token_error}

			# Validate required fields
			required_fields = {'name', 'email', 'password', 'username'}
			allowed_fields = {'name', 'email', 'password', 'phone', 'address', 'job', 'username', 'pcu', 'rcu', 'mobile'}
			
			missing_fields = required_fields - set(data.keys())
			if missing_fields:
				return jsonify({"success": False, "message": f"Missing required fields: {', '.join(missing_fields)}"}), 400
			
			# Validate each field
			validated_data = {}
			for field_name, field_value in data.items():
				if field_name not in allowed_fields:
					continue
					
				is_valid, cleaned_value, error_message = user_pofile.validate_input(field_name, field_value)
				
				if not is_valid:
					print(f"Invalid input for {field_name}: {field_value}")
					return jsonify({"success": False, "message": error_message}), 400
				
				validated_data[field_name] = cleaned_value
			
			# Check for existing email/username
			existing_email = rapid_mysql.select(
				f"SELECT id FROM `users` WHERE `email` = '{validated_data['email']}'"
			)

			if existing_email:
				print(f"Email already exists: {validated_data['email']}")
				return jsonify({"success": False, "message": "Email already registered"}), 400

			# Check for existing username
			existing_username = rapid_mysql.select(
				f"SELECT id FROM `users` WHERE `username` = '{validated_data['username']}'"
			)

			if existing_username:
				print(f"Username already exists: {validated_data['username']}")
				return jsonify({"success": False, "message": "Username already taken"}), 400
						
			# Build and execute SQL
			columns = []
			placeholders = []
			values = []
			
			for field_name, field_value in validated_data.items():
				columns.append(f"`{field_name}`")
				placeholders.append("%s")
				values.append(field_value)
			
			columns.append("`status`")
			placeholders.append("%s")
			values.append("pending")
			
			sql = f"INSERT INTO `users` ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
			
			try:
				result = rapid_mysql.do(sql, values)
				return jsonify({
					"success": True, 
					"message": "Registration successful!",
					"location": "/login"  # Use Location header for redirect
				}), 302
			except Exception as e:
				print(f"Database error: {str(e)}")
				return jsonify({"success": False, "message": "Registration failed. Please try again."}), 500

		except Exception as e:
			print(f"Unexpected error: {str(e)}")
			return jsonify({"success": False, "message": "An unexpected error occurred"}), 500

	def edit_user_profile(req):
		data = dict(req.form)
		key = [];val = [];args=""

		is_exist = len(rapid_mysql.select("SELECT * FROM `users` WHERE `id` ='{}' ;".format(req.form['id'])))
		
		# Define allowed fields for update (excluding sensitive fields)
		allowed_fields = {'name', 'phone', 'address', 'job', 'pcu', 'rcu', 'mobile','email', 'username', 'security_group', 'status', 'id'}

		# Validate each field
		validated_data = {}
		for field_name, field_value in data.items():
			if field_name not in allowed_fields:
				continue  # Skip unknown fields

			# Validate the field
			is_valid, cleaned_value, error_message = user_pofile.validate_input(field_name, field_value)

			if not is_valid:
				return {"error": error_message}

			validated_data[field_name] = cleaned_value

		print("validated_data:", validated_data)

		if not validated_data:
			return {"error": "No valid fields to update"}

		if(is_exist==0):
			for datum in validated_data:
				if datum != 'id': 
					key.append("`{}`".format(datum))
					val.append("'{}'".format(validated_data[datum]))
			sql = ('''INSERT INTO `users` ({},`password`) VALUES ({},'dtirapid');'''.format(", ".join(key),", ".join(val)))
			# sql = ('''INSERT INTO `users` ({},`status`) VALUES ({},'pending');'''.format(", ".join(key),", ".join(val)))
		else:
			for datum in validated_data:
				if datum != 'id':
					args += ",`{}`='{}'".format(datum,validated_data[datum])
			sql = "UPDATE `users` SET  {}  WHERE `id`='{}';".format(args[1:],req.form['id'])

		print("SQL query:", sql)

		last_row_id = rapid_mysql.do(sql)
		return last_row_id

	def edit_user_profilepic(req):
		__f = FILE_REQ.save_file_from_request(req, "profilepic", c.RECORDS + "/objects/userpics/", False, True)
		profilepic = __f["file_arr_str"]
		user_id = req.form.get('id')
		if not user_id:
			return {"error": "User ID is required"}
		sql = f"UPDATE `users` SET `profilepic` = '{profilepic}' WHERE `id` = '{user_id}'"
		rapid_mysql.do(sql)
		return __f

	def edit_user_profilepass(req):
		new_password = req.form.get('password')
		user_id = req.form.get('id')
		current_pass = req.form.get('current_pass')
		if not all([new_password, user_id, current_pass]):
			return {"error": "Missing required fields"}
		sql = f"""UPDATE `users` SET `password` = '{new_password}' WHERE `id` = '{user_id}' AND `password` = '{current_pass}'"""
		result = rapid_mysql.do(sql)
		if isinstance(result, dict) and 'error' in result:
			return {"error": "Failed to update password"}
		return {"success": True}
# ================================================
# ================================================
# ================================================
# ================================================
class system_settings:
	def add_user_group(req):
		data = req.form
		key = [];val = [];args=""
		for datum in data:
			# print(datum)
			_VAL = data[datum]
			if _VAL.lower() in ["true","false"]: _VAL =  _VAL.lower() in ["true"] 
			else: _VAL = f"'{_VAL}'"

			key.append("`{}`".format(datum))
			val.append("{}".format(_VAL) )

		sql = ('''INSERT INTO `_securitygroup` ({}) VALUES ({});'''.format(", ".join(key),", ".join(val)))
		print(rapid_mysql.do(sql))
		return ""

	def get_staff_info(req):
		return rapid_mysql.select("SELECT * FROM `users` WHERE `id`={}".format(req.form['id']) )[0]
		
	def get_user():
		pass

# ================================================
# ================================================
# ================================================
# ================================================

class file_manager:
	def add_modify_folder(req):
		for ids in req.form:
			print(f"{ids} : {req.form[ids]}")
		sql_ress = rapid_mysql.insert_or_add_to_db(req,"file_manager_folders","id")
		print(sql_ress)
		return sql_ress

	def add_file(req):
		_files = json.loads(f"[{req.form['files_arr']}]")
		sql_res = []
		for _f in _files:
			__req = AttrDict({'form':_f})
			print(__req.form)
			sql_ress = rapid_mysql.insert_or_add_to_db(__req,"file_manager_files","id")
			sql_res.append(sql_ress)
		res = FILE_REQ.save_file_from_request(
			req,
			"fileInput",
			pathtosave=c.RECORDS+"objects/mis_drive",
			raise_error=True,
			timestamp=False,
			custom_name="")
		return {"sql_note":sql_res, "file_handling_msg":res}

	def modify_file(req):
		sql_ress = rapid_mysql.insert_or_add_to_db(req,"file_manager_files","id")
		return {"sql_note":sql_ress}


	def get_file(req):
		file = req.args['file']
		print(file)
		return send_file(c.RECORDS+"/objects/mis_drive/_"+file.replace(' ','_'))
		# img = img.replace('C:fakepath', '').replace(" ","_").replace(")","").replace("(","")

# ================================================
# ================================================

class file_handling:
	def download_db_pfa(req,obj):
		_sql = "SELECT * FROM `{}` WHERE {} ;".format(obj,where_rcu_is(req.args['rcu']))
		print(_sql)
		ls_arr = rapid_mysql.select(_sql)
		return ls_arr

# ================================================
# ================================================
class AttrDict(dict):
	def __init__(self, *args, **kwargs):
		super(AttrDict, self).__init__(*args, **kwargs)
		self.__dict__ = self
# ================================================
# ================================================
# ================================================
# ================================================

class fmi_tracker:
	def update_add(req):
		return rapid_mysql.insert_or_add_to_db(req,"fmi_basic_info","id")

# ================================================
# ================================================
# ================================================
# ================================================

class personal_forms:
	def save_template(req):
		datas = dict(req.form)
		# temp_src = c.RECORDS + "objects/save_templates/"+req.form['form_code']+".html"
		temp_src = c.RECORDS + "../v2_view/core/pages/chunks/__templates__/"+req.form['form_code']+".html"
		temps = open(temp_src,"w")
		temps.write(datas['form_design'].replace("~",'"'))
		temps.close()
		del datas['form_design']
		key = [];val = [];args=""
		for datum in datas:
			_VAL = datas[datum]
			key.append("`{}`".format(datum))
			val.append("'{}'".format(_VAL) )

		sql = ('''INSERT INTO `_form_templates` ({}) VALUES ({});'''.format(", ".join(key),", ".join(val)))
		print(rapid_mysql.do(sql))
		return datas

	def save_data(req):
		datas = dict(req.form)
		datas['__data'] = {}; key_to_rem=[];
		for datum in datas:
			if("__" not in datum):
				datas['__data'][datum] = datas[datum]
				key_to_rem.append(datum)
		for key in key_to_rem: datas.pop(key,None)
		datas['__data']  = json.dumps(datas['__data'] )
		key = [];val = [];args=""
		for datum in datas:
			_VAL = datas[datum]
			key.append("`{}`".format(datum))
			val.append("'{}'".format(_VAL) )
		sql = ('''INSERT INTO `_form_templates_data` ({}) VALUES ({});'''.format(", ".join(key),", ".join(val)))
		print(sql)
		print(rapid_mysql.do(sql))
		return datas

	def get_template(req):
		temp_src = c.RECORDS + "../v2_view/core/pages/chunks/__templates__/"+req.form['form_code']+".html"
		temps = open(temp_src,"r",)
		html = temps.read()
		temps.close()
		return "--"
		# return html.encode('cp1252')

	def save_dip_rep(req):
		excel_ = req.files
		UPLOAD_NAME = "{}_DIP_TRACKER.xlsx".format(session["USER_DATA"][0]["id"])
		__f = FILE_REQ.save_file_from_request(req,"demoA",c.RECORDS+"/objects/spreadsheets_dcf",False,False,UPLOAD_NAME)

		return redirect("/mis-v4/core-tools-trackers-specific?panel&m=mg")

# ================================================
# ================================================
# ================================================
# ================================================

def position_data_filter():
	_filter = " 1 "
	JOB = session["USER_DATA"][0]["job"].lower()
	print(session["USER_DATA"][0]['sg_info']['user_group'])
	if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = " 1 ";
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = " USER_ID in ( SELECT id from users WHERE rcu = '{}' )".format(session["USER_DATA"][0]["rcu"])
	return _filter

def __position_data_filter():
	_filter = " 1 "
	JOB = session["USER_DATA"][0]["job"].lower()
	print(session["USER_DATA"][0]['sg_info']['user_group'])
	if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = " 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = " USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
	return _filter

def where_rcu_is(_rcu):
	return " USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(_rcu)

