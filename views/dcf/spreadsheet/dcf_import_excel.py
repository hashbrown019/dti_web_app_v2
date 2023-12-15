from flask import request, flash,redirect, session
from modules.Connections import mysql
from flask_session import Session
import Configurations as c
import xlrd
from werkzeug.utils import secure_filename
import os

db = mysql(*c.DB_CRED)
db.err_page = 0
def is_on_session(): return ('USER_DATA' in session)

def importcsvform1(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-","").replace(" ","").replace(":","").replace(".","")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader)+"#"+str(today)+"#"+secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS+"/objects/spreadsheets_dcf/queued/",UPLOAD_NAME ))
				excel_upload_open(os.path.join(c.RECORDS+"/objects/spreadsheets_dcf/queued/",UPLOAD_NAME ))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
			
	return redirect("/dcfspreadsheet")

def excel_upload_open(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	if(sheet.name !='form1'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_1_rcus = str(row[0]).split(".")[0]
		form_1_name_dip = row[1]
		form_1_anchor_firm = row[2]
		form_1_size_of_anchor = row[3]
		form_1_msmes = row[4]
		form_1_scope_provinces = row[5]
		form_1_commodity = row[6]
		form_1_for_development = row[7]
		form_1_finalized_approved = row[8]
		form_1_date_of_parallel_review = row[9]
		form_1_date_of_submission = row[10]
		form_1_date_of_rtwg = row[11]
		form_1_date_of_npco_cursory = row[12]
		form_1_date_of_ifad_no_inssuance = row[13]
		total_large_enterprise = row[14]
		total_medium_enterprise = row[15]
		total_small_enterprise = row[16]
		total_micro_enterprise = row[17]
		form_1_totalmale = row[18]
		form_1_maleyouth = row[19]
		form_1_maleip = row[20]
		form_1_malepwd = row[21]
		form_1_totalfemale = row[22]
		form_1_femaleyouth = row[23]
		form_1_femaleip = row[24]
		form_1_femalepwd = row[25]
		form_1_totalyouth = row[26]
		form_1_totalip = row[27]
		form_1_totalpwd = row[28]
		form_1_totalcooperatives = row[29]
		form_1_totalassociations = row[30]
		form_1_totalmsme = row[31]
		form_1_total_farmerbene = row[32]
		form_1_totalfo = row[33]
		form_1_hect_rehab = row[34]
		form_1_total_cost_rehab = row[35]
		form_1_hect_exp = row[36]
		form_1_cost_exp = row[37]
		form_1_totalhectarage_cov = row[38]
		form_1_euqipment = row[39]
		form_1_Facilities_warehouse = row[40]
		form_1_totalcost_prodinvest = row[41]
		form_1_total_rehab = row[42]
		form_1_total_exp = row[43]
		form_1_totalcost_prodinvest2 = row[44]
		form_1_partners_counterpart = row[45]
		form_1_total_matching_grant = row[46]
		form1_total_mg_cost = row[47]
		form_1_organizational = row[48]
		form_1_technical_trainings = row[49]
		form_1_post_production = row[50]
		form_1_others = row[51]
		form_1_total_capbuild = row[52]
		form_1_total_capbuild_counterpart = row[53]
		form_1_supply_chain_manager = row[54]
		supply_chain_manager_counterpart = row[55]
		form_1_fmi = row[56]
		form_1_fmi_kms = row[57]
		fmi_part_counter = row[58]
		form_1_y = row[59]
		form_1_ac = row[60]
		form_1_ad = row[61]
		form1_total_fmi = row[62]
		form_1_totalproject_cost = row[63]
		partner_counterpart_MG = row[64]
		partner_counterpart_CB = row[65]
		partner_counterpart_SCM = row[66]
		partner_counterpart_FMI = row[67]
		partner_counterpart_total = row[68]
		total_dip_cost_MG = row[69]
		total_dip_cost_CB = row[70]
		total_dip_cost_SCM = row[71]
		total_dip_cost_FMI = row[72]
		total_dip_cost_total = row[73]                                                                                      
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_prep_review_aprv_status ( upload_by, form_1_rcus,form_1_name_dip,form_1_anchor_firm,form_1_size_of_anchor,form_1_msmes,form_1_scope_provinces,form_1_commodity,form_1_for_development,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_ifad_no_inssuance,total_large_enterprise,total_medium_enterprise,total_small_enterprise,total_micro_enterprise,form_1_totalmale,form_1_maleyouth,form_1_maleip,form_1_malepwd,form_1_totalfemale,form_1_femaleyouth,form_1_femaleip,form_1_femalepwd,form_1_totalyouth,form_1_totalip,form_1_totalpwd,form_1_totalcooperatives,form_1_totalassociations,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalhectarage_cov,form_1_euqipment,form_1_Facilities_warehouse,form_1_totalcost_prodinvest,form_1_total_rehab,form_1_total_exp,form_1_totalcost_prodinvest2,form_1_partners_counterpart,form_1_total_matching_grant,form1_total_mg_cost,form_1_organizational,form_1_technical_trainings,form_1_post_production,form_1_others,form_1_total_capbuild,form_1_total_capbuild_counterpart,form_1_supply_chain_manager,supply_chain_manager_counterpart,form_1_fmi,form_1_fmi_kms,fmi_part_counter,form_1_y,form_1_ac,form_1_ad,form1_total_fmi,form_1_totalproject_cost,partner_counterpart_MG,partner_counterpart_CB,partner_counterpart_SCM,partner_counterpart_FMI,partner_counterpart_total,total_dip_cost_MG,total_dip_cost_CB,total_dip_cost_SCM,total_dip_cost_FMI,total_dip_cost_total,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_1_rcus,form_1_name_dip,form_1_anchor_firm,form_1_size_of_anchor,form_1_msmes,form_1_scope_provinces,form_1_commodity,form_1_for_development,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_ifad_no_inssuance,total_large_enterprise,total_medium_enterprise,total_small_enterprise,total_micro_enterprise,form_1_totalmale,form_1_maleyouth,form_1_maleip,form_1_malepwd,form_1_totalfemale,form_1_femaleyouth,form_1_femaleip,form_1_femalepwd,form_1_totalyouth,form_1_totalip,form_1_totalpwd,form_1_totalcooperatives,form_1_totalassociations,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalhectarage_cov,form_1_euqipment,form_1_Facilities_warehouse,form_1_totalcost_prodinvest,form_1_total_rehab,form_1_total_exp,form_1_totalcost_prodinvest2,form_1_partners_counterpart,form_1_total_matching_grant,form1_total_mg_cost,form_1_organizational,form_1_technical_trainings,form_1_post_production,form_1_others,form_1_total_capbuild,form_1_total_capbuild_counterpart,form_1_supply_chain_manager,supply_chain_manager_counterpart,form_1_fmi,form_1_fmi_kms,fmi_part_counter,form_1_y,form_1_ac,form_1_ad,form1_total_fmi,form_1_totalproject_cost,partner_counterpart_MG,partner_counterpart_CB,partner_counterpart_SCM,partner_counterpart_FMI,partner_counterpart_total,total_dip_cost_MG,total_dip_cost_CB,total_dip_cost_SCM,total_dip_cost_FMI,total_dip_cost_total,filename))
		insert=db.do(querycsv)
		
	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
		print(sheet.name)
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform2(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open2(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open2(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[3]
	
	print(sheet.name)
	if(sheet.name !='form2'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[3:]:
		upload_by = session["USER_DATA"][0]['id']
		form_2_rcus = row[0]                                                                       
		form_2_pcu = row[1]                                                                                                     
		form_2_commodity = row[2]                                                               
		form_2_dip_alignment = row[3]                                                               
		form_2_name_owner_manager = row[4]                                                   
		form_2_sex_owner_manager = row[5]                                                         
		form_2_sector_owner_manager = row[6]                                                   
		form_2_business_owner_manager = row[7]                                                                                                       
		form_2_partner_fo_engaged = row[8]                                                  
		form_2_chairperson_manager = row[9]                                                     
		form_2_sex_chairperson_manager = row[10]                                                                                                  
		form_2_sector_chairperson_manager = row[11]                                                                                   
		form_2_office_address_province = row[12]                                                                                      
		form_2_total_number_fo = row[13]                                                                                           
		form_2_male = row[14]                                                                                                                                             
		form_2_female = row[15]                                                                                           
		form_2_pwde = row[16]                                                                                     
		form_2_youth = row[17]                                                                                             
		form_2_ip = row[18]                                                                                                                                            
		form_2_sc = row[19]                                                                                                                                        
		form_2_address_of_fo_members = row[20]                                                   
		form_2_hectares_covered = row[21]                                            
		form_2_cpa_date_signing = row[22]                                          
		form_2_cpa_date_expiration = row[23]                                                                                            
		form_2_days_remaining = row[24]                                                                                           
		form_2_date_renewed = row[25]                                         
		form_2_notable_cpa_incentives = row[26]                                                                                     
		form_2_activity_agreements = row[27]                                             
		form_2_date_conducted = row[28]                                                                           
		form_2_remarks_status = row[29]                                                                                                                                  
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_implementing_unit ( upload_by,form_2_rcus,form_2_pcu,form_2_commodity,form_2_dip_alignment,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_activity_agreements,form_2_date_conducted,form_2_remarks_status,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by,form_2_rcus,form_2_pcu,form_2_commodity,form_2_dip_alignment,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_activity_agreements,form_2_date_conducted,form_2_remarks_status,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform3(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open3(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			print("Invalid file template on import!")
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open3(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	print(str(sheet.name) !='form3')
	if(str(sheet.name) !='form3'):
		print("Invalid file template!")
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_3_types_of_bdsp = row[0]
		form_3_contact_person = row[1]
		form_3_sex = row[2]
		form_3_office_addr = row[3]
		form_3_email = row[4]
		form_3_breif_description = row[5]
		phone = row[6]
		form_3_choices = row[7]
		form_3_preferred_region = row[8]
		form_3_preferred_province = row[9]
		form_3_name = row[10]
		form_3_education = row[11]
		form_3_expertise = row[12]
		form_3_prior_rapid_engagements = row[13]
		form_3_date_registered = row[14]
		form_3_rapid_implementing_unit = row[15]
		form_3_nature_engagements = row[16]
		form_3_suppliers_evaluation = row[17]
		form_3_other_engagement_outside_rapid = row[18]
		form_3_lecture_training_seminar = row[19]
		form_3_training_materials = row[20]
		form_3_organize_pool = "row[21]"
		form_3_demand_basis = "row[22]"
		form_3_extension_service_facilitation = "row[23]"
		form_3_philgeps_registered = "row[24]"                                                                                                          
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_bdsp_reg ( upload_by,form_3_types_of_bdsp,form_3_contact_person,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by,form_3_types_of_bdsp,form_3_contact_person,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform4(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open4(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open4(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form4'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[4:]:
		upload_by = session["USER_DATA"][0]['id']
		cbb_implementing_unit = row[0]
		cbb_activity_title = row[1]
		cbb_types_of_training = row[2]
		cbb_topic_of_training = row[3]
		cbb_dip_approved_alignment = row[4]
		cbb_name_of_dip = row[5]
		cbb_date_start = row[6]
		cbb_total_number_of_participants = row[7]
		cbb_commodity = row[8]
		cbb_venue = row[9]
		cbb_name_of_resource_person = row[10]
		cbb_rapid_actual_budget = row[11]
		cbb_dip_capbuild_activities_NPO = row[12]
		cbb_dip_capbuild_activities_CA = row[13]
		cbb_total_number_per_gender_male = row[14]
		cbb_total_number_per_gender_female = row[15]
		cbb_total_number_per_gender_total = row[16]
		cbb_total_number_per_sector_pwd = row[17]
		cbb_total_number_per_sector_youth = row[18]
		cbb_total_number_per_sector_ip = row[19]
		cbb_total_number_per_sector_sc = row[20]
		cbb_total_number_per_sector_total = row[21]
		cbb_results_of_activity_pre_test = row[22]
		cbb_results_of_activity_post_test = row[23]
		cbb_client_feedback_survey_rating = row[24]
		cbb_client_feedback_survey_comments_AOI = row[25]                                                                                                        
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_capacity_building ( upload_by, cbb_implementing_unit,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_total_number_of_participants,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, cbb_implementing_unit,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_total_number_of_participants,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform5(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open5(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open5(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form5'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[6:]:
		upload_by = session["USER_DATA"][0]['id']
		mgit_implementing_unit = row[0]
		mgit_name_of_dip = row[1]
		mgit_msme_recipient = row[2]
		mgit_total_member_recipient = row[3]
		mgit_commodity = row[4]
		mgit_total_number_fo_gender_male = row[5]
		mgit_total_number_fo_gender_female = row[6]
		mgit_total_number_fo_sectoral_pwd = row[7]
		mgit_total_number_fo_sectoral_youth = row[8]
		mgit_total_number_fo_sectoral_IP = row[9]
		mgit_total_number_fo_sectoral_SC = row[10]
		mgit_type_of_investment = row[11]
		mgit_total_mgas_based_approved_DIP = row[12]
		mgit_total_mgas_signed = row[13]
		mgit_total_mgas_not_yet_signed = row[14]
		mgit_total_matching_grant_based_on_approved_business = row[15]
		mgit_pmga_first_availment = row[16]
		mgit_mgar_period_date = row[17]
		mgit_remaining_matching_grant_balance = row[18]
		mgit_inclusive_timeline_implementation_start = row[19]
		mgit_inclusive_timeline_implementation_end = row[20]
		mgit_time_elapse = row[21]
		mgit_total_budget_approved_in_the_DIP = row[22]
		mgit_actual_cost_of_procurement = row[23]
		mgit_summary_of_actual_tools_procured = row[24]
		mgit_inclusive_timeline_implementation_start1 = row[25]
		mgit_inclusive_timeline_implementation_end1 = row[26]
		mgit_time_elapse1 = row[27]
		mgit_date_of_distribution = row[28]
		mgit_remarks_on_the_deliverd_tools = row[29]                                                                                                     
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_matching_grant ( upload_by,mgit_implementing_unit,mgit_name_of_dip,mgit_msme_recipient,mgit_total_member_recipient,mgit_commodity,mgit_total_number_fo_gender_male,mgit_total_number_fo_gender_female,mgit_total_number_fo_sectoral_pwd,mgit_total_number_fo_sectoral_youth,mgit_total_number_fo_sectoral_IP,mgit_total_number_fo_sectoral_SC,mgit_type_of_investment,mgit_total_mgas_based_approved_DIP,mgit_total_mgas_signed,mgit_total_mgas_not_yet_signed,mgit_total_matching_grant_based_on_approved_business,mgit_pmga_first_availment,mgit_mgar_period_date,mgit_remaining_matching_grant_balance,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_budget_approved_in_the_DIP,mgit_actual_cost_of_procurement,mgit_summary_of_actual_tools_procured,mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_date_of_distribution,mgit_remarks_on_the_deliverd_tools,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by,mgit_implementing_unit,mgit_name_of_dip,mgit_msme_recipient,mgit_total_member_recipient,mgit_commodity,mgit_total_number_fo_gender_male,mgit_total_number_fo_gender_female,mgit_total_number_fo_sectoral_pwd,mgit_total_number_fo_sectoral_youth,mgit_total_number_fo_sectoral_IP,mgit_total_number_fo_sectoral_SC,mgit_type_of_investment,mgit_total_mgas_based_approved_DIP,mgit_total_mgas_signed,mgit_total_mgas_not_yet_signed,mgit_total_matching_grant_based_on_approved_business,mgit_pmga_first_availment,mgit_mgar_period_date,mgit_remaining_matching_grant_balance,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_budget_approved_in_the_DIP,mgit_actual_cost_of_procurement,mgit_summary_of_actual_tools_procured,mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_date_of_distribution,mgit_remarks_on_the_deliverd_tools,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform6(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open6(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open6(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form6'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_6_implementing_unit = row [0]
		form_6_type_of_assisstance = row [1]
		form_6_type_of_activity = row [2]
		form_6_dip_alignment = row [3]
		form_6_activity_duration_start = row [4]
		form_6_activity_duration_end = row [5]
		form_6_venue = row [6]
		form_6_resource_person = row [7]
		form_6_rapid_actual_budget = row [8]
		form_6_name_of_partner_organization_1 = row [9]
		form_6_name_of_partner_organization_2 = row [10]
		form_6_beneficiary_participant = row [11]
		form_6_commodity = row [12]
		form_6_type_of_beneficiary = row [13]
		form_6_sex = row [14]
		form_6_sector = row [15]
		form_6_product_developed = row [16]
		form_6_date_launched_to_market = row [17]
		form_6_improved_product = row [18]
		form_6_type_of_product_improvement = row [19]
		form_6_name_of_product_developed = row [20]
		form_6_ = row [21]
		form_6_certification = row [22]
		form_6_certification2 = row [23]
		form_6_date_issuance = row [24]
		form_6_expiration_date = row [25]
		form_6_product_certified = row [26]
		form_6_rating = row [27]
		form_6_comment_ares_of_improvement = row [28]                                                                                                     
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_product_development ( upload_by, form_6_implementing_unit,form_6_type_of_assisstance,form_6_type_of_activity,form_6_dip_alignment,form_6_activity_duration_start,form_6_activity_duration_end,form_6_venue,form_6_resource_person,form_6_rapid_actual_budget,form_6_name_of_partner_organization_1,form_6_name_of_partner_organization_2,form_6_beneficiary_participant,form_6_commodity,form_6_type_of_beneficiary,form_6_sex,form_6_sector,form_6_product_developed,form_6_date_launched_to_market,form_6_improved_product,form_6_type_of_product_improvement,form_6_name_of_product_developed,form_6_,form_6_certification,form_6_certification2,form_6_date_issuance,form_6_expiration_date,form_6_product_certified,form_6_rating,form_6_comment_ares_of_improvement,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_6_implementing_unit,form_6_type_of_assisstance,form_6_type_of_activity,form_6_dip_alignment,form_6_activity_duration_start,form_6_activity_duration_end,form_6_venue,form_6_resource_person,form_6_rapid_actual_budget,form_6_name_of_partner_organization_1,form_6_name_of_partner_organization_2,form_6_beneficiary_participant,form_6_commodity,form_6_type_of_beneficiary,form_6_sex,form_6_sector,form_6_product_developed,form_6_date_launched_to_market,form_6_improved_product,form_6_type_of_product_improvement,form_6_name_of_product_developed,form_6_,form_6_certification,form_6_certification2,form_6_date_issuance,form_6_expiration_date,form_6_product_certified,form_6_rating,form_6_comment_ares_of_improvement,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform7(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open7(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open7(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form7'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_7_implementing_unit = row [0]
		form_7_title_trade_promotion = row [1]
		form_7_type_of_trade_promotion = row [2]
		form_7_dip_indicate = row [3]
		form_7_start_date = row [4]
		form_7_end_date = row [5]
		form_7_name_of_po = row [6]
		form_7_amount = row [7]
		form_7_venue = row [8]
		form_7_rapid_actual_budget = row [9]
		form_7_name_of_beneficiary = row [10]
		form_7_commodity = row [11]
		form_7_beneficiary = row [12]
		form_7_sex = row [13]
		form_7_sector = row [14]
		form_7_type_of_products = row [15]
		form_7_name_of_buyer = row [16]
		form_7_cash_sales = row [17]
		form_7_booked_sales = row [18]
		form_7_under_negotiations = row [19]
		form_7_total_autosum = row [20]                                                                                                 
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_trade_promotion ( upload_by, form_7_implementing_unit,form_7_title_trade_promotion,form_7_type_of_trade_promotion,form_7_dip_indicate,form_7_start_date,form_7_end_date,form_7_name_of_po,form_7_amount,form_7_venue,form_7_rapid_actual_budget,form_7_name_of_beneficiary,form_7_commodity,form_7_beneficiary,form_7_sex,form_7_sector,form_7_type_of_products,form_7_name_of_buyer,form_7_cash_sales,form_7_booked_sales,form_7_under_negotiations,form_7_total_autosum,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_7_implementing_unit,form_7_title_trade_promotion,form_7_type_of_trade_promotion,form_7_dip_indicate,form_7_start_date,form_7_end_date,form_7_name_of_po,form_7_amount,form_7_venue,form_7_rapid_actual_budget,form_7_name_of_beneficiary,form_7_commodity,form_7_beneficiary,form_7_sex,form_7_sector,form_7_type_of_products,form_7_name_of_buyer,form_7_cash_sales,form_7_booked_sales,form_7_under_negotiations,form_7_total_autosum,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform9(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open9(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open9(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form9'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_9_implementing_unit = row[0]
		form_9_title_trade_promotion = row[1]
		form_9_type_of_training = row[2]
		form_9_start_date = row[3]
		form_9_end_date = row[4]
		form_9_venue = row[5]
		form_9_rapid_actual_budget = row[6]
		form_9_name_of_resource_person = row[7]
		form_9_name_of_participant_org = row[8]
		form_9_counterpart_amount = row[9]
		form_9_name_of_participant = row[10]
		form_9_sex = row[11]
		form_9_sector = row[12]
		form_9_organization = row[13]
		form_9_designation = row[14]
		form_9_pre_test1 = row[15]
		form_9_post_test1 = row[16]
		form_9_activity_output = row[17]
		form_9_pre_test2 = row[18]
		form_9_post_test2 = row[19]
		form_9_rating = row[20]
		form_9_comments = row[21]                                                                                              
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_enablers_activity ( upload_by, form_9_implementing_unit,form_9_title_trade_promotion,form_9_type_of_training,form_9_start_date,form_9_end_date,form_9_venue,form_9_rapid_actual_budget,form_9_name_of_resource_person,form_9_name_of_participant_org,form_9_counterpart_amount,form_9_name_of_participant,form_9_sex,form_9_sector,form_9_organization,form_9_designation,form_9_pre_test1,form_9_post_test1,form_9_activity_output,form_9_pre_test2,form_9_post_test2,form_9_rating,form_9_comments,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_9_implementing_unit,form_9_title_trade_promotion,form_9_type_of_training,form_9_start_date,form_9_end_date,form_9_venue,form_9_rapid_actual_budget,form_9_name_of_resource_person,form_9_name_of_participant_org,form_9_counterpart_amount,form_9_name_of_participant,form_9_sex,form_9_sector,form_9_organization,form_9_designation,form_9_pre_test1,form_9_post_test1,form_9_activity_output,form_9_pre_test2,form_9_post_test2,form_9_rating,form_9_comments,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"


def importcsvform10(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open10(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open10(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form10'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[6:]:
		upload_by = session["USER_DATA"][0]['id']
		form_10_nc_location = row [0]
		form_10_name_of_nc = row [1]
		form_10_title_of_rapid_activity = row [2]
		form_10_type_of_assistance = row [3]
		form_10_date = row [4]
		form_10_type_of_beneficiary = row [5]
		form_10_sex_male = row [6]
		form_10_sex_female = row [7]
		form_10_commodity = row [8]                                                                                           
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_negosyo_center ( upload_by, form_10_nc_location,form_10_name_of_nc,form_10_title_of_rapid_activity,form_10_type_of_assistance,form_10_date,form_10_type_of_beneficiary,form_10_sex_male,form_10_sex_female,form_10_commodity,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_10_nc_location,form_10_name_of_nc,form_10_title_of_rapid_activity,form_10_type_of_assistance,form_10_date,form_10_type_of_beneficiary,form_10_sex_male,form_10_sex_female,form_10_commodity,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"

	

def importcsvform11(request):
	from datetime import date, datetime
	today = str(datetime.today()).replace("-", "").replace(" ", "").replace(":", "").replace(".", "")
	uploader = session["USER_DATA"][0]["id"]
	if request.method == "POST":
		try:
			files = request.files
			for file in files:
				f = files[file]
				global UPLOAD_NAME
				UPLOAD_NAME = str(uploader) + "#" + str(today) + "#" + secure_filename(f.filename)
				f.save(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
				excel_upload_open11(os.path.join(c.RECORDS + "/objects/spreadsheets_dcf/queued/", UPLOAD_NAME))
		except IndexError:
			flash(f"Invalid file template!", "error")
			
	return redirect("/dcfspreadsheet")

def excel_upload_open11(path):  
	book = xlrd.open_workbook(path)
	sheet = book.sheet_by_index(0)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	header = data[4]
	
	print(sheet.name)
	if(sheet.name !='form11'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_11_dip_alignment = row [0]
		form_11_activity_title = row [1]
		form_11_name_of_beneficiary = row [2]
		form_11_industry_cluster = row [3]
		form_11_msme_regional = row [4]
		form_11_msme_province = row [5]
		form_11_male = row [6]
		form_11_female = row [7]
		form_11_pwd = row [8]
		form_11_youth = row [9]
		form_11_ip = row [10]
		form_11_sc = row [11]
		form_11_date_submitted = row [12]
		form_11_date_approved = row [13]
		form_11_name_of_fsp = row [14]
		form_11_location_address = row [15]
		form_11_amount_of_equity = row [16]
		form_11_date_released = row [17]                                                                                         
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_access_financing ( upload_by, form_11_dip_alignment,form_11_activity_title,form_11_name_of_beneficiary,form_11_industry_cluster,form_11_msme_regional,form_11_msme_province,form_11_male,form_11_female,form_11_pwd,form_11_youth,form_11_ip,form_11_sc,form_11_date_submitted,form_11_date_approved,form_11_name_of_fsp,form_11_location_address,form_11_amount_of_equity,form_11_date_released,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_11_dip_alignment,form_11_activity_title,form_11_name_of_beneficiary,form_11_industry_cluster,form_11_msme_regional,form_11_msme_province,form_11_male,form_11_female,form_11_pwd,form_11_youth,form_11_ip,form_11_sc,form_11_date_submitted,form_11_date_approved,form_11_name_of_fsp,form_11_location_address,form_11_amount_of_equity,form_11_date_released,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

	if(insert["response"]=="error"):
		flash(f"An error occured!", "error")
		print(str(insert))
	else:
		flash(f"The file was imported successfully!", "success")
	return "done"
