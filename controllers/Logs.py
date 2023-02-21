from datetime import datetime
import Configurations as c

def ACCESS_LOGS(addr,endpoint,session):
	in_session = False
	user_id = "null"

	if("USER_DATA" in session):
		user_id = session["USER_DATA"][0]['id']
		in_session = True

	DATE_NOW = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
	strs = "{}||{}||{}||{}||{}".format(DATE_NOW, in_session, user_id, addr, endpoint)
	file_object = open(c.RECORDS+'/objects/logs/access.logs', 'a')
	file_object.write('{}\n'.format(strs))
	file_object.close()
