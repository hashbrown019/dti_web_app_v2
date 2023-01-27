import Configurations as c
from tqdm import tqdm
import os
import json
from modules.Connections import mysql,sqlite


rapid_sqlite = sqlite(c.SQLITE_DB)
rapid_mysql = mysql(*c.DB_CRED)


class file_handler:
	"""docstring for file_handler"""
	def __init__(self, app_):
		super(file_handler, self).__init__()
		self.app_ = app_
		
	def _test_(self):
		print(" * Testing file_handler | {}".format(self.app_))
		pass

	def get_all_file_farmer_profile():
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@profile")>=0):
					loads_.desc = " * "+path
					# res.append(path)
					try:
						res.append(file_handler.profile_info_farmer(path))
						pass
					except Exception as e:
						print(e)
		# res = migrations.excel_popu()
		# res = res + migrations.excel_popu()
		random.shuffle(res)
		return res

	def profile_info_farmer(path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['addr_region'] = file_handler.region_name_cleaner(prof_1['addr_region'])
		prof_1['farmer-primary_crop'] = file_handler.crops_name_cleaner(prof_1['farmer-primary_crop'])
		prof_1['farmer-fo_name_rapid']  = file_handler.other_name_cleaner(prof_1['farmer-fo_name_rapid'])
		prof_1['farmer_dip_ref']  = file_handler.other_name_cleaner(prof_1['farmer_dip_ref'])
		prof_1['farmer_img_base64'] = "";
		prof_1['SOURCE'] = "MOBILE";

		USER = rapid_sqlite.select("SELECT * FROM `users` WHERE `id`={} ORDER BY `name` ASC; ".format(prof_1["USER_ID"]))
		if(len(USER)<=0):
			prof_1["input_by"] = {"name":"none"}
		else:
			prof_1["input_by"] = {}
			USER[0]["password"] = "CONFIDENTIAL"
			prof_1["input_by"] = USER[0]
		return prof_1


	# =======================================

	# =========================================================================================
	# THIS FUNCTION FIX THE REGION name with SIMILAR AREA
	def region_name_cleaner(region):
		region = str(region)
		roman_numerals = ["i","ii","iii","iv","v","vi","vii","viii","ix","x","xi","xii","xiii"]
		num_digits = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
		region = region.lower()
		region = region.replace(" ","")
		region = region.replace("caraga","13")
		region = region.replace("car","13")
		region = region.replace("region","")
		region = region.replace("r-","")
		region = region.replace("r:","")
		if(region==""):region = 'Untagged';
		else:
			try:
				if(region.isnumeric()):
					region = region
				else:
					region = num_digits[roman_numerals.index(region)]
			except Exception as e:
				region = region + ""
		return region

	# THIS FUNCTION FIX THE crops name with SIMILAR AREA
	def crops_name_cleaner(crops):
		crops = str(crops);
		crops = crops.lower();
		crops = crops.replace(" ","");
		if(crops==""):crops = 'Untagged';
		return crops

	# THIS FUNCTION FIX THE crops name with SIMILAR AREA
	def other_name_cleaner(strs):
		strs = str(strs);
		strs = strs.lower();
		strs = strs.replace("  "," ");
		strs = strs.replace(" - ","-");
		strs = strs.replace(" -","-");
		strs = strs.replace("- ","-");
		if(strs==""):strs = 'Untagged';
		return strs.upper();