import Configurations as c
import requests
from flask import Flask, session, jsonify, request, redirect, Blueprint, make_response, render_template

# ======FOR_LIGIN_AUTH==============
# @c.login_auth_web()
from modules.Req_Brorn_util import authenication
_auth = authenication(request,redirect,session,"USER_DATA","/login")
c.login_auth_web = _auth.login_auth_web

from flask_cors import CORS,cross_origin
from flask_minify import Minify
from datetime import datetime, timedelta

from views.login import login
from views.home  import home
from views.webrep  import webrep
from views.feature_0  import feature_0
from views.feature_0  import feature_0_sub
from views.psalm  import bp_app as psalm
from views.doofen  import bp_app as doofen
from views.fund_tracker  import bp_app as fund_tracker
# from views.dcf  import bp_app as dcf
from views.dcfv2  import bp_app as dcfv2
from views.npco_act_tracker  import npco_track as npco_tracker
from v2_view.core import _backend_main as dash
from v2_view.core import _backend_micro as _micro

from views.fmi  import bp_app as fmi

from views._tests_  import bp_app as test

from modules.public_vars import public_vars
from controllers.inbound import inbound
from apis import api
import json
from jinja_templates import templates
from controllers import Logs

Logs.ACCESS_LOGS("_SYSTEM_"+__name__,"SYS_RESTART",{}, "TERMINAL","APACE_RESTART")

app = Flask(__name__)
c.FLASK_APP = app

app.config['JSON_SORT_KEYS'] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.secret_key=c.SECRET_KEY
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(login.app);
app.register_blueprint(home.app);
app.register_blueprint(api.app);
app.register_blueprint(feature_0.app);
app.register_blueprint(feature_0_sub.app);
app.register_blueprint(webrep.app);
app.register_blueprint(psalm.app);
app.register_blueprint(doofen.app);
app.register_blueprint(fund_tracker.app);
app.register_blueprint(npco_tracker.app);
# app.register_blueprint(dcf.app);
app.register_blueprint(dcfv2.app);
app.register_blueprint(fmi.app);
app.register_blueprint(test.app);

app.register_blueprint(dash.app);
app.register_blueprint(_micro.app);

templates(app).init()

@app.route("/")
def index():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	if(c.IS_ON_SERVER):
		# c.DB_CRED[3] = c.SERVER_DATABASE
		return redirect("https://dtirapid.ph/webrep")
	else:
		# c.DB_CRED[3] = c.LOCAL_DATABASE
		return redirect("http://{}:5000/webrep".format(c.IP_address))

@app.route("/test_server") #NOT FOR LOCAL USE
def test_server():#NOT FOR LOCAL USE
	if(c.IS_ON_SERVER):#NOT FOR LOCAL USE
		return redirect("http://18.138.151.175/webrep") #NOT FOR LOCAL USE
	else:#NOT FOR LOCAL USE
		return redirect("http://{}:5000/webrep".format(c.IP_address))#NOT FOR LOCAL USE


@app.route("/proxy",methods=['POST','GET']) #NOT FOR LOCAL USE
def proxy():#NOT FOR LOCAL USE
	print(request.headers)
	url = request.headers['X-Proxy-Url']
	print(f" == Proxy Url [{url}]")
	data = dict(request.get_json())
	print(" == data from proxy")
	print(data)
	print(" == send data from proxy")
	response = requests.post(url, data=data,headers = {'Content-type': 'application/json'})

	print(response.status_code)
	print(response.content)

	print(" == Returning")
	return response.content

@app.before_request
def before_request():
	# print("databse = "+c.DB_CRED[3])
	# ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
	pass


# 	return redirect("/we_will_be_back_later")
@app.after_request
def after_request_func(response):
	ip_addr = request.access_route[0]
	agent = request.headers.get('User-Agent')
	agent = request.headers.get('User-Agent')
	referer = request.headers.get('referer')
	# ss = open("l_header.txt","a")
	# ss.write("{}\n".format(json.dumps((request))))
	# ss.close()
	if( request.endpoint != "static" and "get_notif_unseen" not in str(request.endpoint).split(".")):
		if(request.endpoint != "index"):
			Logs.ACCESS_LOGS(ip_addr, request.endpoint, session, agent, referer)
			# updated_mac = get_mac_address(ip=ip_addr)
			# print(" MAC ADDRESS")
			# print(updated_mac)
			# print(request.headers)
	# if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	# print(response.get_json())
	# ===============================
	response.headers.set('Strict-Transport-Security', "max-age=31536000 ")
	# response.headers.set('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'")
	response.headers.set('X-Frame-Options', "SAMEORIGIN")
	response.headers.set('X-Content-Type-Options', "nosniff")
	# response.headers.set('Referrer-Policy', "same-origin'")
	response.headers.set('Permissions-Policy', "geolocation=(self 'none'), camera=(), microphone=()")
	return response



# Minify(app=app, html=True, js=True, cssless=True)
# SECRET RECIPEE COCKTAIL
# - Dutchmil strawberry:
# - Zafiro Premium GIN
# - COLD- 

# BE YOURSELF, TRUST UR GUTS 


