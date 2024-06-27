import Configurations as c
from modules.Connections import mysql

def _init_config_():
	c.SQLITE_DB = c.SQLITE_DB_LOCAL
	c.RECORDS = c.RECORDS_LINUX_LOCAL
	c.M_APPVER = c.M_APPVER_LOCAL

	c._SERVER_PORT = c.LOCAL_PORT
	c._HOST = c.LOCAL_HOST
	c._USER = c.LOCAL_USER
	c._PASSWORD = c.LOCAL_PASSWORD
	c._DATABASE = c.LOCAL_DATABASE
	c.DB_CRED = [c.LOCAL_HOST,"root","dtirapid",c.LOCAL_DATABASE,True] # DEV
	c.PORT = 80
	c.IS_ON_SERVER = False
	c.IP_address = c.LOCAL_IP



# ===========================================================================
print(" * LINUX -LOCAL Launch")


_init_config_()
import start_point as sp
db = mysql(*c.DB_CRED)
db.do("SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));")
_init_config_()
app = sp.app
# app.run(host=c.HOST,port=c._PORT,debug=c.IS_DEBUG,ssl_context='adhoc') 
app.run(host=c.HOST,port=c._PORT,debug=c.IS_DEBUG)
# app.run(debug=c.IS_DEBUG)
from controllers import Logs
Logs.ACCESS_LOGS("_SYSTEM_"+__name__,"SYS_EXIT",{}, "TERMINAL")

# mysql> source /mnt/c/Users/USER/Documents/dumps/Dump20240530/mis_2023backup05302024.sql