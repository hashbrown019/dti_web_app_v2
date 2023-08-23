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
	if(sheet.name !='Form1DIPdetails'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_1_rcus = row[0]                                                                       
		form_1_number_of_dips = row[1]                                                                                                     
		form_1_anchor_firm = row[3]                                                               
		form_1_size_of_anchor = row[5]                                                               
		form_1_commodity = row[6]                                                   
		form_1_scope_provinces = row[7]                                                         
		form_1_for_development = row[8]                                                   
		form_1_cn_approved = row[9]                                                                                                       
		form_1_finalized_approved = row[10]                                                  
		form_1_date_of_parallel_review = row[11]                                                     
		form_1_date_of_submission = row[12]                                                                                                  
		form_1_date_of_rtwg = row[13]                                                                                   
		form_1_date_of_npco_cursory = row[14]                                                                                      
		form_1_date_of_uploading_to_ifad = row[15]                                                                                           
		form_1_date_of_ifad_no_inssuance = row[16]                                                                                                                                             
		form_1_totalmsme = row[17]                                                                                           
		form_1_total_farmerbene = row[18]                                                                                     
		form_1_totalfo = row[19]                                                                                             
		form_1_namefo = row[20]                                                                                                                                            
		form_1_totalhectarage_cov = row[21]                                                                                                                                        
		form_1_hect_rehab = row[22]                                                   
		form_1_total_cost_rehab = row[23]                                            
		form_1_hect_exp = row[24]                                          
		form_1_cost_exp = row[25]                                                                                            
		form_1_totalcost_prodinvest = row[26]                                                                                           
		form_1_total_matching_grant = row[27]                                         
		form_1_capbuilding = row[28]                                                                                     
		form_1_supply_chain_manager = row[29]                                             
		form_1_totalproject_cost = row[30]                                                                           
		form_1_fmi = row[31]                                               
		form_1_fmi_kms = row[32]                                                                                       
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_prep_review_aprv_status ( upload_by,form_1_rcus,form_1_number_of_dips,form_1_anchor_firm,form_1_size_of_anchor,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalcost_prodinvest,form_1_total_matching_grant,form_1_capbuilding,form_1_supply_chain_manager,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by, form_1_rcus,form_1_number_of_dips,form_1_anchor_firm,form_1_size_of_anchor,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalcost_prodinvest,form_1_total_matching_grant,form_1_capbuilding,form_1_supply_chain_manager,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms,filename))
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
	if(sheet.name !='CPAs_Details_edited'):
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
	if(sheet.name !='form3'):
		flash(f"Invalid file template!", "error")
		return "done:Sheet Error"
	for row in data[3:]:
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
		 form_3_organize_pool = row[21]
		 form_3_demand_basis = row[22]
		 form_3_extension_service_facilitation = row[23]
 		 form_3_philgeps_registered = row[24]                                                                                                                             
		 filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_implementing_unit ( upload_by,form_3_types_of_bdsp,form_3_contact_person,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
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
