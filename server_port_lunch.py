import Configurations as c
from modules.Connections import mysql
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path="/var/www/html/dti_web_app_v2/.env")

def _init_config_():
	c.SQLITE_DB = c.SQLITE_DB_SERVER
	c.RECORDS = c.RECORDS_SERVER
	c.M_APPVER = c.M_APPVER_SERVER
 
	SERVER_PORT = ( os.getenv("SERVER_PORT") if os.getenv("SERVER_PORT") else "" )
	SERVER_HOST = ( os.getenv("SERVER_HOST") if os.getenv("SERVER_HOST") else "" )
	SERVER_USER = ( os.getenv("SERVER_USER") if os.getenv("SERVER_USER") else "" )
	SERVER_PASSWORD = ( os.getenv("SERVER_PASSWORD") if os.getenv("SERVER_PASSWORD") else "" )
	SERVER_DATABASE = ( os.getenv("SERVER_DATABASE") if os.getenv("SERVER_DATABASE") else "" )
	
	c._SERVER_PORT = SERVER_PORT
	c._HOST = SERVER_HOST
	c._USER = SERVER_USER
	c._PASSWORD = SERVER_PASSWORD
	c._DATABASE = SERVER_DATABASE
	c.DB_CRED = [SERVER_HOST,SERVER_USER,SERVER_PASSWORD,SERVER_DATABASE] # DEV
	c.PORT = SERVER_PORT
 
	c.IS_ON_SERVER = True
# ======================================================================

print(" * Providing Imports Flask app")

def nullified(args):pass
# print = nullified

_init_config_()
import start_point as sp
db = mysql(*c.DB_CRED)
# db.do("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
_init_config_()
app = sp.app

# app.run(host=c.HOST,port=c._PORT,debug=c.IS_DEBUG,ssl_context='adhoc')
# app.run(host=c.HOST,port=c._PORT,debug=c.IS_DEBUG)
app.run(host="0.0.0.0",port=c._PORT,debug=c.IS_DEBUG)

from controllers import Logs
Logs.ACCESS_LOGS("_SYSTEM_"+__name__,"SYS_EXIT",{}, "TERMINAL")
