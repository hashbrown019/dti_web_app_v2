import Configurations as c

from flask import Flask, session, jsonify, request, redirect
from flask_cors import CORS,cross_origin
from flask_minify import Minify

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

print(" * MIS Stats ¾")

@app.route("/")
def index():
	if(c.IS_ON_SERVER):
		c.DB_CRED[3] = c.SERVER_DATABASE
		return redirect("https://dtirapid.ph/webrep")
	else:
		c.DB_CRED[3] = c.LOCAL_DATABASE
		return redirect("http://localhost:5000/webrep")

@app.route("/test_server") #NOT FOR LOCAL USE
def test_server():
	if(c.IS_ON_SERVER):
		return redirect("http://18.138.151.175/test_server_on_aws") #NOT FOR LOCAL USE
	else:
		return redirect("http://localhost:5000/test_server_on_aws")


@app.route("/test_server_on_aws")
def test_server_on_aws():
	c.DB_CRED[3] = c.MOCK_DATABASE_TEST
	print("=====================================")
	print(c.MOCK_DATABASE_TEST)
	print(c.DB_CRED[3])
	print("=====================================")
	return redirect("/webrep")


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

# SECRET RECIPEE COCKTAIL
# - Dutchmil strawberry:
# - Zafiro Premium GIN
# - COLD- 

# BE YOURSELF, TRUST UR GUTS 