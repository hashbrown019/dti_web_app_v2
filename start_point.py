import Configurations as c

from flask import Flask, session, jsonify, request, redirect, Blueprint

# ======FOR_LIGIN_AUTH==============
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
from views.dcf  import bp_app as dcf
from views.fmi  import bp_app as fmi

from modules.public_vars import public_vars
from controllers.inbound import inbound
from apis import api
import json
from controllers import Logs

Logs.ACCESS_LOGS("_SYSTEM_"+__name__,"SYS_RESTART",{}, "TERMINAL")

app = Flask(__name__)
# Minify(app=app, html=True, js=True, cssless=True)
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
app.register_blueprint(dcf.app);
app.register_blueprint(fmi.app);

print(" * MIS Stat")


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

@app.before_request
def before_request():
	# print("databse = "+c.DB_CRED[3])
	# ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
	ip_addr = request.access_route[0]
	agent = request.headers.get('User-Agent')
	# ss = open("l_header.txt","a")
	# ss.write("{}\n".format(json.dumps((request))))
	# ss.close()
	if( request.endpoint != "static" and "get_notif_unseen" not in str(request.endpoint).split(".")):
		if(request.endpoint != "index"):
			Logs.ACCESS_LOGS(ip_addr, request.endpoint, session, agent)
			# updated_mac = get_mac_address(ip=ip_addr)
			# print(" MAC ADDRESS")
			# print(updated_mac)
			# print(request.headers)
	pass


# 	return redirect("/we_will_be_back_later")
@app.after_request
def after_request_func(response):
	# if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	# print(response.get_json())
	return response

	
# - Dutchmil strawberry:
# SECRET RECIPEE COCKTAIL
# - Zafiro Premium GIN
# - COLD- 

# BE YOURSELF, TRUST UR GUTS 



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


# Register the custom filter on the Flask application
app.jinja_env.filters['format_timestamp'] = format_timestamp
