from datetime import datetime
import Configurations as c

from getmac import get_mac_address

def ACCESS_LOGS(addr, endpoint, session, agent):
	in_session = False
	user_id = "null"
	user_name = "null"
	uname = "null"
	mac_addr = get_mac_address(ip=addr)
	if("USER_DATA" in session):
		user_id = session["USER_DATA"][0]['id']
		user_name = session["USER_DATA"][0]['username']
		uname = session["USER_DATA"][0]['name']
		in_session = True

	date_ar = str(datetime.today()).split(" ")[0].split("-")
	date_file_name = "{}_{}".format(date_ar[0],date_ar[1])
	print(date_file_name)
	DATE_NOW = str(str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_"))
	strs = "{}||{}||{}||{}||{}||{}||{}||{}||{}\n".format(DATE_NOW, in_session, user_id,user_name, uname, addr, mac_addr,endpoint,agent)
	file_object = open(c.RECORDS+'/objects/logs/'+date_file_name+'.logs', 'a')
	file_object.write(f"{strs}")
	# file_object.write(str(('{}\n'.format(strs)).encode('utf-8').strip()))
	file_object.close()
