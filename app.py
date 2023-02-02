import Configurations as c
c.SQLITE_DB = c.SQLITE_DB_SERVER
c.RECORDS = c.RECORDS_SERVER
c.M_APPVER = c.M_APPVER_SERVER

c._SERVER_PORT = c.SERVER_PORT
c._HOST = c.SERVER_HOST
c._USER = c.SERVER_USER
c._PASSWORD = c.SERVER_PASSWORD
c._DATABASE = c.SERVER_DATABASE
c.DB_CRED = [c.SERVER_HOST,c.SERVER_USER,c.SERVER_PASSWORD,c.SERVER_DATABASE] # DEV
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
from modules.Connections import mysql,sqlite

# print(" * Checking Database")
# rapid_mysql = mysql(*c.DB_CRED)
# print(rapid_mysql.select("SELECT * from `users`"))
# print(" * Checking Database DONE")


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

@app.route("/")
def index():return redirect("/login")
# ==================================
inbound_ = inbound(app)
inbound_._test_()
# ====================================


# =============================================================
if __name__ == '__main__':
	app.run()