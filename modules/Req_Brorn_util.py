from werkzeug.utils import secure_filename
import os

class file_from_request:
	"""docstring for file_from_request"""
	def __init__(self,flaskapp, request):
		super(file_from_request, self).__init__()
		self.flaskapp = flaskapp
		self.request = request

	def save_file_from_request(self, idfield,pathtosave,raise_error=False):
		file_arr_str = ""
		file_arr = []
		files_count = 0
		status ="unfinished"
		msg ="unfinished"
		try:
			files = self.request.files.getlist(idfield)
			for f in files:
				UPLOAD_NAME = secure_filename(f.filename)
				f.save(os.path.join(pathtosave,UPLOAD_NAME ))
				file_arr_str+= "||"+(UPLOAD_NAME)
				file_arr.append(UPLOAD_NAME)
			files_count = len(files)
			status ="success"
			msg ="File transfer succeed"
		except Exception as e:
			status ="error"
			msg ="{}".format(e)
			if(raise_error):
				raise e
		return {
			"status" : status,
			"msg" : msg,
			"file_arr_str" : file_arr_str[2:],
			"file_arr" : file_arr,
			"idfield" : idfield,
			"pathtosave" : pathtosave,
			"files_count": files_count
		}