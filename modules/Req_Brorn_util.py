from werkzeug.utils import secure_filename
from datetime import date, datetime
import os

class file_from_request:
	"""docstring for file_from_request"""
	def __init__(self,flaskapp):
		super(file_from_request, self).__init__()
		self.flaskapp = flaskapp

	def save_file_from_request(self,request,idfield,pathtosave="",raise_error=False,timestamp=False):
		file_arr_str = "";file_arr = [];files_count = 0;status ="unfinished";msg ="unfinished"
		try:
			files = request.files.getlist(idfield)
			for f in files:
				today = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
				tms = "";UPLOAD_NAME = secure_filename(f.filename)
				if(timestamp):tms=today
				_SAVE_NAME_FILE = "{}_{}".format(tms,UPLOAD_NAME)
				f.save(os.path.join(pathtosave,_SAVE_NAME_FILE ))
				file_arr_str+= "||"+(_SAVE_NAME_FILE)
				file_arr.append(_SAVE_NAME_FILE)
			files_count = len(files)
			status ="success"
			msg ="File transfer succeed"
		except Exception as e:
			status ="error"
			msg ="{}".format(e)
			if(raise_error):raise e
		return {
			"status" : status,
			"msg" : msg,
			"file_arr_str" : file_arr_str[2:],
			"file_arr" : file_arr,
			"idfield" : idfield,
			"pathtosave" : pathtosave,
			"files_count": files_count
		}