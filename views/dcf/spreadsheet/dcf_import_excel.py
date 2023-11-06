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
	print("tafdagfefgrhgragharghahu")
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
	print("tafdagfefgrhgragharghahu")
	print(sheet.name)
	print(str(sheet.name) !='form3')
	if(str(sheet.name) !='form3'):
		print("Invalid file template!")
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[4:]:
		upload_by = session["USER_DATA"][0]['id']
		form_3_types_of_bdsp = row[3]
		form_3_contact_person = row[4]
		form_3_sex = row[6]
		form_3_office_addr = row[7]
		form_3_email = row[8]
		form_3_breif_description = row[10]
		phone = row[9]
		form_3_choices = row[11]
		form_3_preferred_region = row[12]
		form_3_preferred_province = row[13]
		form_3_name = row[14]
		form_3_education = row[15]
		form_3_expertise = row[16]
		form_3_prior_rapid_engagements = row[17]
		form_3_date_registered = row[19]
		form_3_rapid_implementing_unit = row[20]
		form_3_nature_engagements = row[21]
		form_3_suppliers_evaluation = row[22]
		form_3_other_engagement_outside_rapid = row[23]
		form_3_lecture_training_seminar = row[24]
		form_3_training_materials = row[25]
		form_3_organize_pool = "row[26]"
		form_3_demand_basis = "row[27]"
		form_3_extension_service_facilitation = "row[28]"
		form_3_philgeps_registered = "row[29]"                                                                                                          
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
	print("tafdagfefgrhgragharghahu")
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

