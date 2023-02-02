import Configurations as c
c.SQLITE_DB = c.SQLITE_DB_SERVER
c.RECORDS = c.RECORDS_SERVER
c.M_APPVER = c.M_APPVER_SERVER

c._SERVER_PORT = c.SERVER_PORT
c._HOST = c.SERVER_HOST
c._USER = c.SERVER_USER
c._PASSWORD = c.SERVER_PASSWORD
c._DATABASE = c.SERVER_DATABASE
c.DB_CRED = [c.LOCAL_HOST,c.LOCAL_USER,c.LOCAL_PASSWORD,c.LOCAL_DATABASE] # DEV
# ======================================================================
print(" * Providing Imports Flask app")

from flask import Flask, session, jsonify, request, redirect
from flask_cors import CORS,cross_origin
from flask_minify import Minify

from views.login import login
from views.home  import home
from views.feature_0  import feature_0 

from modules.public_vars import public_vars
from controllers.inbound import inbound
from apis import api


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

# ==================================
inbound_ = inbound(app)
inbound_._test_()
# ====================================

print(" * Running Flask app")

rapid_mysql = mysql(*c.DB_CRED)
# =============================================================
if __name__ == '__main__':
	app.run()