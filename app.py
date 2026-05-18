import Configurations as c
from modules.Connections import mysql

def _init_config_():
	c.SQLITE_DB = c.SQLITE_DB_SERVER
	c.RECORDS = c.RECORDS_SERVER
	c.M_APPVER = c.M_APPVER_SERVER

	c._SERVER_PORT = c.SERVER_PORT
	c._HOST = c.SERVER_HOST
	c._USER = c.SERVER_USER
	c._PASSWORD = c.SERVER_PASSWORD
	c._DATABASE = c.SERVER_DATABASE
	c.DB_CRED = [c.SERVER_HOST,c.SERVER_USER,c.SERVER_PASSWORD,c.SERVER_DATABASE] # PRODUCTION DB CRED
	c.PORT = 80
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

from controllers import Logs
Logs.ACCESS_LOGS("_SYSTEM_"+__name__,"SYS_EXIT",{}, "TERMINAL","terminal_start")
