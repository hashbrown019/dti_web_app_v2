import Configurations as c

from flask import Flask, session, jsonify, request, redirect
from flask_cors import CORS,cross_origin
from flask_minify import Minify

from views.login import login
from views.home  import home
from views.webrep  import webrep
from views.feature_0  import feature_0
from views.psalm  import bp_app as psalm
from views.doofen  import bp_app as doofen
from views.fund_tracker  import bp_app as fund_tracker
from views.dcf  import bp_app as dcf

from modules.public_vars import public_vars
from controllers.inbound import inbound
from apis import api
import json
from controllers import Logs
# from getmac import get_mac_address
Logs.ACCESS_LOGS("_SYSTEM_"+__name__,"SYS_RESTART",{}, "TERMINAL")

app = Flask(__name__)
# Minify(app=app, html=True, js=True, cssless=True)
app.config['JSON_SORT_KEYS'] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.secret_key=c.SECRET_KEY
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(login.app)
app.register_blueprint(home.app)
app.register_blueprint(api.app)
app.register_blueprint(feature_0.app)
app.register_blueprint(webrep.app)
app.register_blueprint(psalm.app)
app.register_blueprint(doofen.app)
app.register_blueprint(fund_tracker.app)
app.register_blueprint(dcf.app)


@app.route("/")
def index():return redirect("/webrep")


@app.before_request
def before_request():
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

# SECRET RECIPEE COCKTAIL
# - Dutchmil strawberry:
# - Zafiro Premium GIN
# - COLD- 

# BE YOURSELF, TRUST UR GUTS 