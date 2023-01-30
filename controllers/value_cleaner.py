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

# 