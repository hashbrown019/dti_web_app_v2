import os, json, random, shutil
from tqdm import tqdm
import Configurations as c
from modules.Connections import mysql,sqlite



rapid_sqlite = sqlite(c.SQLITE_DB)
rapid_mysql = mysql(*c.DB_CRED)

# rapid_mysql.err_page = 0 # VALUE 0 = allow mysql error not to display err-page

# print(rapid_mysql.select("SELECT `names` FROM `form_a_farmer_profiles`;"))

class file_handler:
	"""docstring for file_handler"""
	def __init__(self, app_):
		super(file_handler, self).__init__()
		self.app_ = app_
		
	def _test_(self):
		print(" * Testing file_handler | {}".format(self.app_))
		pass
		# ======================================
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

# =====================================================================================================
# =====================================================================================================
# ====================FARMER PROFILE=======================================================================
# =====================================================================================================
class form_a1_handler:
	def __init__(self,args):
		super(form_a1_handler, self).__init__()
		self.args = args

	def get_all_file_farmer_profile(self):
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		# dir_path = c.RECORDS+"/objects/profiling_forms/queued/_temp_/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		_counter = 0
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@profile")>=0):
					loads_.desc = "inserted [{}] * {}".format(_counter,path)
					# res.append(path)
					# try:
					try:
						data_ = self.profile_info_farmer(path)
						self.push_mysql(data_,path)
						res.append(path)
						_counter = _counter + 1
					except ValueError:
						print("json error")
						# return ({"response":"error","message":ValueError})
					except Exception as ex:
						template = "An exception of type {0} occurred. Arguments:\n{1!r}"
						message = template.format(type(ex).__name__, ex.args)
						print(message)
						return ({"response":"error","message":message})

					# 	pass
					# except Exception as e:
					# 	print("ERROR : |"+str(e))
			# if(_counter == 4):
			# 	break
		# res = migrations.excel_popu()
		# res = res + migrations.excel_popu()
		random.shuffle(res)
		return res

	def profile_info_farmer(self,path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		# f = open(c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['addr_region'] = file_handler.region_name_cleaner(prof_1['addr_region'])
		prof_1['farmer-primary_crop'] = file_handler.crops_name_cleaner(prof_1['farmer-primary_crop'])
		prof_1['farmer-fo_name_rapid']  = file_handler.other_name_cleaner(prof_1['farmer-fo_name_rapid'])
		prof_1['farmer_dip_ref']  = file_handler.other_name_cleaner(prof_1['farmer_dip_ref'])
		# prof_1['farmer_img_base64'] = "";
		prof_1['SOURCE'] = "MOBILE";
		return prof_1

	def push_mysql(self,data_,FILENAME):
		path_img_res = c.RECORDS+"/objects/img_resource/farmer_profile_img/"
		fields = ""
		vals = ""


		farmer_code = data_["farmer_code"]  # get farmer code
		img_data = data_["farmer_img_base64"] # get img_data for storing
		filename_img = "farmer_profile_img_{}".format(farmer_code) # generate filename for img_data

		if(len(img_data)>=20):
			fff = open(path_img_res+filename_img,"w")
			fff.write(img_data)
			fff.close()

		data_["farmer_img_base64"] = filename_img # #force value for mysql - VALUE = FILENAME
		
		for datum in data_:
			datum_ = datum.replace("-","_")
			fields = fields + ",`"+ datum_ +"`"
			datum_val = data_[datum]
			vals = vals + ",'"+ str(datum_val).replace("'"," ").replace('''"'''," ") +"'"
			
		fields = fields[1:]
		vals = vals[1:]

		sql = ("INSERT INTO `form_a_farmer_profiles` ({}) VALUES ({})".format(fields,vals))
		rapid_mysql.do(sql)


		shutil.move(
			c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+FILENAME,
			# c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/migrated/pf_a/a1/"+FILENAME
		)
		pass
# =====================================================================================================
# =====================================================================================================
# ================FARM LAND INFO=====================================================================================
# =====================================================================================================
class form_a2_handler:
	def __init__(self,args):
		super(form_a2_handler, self).__init__()
		self.args = args

	def get_all_file_farmer_farmland(self):
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		# dir_path = c.RECORDS+"/objects/profiling_forms/queued/_temp_/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		_counter = 0
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@add_farm")>=0):
					loads_.desc = "inserted [{}] * {}".format(_counter,path)
					# res.append(path)
					try:
						data_ = self.profile_info_farmer(path)
						self.push_mysql(data_,path)
						res.append(path)
						_counter = _counter + 1
					except ValueError:
						print("json error")
						# return ({"response":"error","message":ValueError})
					except Exception as ex:
						template = "An exception of type {0} occurred. Arguments:\n{1!r}"
						message = template.format(type(ex).__name__, ex.args)
						print(message)
						return ({"response":"error","message":message})
			# if(_counter == 4):
			# 	break
		random.shuffle(res)
		return res

	def profile_info_farmer(self,path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		# f = open(c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['addr_region'] = file_handler.region_name_cleaner(prof_1['addr_region'])
		prof_1['SOURCE'] = "MOBILE";
		return prof_1

	def push_mysql(sef,data_,FILENAME):
		path_img_res = c.RECORDS+"/objects/img_resource/farmland_img/"
		fields = ""
		vals = ""

		farmer_code = data_["farmer_code"]  # get farmer code
		img_data = data_["farm-photo"] # get img_data for storing
		filename_img = "farmland_img{}".format(farmer_code) # generate filename for img_data

		if(len(img_data)>=20):
			fff = open(path_img_res+filename_img,"w")
			fff.write(img_data)
			fff.close()

		data_["farm-photo"] = filename_img # #force value for mysql - VALUE = FILENAME
		
		for datum in data_:
			datum_ = datum.replace("-","_")
			fields = fields + ",`"+ datum_ +"`"
			datum_val = data_[datum]
			vals = vals + ",'"+ str(datum_val).replace("'"," ").replace('''"'''," ") +"'"
			
		fields = fields[1:]
		vals = vals[1:]

		sql = ("INSERT INTO `form_a_farm_land` ({}) VALUES ({})".format(fields,vals))
		rapid_mysql.do(sql)


		shutil.move(
			# c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/migrated/pf_a/a2/"+FILENAME
		)
		pass
# =====================================================================================================
# =====================================================================================================
# ================HOUSE HOLd PROFILE=====================================================================================
# =====================================================================================================
class form_a3_handler:
	def __init__(self,args):
		super(form_a3_handler, self).__init__()
		self.args = args

	def get_all_file_farmer_hh_profile(self):
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		# dir_path = c.RECORDS+"/objects/profiling_forms/queued/_temp_/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		_counter = 0
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@hh_profile")>=0):
					loads_.desc = "inserted [{}] * {}".format(_counter,path)
					# res.append(path)
					try:
						data_ = self.profile_info_farmer(path)
						self.push_mysql(data_,path)
						res.append(path)
						_counter = _counter + 1
					except ValueError:
						print("json error")
						# return ({"response":"error","message":ValueError})
					except Exception as ex:
						template = "An exception of type {0} occurred. Arguments:\n{1!r}"
						message = template.format(type(ex).__name__, ex.args)
						print(message)
						return ({"response":"error","message":message})
			# if(_counter == 4):
			# 	break
		random.shuffle(res)
		return res

	def profile_info_farmer(self,path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		# f = open(c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['SOURCE'] = "MOBILE";
		return prof_1

	def push_mysql(sef,data_,FILENAME):
		fields = ""
		vals = ""
		
		for datum in data_:
			datum_ = datum.replace("-","_")
			fields = fields + ",`"+ datum_ +"`"
			datum_val = data_[datum]
			vals = vals + ",'"+ str(datum_val).replace("'"," ").replace('''"'''," ") +"'"
			
		fields = fields[1:]
		vals = vals[1:]

		sql = ("INSERT INTO `form_a_hh_profile` ({}) VALUES ({})".format(fields,vals))
		rapid_mysql.do(sql)


		shutil.move(
			# c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/migrated/pf_a/a3/"+FILENAME
		)
		pass
# =====================================================================================================
# =====================================================================================================
# ================PRODUCTION COST=====================================================================================
# =====================================================================================================
class form_a4_handler:
	def __init__(self,args):
		super(form_a4_handler, self).__init__()
		self.args = args

	def get_all_file_farmer_prod_cost(self):
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		# dir_path = c.RECORDS+"/objects/profiling_forms/queued/_temp_/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		_counter = 0
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@prod_cost")>=0):
					loads_.desc = "inserted [{}] * {}".format(_counter,path)
					# res.append(path)
					try:
						data_ = self.profile_info_farmer(path)
						self.push_mysql(data_,path)
						res.append(path)
						_counter = _counter + 1
					except ValueError:
						print("json error")
						# return ({"response":"error","message":ValueError})
					except Exception as ex:
						template = "An exception of type {0} occurred. Arguments:\n{1!r}"
						message = template.format(type(ex).__name__, ex.args)
						print(message)
						return ({"response":"error","message":message})
			# if(_counter == 4):
			# 	break
		random.shuffle(res)
		return res

	def profile_info_farmer(self,path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		# f = open(c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['SOURCE'] = "MOBILE";
		return prof_1

	def push_mysql(sef,data_,FILENAME):
		fields = ""
		vals = ""
		
		for datum in data_:
			datum_ = datum.replace("-","_")
			fields = fields + ",`"+ datum_ +"`"
			datum_val = data_[datum]
			vals = vals + ",'"+ str(datum_val).replace("'"," ").replace('''"'''," ") +"'"
			
		fields = fields[1:]
		vals = vals[1:]

		sql = ("INSERT INTO `form_a_prod_cost` ({}) VALUES ({})".format(fields,vals))
		rapid_mysql.do(sql)


		shutil.move(
			# c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/migrated/pf_a/a4/"+FILENAME
		)
		pass
# =====================================================================================================
# =====================================================================================================
# ================WORKERS AND LABORERS=====================================================================================
# =====================================================================================================
class form_a5_handler:
	def __init__(self,args):
		super(form_a5_handler, self).__init__()
		self.args = args

	def get_all_file_farmer_workers_laborers(self):
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		# dir_path = c.RECORDS+"/objects/profiling_forms/queued/_temp_/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		_counter = 0
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@workers_laborers")>=0):
					loads_.desc = "inserted [{}] * {}".format(_counter,path)
					# res.append(path)
					try:
						data_ = self.profile_info_farmer(path)
						self.push_mysql(data_,path)
						res.append(path)
						_counter = _counter + 1
					except ValueError:
						print("json error")
						# return ({"response":"error","message":ValueError})
					except Exception as ex:
						template = "An exception of type {0} occurred. Arguments:\n{1!r}"
						message = template.format(type(ex).__name__, ex.args)
						print(message)
						return ({"response":"error","message":message})
			# if(_counter == 4):
			# 	break
		random.shuffle(res)
		return res

	def profile_info_farmer(self,path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		# f = open(c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['SOURCE'] = "MOBILE";
		return prof_1

	def push_mysql(sef,data_,FILENAME):
		fields = ""
		vals = ""
		
		for datum in data_:
			datum_ = datum.replace("-","_")
			fields = fields + ",`"+ datum_ +"`"
			datum_val = data_[datum]
			vals = vals + ",'"+ str(datum_val).replace("'"," ").replace('''"'''," ") +"'"
			
		fields = fields[1:]
		vals = vals[1:]

		sql = ("INSERT INTO `form_a_farm_workers_laborers` ({}) VALUES ({})".format(fields,vals))
		rapid_mysql.do(sql)


		shutil.move(
			# c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+FILENAME,
			c.RECORDS+"/objects/profiling_forms/migrated/pf_a/a5/"+FILENAME
		)
		pass


# =====================================================================================================
# =====================================================================================================
# ================WORKERS AND LABORERS=====================================================================================
# =====================================================================================================
class form_a6_handler:
	def __init__(self,args):
		super(form_a6_handler, self).__init__()
		self.args = args

	def get_all_file_farmer_post_harvest(self):
		res = []
		dir_path = c.RECORDS+"/objects/profiling_forms/queued/pf_a/";
		# dir_path = c.RECORDS+"/objects/profiling_forms/queued/_temp_/";
		_title = "----";
		loads_ = tqdm(os.listdir(dir_path),  desc =_title,ascii ="►>○•|█");
		_counter = 0
		for path in loads_:
			if os.path.isfile(os.path.join(dir_path, path)):
				if(path.find("@post_harvest")>=0):
					loads_.desc = "inserted [{}] * {}".format(_counter,path)
					# res.append(path)
					try:
						data_ = self.profile_info_farmer(path)
						self.push_mysql(data_,path)
						res.append(path)
						_counter = _counter + 1
						# break
					except ValueError:
						print("json error")
						# return ({"response":"error","message":ValueError})
					except Exception as ex:
						template = "An exception of type {0} occurred. Arguments:\n{1!r}"
						message = template.format(type(ex).__name__, ex.args)
						print(message)
						return ({"response":"error","message":message})
			# if(_counter == 100):
			# 	break
		random.shuffle(res)
		return res

	def profile_info_farmer(self,path):
		f = open(c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+ path, "r")
		# f = open(c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+ path, "r")
		strsd = f.read()
		f.close()
		prof_1 = "ERROR"
		prof_1 = json.loads(json.loads(strsd));
		prof_1['SOURCE'] = "MOBILE";
		return prof_1

	def push_mysql(sef,data_,FILENAME):
		post_harvest_fields = {"record_num":[],"record_duplicate_id":[],"farmer_code":[],"is_synced":[],"datetime":[],"post_harv-type_faci_equip":[],"post_harv-type_faci_equip_name":[],"farmer-coords_long":[],"farmer-coords_lat":[],"addr_region":[],"addr_prov":[],"addr_city":[],"addr_brgy":[],"addr_street_purok_sitio":[],"post_harv-ph_product_form":[],"post_harv-phcropothers":[],"post_harv-capacity":[],"post_harv-capacity_unit":[],"post_harv-capacity_unit_time":[],"post_harv-photo":[],"form-remarks":[],"USER_ID":[]}
		fields = ""
		vals = ""
		# if(data_["farmer_code"] == "BMCnJlXQCzZqxyfZAWqXxq0AlmSnIRmg14VP7r6E6JMGn6tSiuL61XzPG42mmgG0j9aazYYz1Yrb"):
		if("addr_prov1" in data_):
			print("===================================")

			print("FARMER_CODE_ID ::: {}".format(data_["farmer_code"]))
			for datum in data_:
				for ph_field in post_harvest_fields:
					if(ph_field in datum):
						post_harvest_fields[ph_field].append(data_[datum])


			print("===================================")
			print(post_harvest_fields)
			# val = None + 1
		# for datum in data_:
		# 	datum_ = datum.replace("-","_")
		# 	fields = fields + ",`"+ datum_ +"`"
		# 	datum_val = data_[datum]
		# 	vals = vals + ",'"+ str(datum_val).replace("'"," ").replace('''"'''," ") +"'"
			
		# fields = fields[1:]
		# vals = vals[1:]

		# sql = ("INSERT INTO `form_a_farm_post_harvest` ({}) VALUES ({})".format(fields,vals))
		# rapid_mysql.do(sql)


		# shutil.move(
		# 	# c.RECORDS+"/objects/profiling_forms/queued/_temp_/"+FILENAME,
		# 	c.RECORDS+"/objects/profiling_forms/queued/pf_a/"+FILENAME,
		# 	c.RECORDS+"/objects/profiling_forms/migrated/pf_a/a6/"+FILENAME
		# )
		pass
