import Configurations as c
c.SQLITE_DB = c.SQLITE_DB_LOCAL
c.RECORDS = c.RECORDS_LOCAL
c.M_APPVER = c.M_APPVER_LOCAL

c._SERVER_PORT = c.LOCAL_PORT
c._HOST = c.LOCAL_HOST
c._USER = c.LOCAL_USER
c._PASSWORD = c.LOCAL_PASSWORD
c._DATABASE = c.LOCAL_DATABASE
c.PORT = 80

# ===========================================================================
print(" * LOCAL Launch")

from flask import Flask, session, jsonify, request, redirect
from flask_cors import CORS,cross_origin
from flask_minify import Minify

from views.login import login
from views.home  import home
from modules.public_vars import public_vars

app = Flask(__name__)
# Minify(app=app, html=True, js=True, cssless=True)
app.config['JSON_SORT_KEYS'] = False
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.secret_key=c.SECRET_KEY
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(login.app)
app.register_blueprint(home.app)


@app.route("/")
def index():return redirect("/login")

# @app.before_request
# def before_request():
# 	if( request.endpoint != "static" and "Handshake" not in str(request.endpoint).split(".")):
# 		if "USER_DATA" not in session:
# 			if(request.endpoint != "login.login"):
# 				return redirect('/login')
# 		else:
# 			if(request.endpoint == "login.login"):
# 				return redirect('/home')
# 	pass

# app.run(host=c.HOST,port=c._PORT,debug=c.IS_DEBUG,ssl_context='adhoc')
public_vars(app)
app.run(host=c.HOST,port=c._PORT,debug=c.IS_DEBUG)
