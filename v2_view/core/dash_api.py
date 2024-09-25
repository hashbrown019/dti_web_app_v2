from modules.Connections import mysql,sqlite
import Configurations as c
from flask import session

from modules.Req_Brorn_util import authenication ## NO UTHENITICATION/SESSION HOLDER

rapid_mysql = mysql(*c.DB_CRED)


def farmer_count_per_area():
	return


def get_area_staff():
	# return session["USER_DATA"]
	if(session["USER_DATA"][0]["security_group"]==1):
		return rapid_mysql.select("SELECT * FROM `users` WHERE `status`='active' ;")

	return rapid_mysql.select("SELECT * FROM `users` WHERE `rcu`='{}' AND `status`='active' ;".format(session["USER_DATA"][0]['rcu']) )

def get_security_group():
	return rapid_mysql.select("SELECT `_securitygroup`.*, `users`.`id` as 'by' , `users`.`name` FROM `_securitygroup` INNER JOIN `users` ON `_securitygroup`.`created_by`= `users`.`id` ;" )


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



