from modules.Connections import mysql,sqlite
import Configurations as c
from flask import session

rapid_mysql = mysql(*c.DB_CRED)


def farmer_count_per_area():
	return

# ================================================
# ================================================
# ================================================
# ================================================


def position_data_filter():
	_filter = "WHERE 1 "
	JOB = session["USER_DATA"][0]["job"].lower()

	if(JOB in "admin" or JOB in "super admin"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = "WHERE 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = "WHERE USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
	return _filter


