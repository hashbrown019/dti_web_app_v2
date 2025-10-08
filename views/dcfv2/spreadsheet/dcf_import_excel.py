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
	for row in data[5:]:
		upload_by = session["USER_DATA"][0]['id']
		form_2_name_dip = row[0]
		form_2_rcus = row[1]                                                                       
		form_2_pcu = row[2]                                                                                                     
		form_2_commodity = row[3]
		form_2_types_of_agreements = row[4]
		form_2_types_of_market = row[5]
		form_2_dip_alignment = row[6]
		form_2_name_owner_manager = row[7]
		form_2_sex_owner_manager = row[8]
		form_2_sector_owner_manager = row[9]
		form_2_business_owner_manager = row[10]
		form_2_partner_fo_engaged = row[11]
		form_2_chairperson_manager = row[12]
		form_2_sex_chairperson_manager = row[13]
		form_2_sector_chairperson_manager = row[14]
		form_2_office_address_province = row[15]
		form_2_total_number_fo = row[16]
		form_2_male = row[17]
		form_2_female = row[18]
		form_2_pwde = row[19]
		form_2_youth = row[20]
		form_2_ip = row[21]
		form_2_sc = row[22]
		form_2_address_of_fo_members = row[23]
		form_2_hectares_covered = row[24]
		form_2_cpa_date_signing = row[25]
		form_2_cpa_date_expiration = row[26]
		form_2_days_remaining = row[27]
		form_2_date_renewed = row[28]
		form_2_notable_cpa_incentives = row[29]
		form_2_activity_agreements = row[30]
		form_2_date_conducted = row[31]
		form_2_remarks_status = row[32]
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_implementing_unit ( upload_by,form_2_name_dip,form_2_rcus,form_2_pcu,form_2_commodity,form_2_types_of_agreements,form_2_types_of_market,form_2_dip_alignment,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_activity_agreements,form_2_date_conducted,form_2_remarks_status,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by,form_2_name_dip,form_2_rcus,form_2_pcu,form_2_commodity,form_2_types_of_agreements,form_2_types_of_market,form_2_dip_alignment,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_activity_agreements,form_2_date_conducted,form_2_remarks_status,filename))
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
		form_3_orgfirm = row[0]
		form_3_types_of_bdsp = row[1]
		form_3_contact_person = row[2]
		form_3_sex = row[3]
		form_3_office_addr = row[4]
		form_3_email = row[5]
		form_3_breif_description = row[6]
		phone = row[7]
		form_3_choices = row[8]
		form_3_preferred_region = row[9]
		form_3_preferred_province = row[10]
		form_3_name = row[11]
		form_3_education = row[12]
		form_3_expertise = row[13]
		form_3_prior_rapid_engagements = row[14]
		form_3_date_registered = row[15]
		form_3_rapid_implementing_unit = row[16]
		form_3_nature_engagements = row[17]
		form_3_suppliers_evaluation = row[18]
		form_3_other_engagement_outside_rapid = row[19]
		form_3_lecture_training_seminar = row[20]
		form_3_training_materials = row[21]
		form_3_organize_pool = "row[22]"
		form_3_demand_basis = "row[23]"
		form_3_extension_service_facilitation = "row[24]"
		form_3_philgeps_registered = "row[25]"                                                                                                          
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_bdsp_reg ( upload_by,form_3_orgfirm,form_3_types_of_bdsp,form_3_contact_person,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by,form_3_orgfirm,form_3_types_of_bdsp,form_3_contact_person,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered,filename))
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
    
    if sheet.name != 'form4':
        flash(f"Invalid file template!", "error")
        return "done:Sheet Error"

    def safe_int(val):
        try:
            if val is None:
                return ''
            return int(float(val))
        except (ValueError, TypeError):
            return 0

    for row in data[5:]:
        upload_by = session["USER_DATA"][0]['id']
        cbb_implementing_unit = row[0]
        cbb_activity_title = row[1]
        cbb_types_of_training = row[2]
        cbb_topic_of_training = row[3]
        cbb_dip_approved_alignment = row[4]
        cbb_name_of_dip = row[5]
        cbb_date_start = row[6]
        cbb_date_end = row[7]
        cbb_commodity = row[8]
        cbb_venue = row[9]
        cbb_name_of_resource_person = row[10]
        cbb_rapid_actual_budget = row[11]
        cbb_dip_capbuild_activities_NPO = row[12]
        cbb_dip_capbuild_activities_CA = row[13]
        cbb_total_number_per_gender_male = safe_int(row[14])
        cbb_total_number_per_gender_female = safe_int(row[15])
        cbb_total_number_per_gender_total = safe_int(row[16])
        cbb_total_number_per_sector_pwd = safe_int(row[17])
        cbb_total_number_per_sector_youth = safe_int(row[18])
        cbb_total_number_per_sector_ip = safe_int(row[19])
        cbb_total_number_per_sector_sc = safe_int(row[20])
        cbb_total_number_per_sector_total = safe_int(row[21])
        cbb_male_ip = safe_int(row[22])
        cbb_female_ip = safe_int(row[23])
        cbb_male_youth = safe_int(row[24])
        cbb_female_youth = safe_int(row[25])
        cbb_male_pwd = safe_int(row[26])
        cbb_female_pwd = safe_int(row[27])
        cbb_male_sc = safe_int(row[28])
        cbb_female_sc = safe_int(row[29])
        cbb_male_total = safe_int(row[30])
        cbb_female_total = safe_int(row[31])
        cbb_results_of_activity_pre_test = row[32]
        cbb_results_of_activity_post_test = row[33]
        cbb_client_feedback_survey_rating = row[34]
        cbb_client_feedback_survey_comments_AOI = row[35]
        filename = UPLOAD_NAME

        querycsv = ("INSERT INTO dcf_capacity_building ( upload_by, cbb_implementing_unit,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_male_ip,cbb_female_ip,cbb_male_youth,cbb_female_youth,cbb_male_pwd,cbb_female_pwd,cbb_male_sc,cbb_female_sc,cbb_male_total,cbb_female_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
        format(upload_by, cbb_implementing_unit,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_male_ip,cbb_female_ip,cbb_male_youth,cbb_female_youth,cbb_male_pwd,cbb_female_pwd,cbb_male_sc,cbb_female_sc,cbb_male_total,cbb_female_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI,filename))


        insert = db.do(querycsv)
        print(insert)
        print("===============================================")

        if insert["response"] == "error":
            flash(f"An error occurred!", "error")
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
		mgit_commodity = row[2]
		mgit_type_of_beneficiary = row[3]
		mgit_msme_recipient = row[4]
		mgit_status_of_mga = row[5]
		mgit_date_signed = row[6]
		mgit_total_amount = row[7]
		mgit_type_of_investment = row[8]
		mgit_total_num_target_of_fo_expansion = row[9]
		mgit_total_num_target_members_expansion = row[10]
		mgit_total_amount_mgrr = row[11]
		mgit_status_mgrr = row[12]
		mgit_date = row[13]
		mgit_amount_release = row[14]
		mgit_remaining_balance = row[15]
		mgit_target_total_amount_of_has = row[16]
		mgit_inclusive_timeline_implementation_start = row[17]
		mgit_inclusive_timeline_implementation_end = row[18]
		mgit_time_elapse = row[19]
		mgit_total_num_target_of_fo_rehab = row[20]
		mgit_total_num_target_members_rehab = row[21]
		mgit_total_amount_of_mooe = row[22]
		mgit_total_amount_of_release = row[23]
		mgit_date_released = row[24]
		mgit_remaining_balance_rehab = row[25]
		mgit_total_amount_of_members_received_rehab = row[26]
		mgit_target_total_amount_of_has_for_rehabilitation = row[27]
		mgit_inclusive_timeline_implementation_start1 = row[28]
		mgit_inclusive_timeline_implementation_end1 = row[29]
		mgit_time_elapse1 = row[30]
		mgit_total_amount_of_mga_signed = row[31]
		mgit_type_of_investment_prod = row[32]
		mgit_productive_investment_requested = row[33]
		mgit_total_amount_in_mgrr = row[34]
		mgit_status_of_mgrr_prodInv = row[35]
		mgit_date_productive_investment = row[36]
		mgit_mgrr_amount_released_php = row[37]
		mgit_total_actual_counterpart = row[38]
		mgit_source_of_funds = row[39]
		mgit_name_of_source = row[40]
		mgit_amount_released_in_php = row[41]
		mgit_remaining_balance_prod = row[42]
		mgit_timeline_start_prod = row[43]
		mgit_timeline_end_prod = row[44]
		mgit_time_elapse_prod = row[45]
		filename = UPLOAD_NAME

		querycsv = ("INSERT INTO dcf_matching_grant (upload_by, mgit_implementing_unit, mgit_name_of_dip, mgit_commodity, mgit_type_of_beneficiary, mgit_msme_recipient, mgit_status_of_mga, mgit_date_signed, mgit_total_amount, mgit_type_of_investment, mgit_total_num_target_of_fo_expansion, mgit_total_num_target_members_expansion, mgit_total_amount_mgrr, mgit_status_mgrr, mgit_date, mgit_amount_release, mgit_remaining_balance, mgit_target_total_amount_of_has, mgit_inclusive_timeline_implementation_start, mgit_inclusive_timeline_implementation_end, mgit_time_elapse, mgit_total_num_target_of_fo_rehab, mgit_total_num_target_members_rehab, mgit_total_amount_of_mooe, mgit_total_amount_of_release, mgit_date_released, mgit_remaining_balance_rehab, mgit_total_amount_of_members_received_rehab, mgit_target_total_amount_of_has_for_rehabilitation, mgit_inclusive_timeline_implementation_start1, mgit_inclusive_timeline_implementation_end1, mgit_time_elapse1, mgit_total_amount_of_mga_signed, mgit_type_of_investment_prod, mgit_productive_investment_requested, mgit_total_amount_in_mgrr, mgit_status_of_mgrr_prodInv, mgit_date_productive_investment, mgit_mgrr_amount_released_php, mgit_total_actual_counterpart, mgit_source_of_fund, mgit_name_of_source, mgit_amount_released_in_php, mgit_remaining_balance_prod, mgit_timeline_start_prod, mgit_timeline_end_prod, mgit_time_elapse_prod, filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
		format(upload_by,mgit_implementing_unit,mgit_name_of_dip,mgit_commodity,mgit_type_of_beneficiary,mgit_msme_recipient,mgit_status_of_mga,mgit_date_signed,mgit_total_amount,mgit_type_of_investment,
		 mgit_total_num_target_of_fo_expansion,mgit_total_num_target_members_expansion,mgit_total_amount_mgrr,mgit_status_mgrr,mgit_date,mgit_amount_release,mgit_remaining_balance,
		 mgit_target_total_amount_of_has,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_num_target_of_fo_rehab,mgit_total_num_target_members_rehab,
		 mgit_total_amount_of_mooe,mgit_total_amount_of_release,mgit_date_released,mgit_remaining_balance_rehab,mgit_total_amount_of_members_received_rehab,mgit_target_total_amount_of_has_for_rehabilitation,
		 mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_total_amount_of_mga_signed,mgit_type_of_investment_prod,mgit_productive_investment_requested,
		 mgit_total_amount_in_mgrr,mgit_status_of_mgrr_prodInv,mgit_date_productive_investment,mgit_mgrr_amount_released_php,mgit_total_actual_counterpart,mgit_source_of_funds,mgit_name_of_source,mgit_amount_released_in_php,
		 mgit_remaining_balance_prod,mgit_timeline_start_prod,mgit_timeline_end_prod,mgit_time_elapse_prod,filename))
		insert=db.do(querycsv)
		print(insert)
		print("===============================================")

		if insert["response"] == "error":
			flash(f"An error occurred!", "error")
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
    from datetime import datetime
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
            flash("Invalid file template!", "error")

    return redirect("/dcfspreadsheet")


def excel_upload_open11(path):
    book = xlrd.open_workbook(path)

    # Normalize sheet names (case-insensitive, strip spaces)
    sheet_names = [s.strip().lower() for s in book.sheet_names()]
    expected_sheets = ["farmer profile", "fos-msmes profile"]

    # Debug: show detected sheets
    print("Detected sheets:", sheet_names)

    # Ensure both sheets exist
    for expected in expected_sheets:
        if expected not in sheet_names:
            flash(f"Invalid file template! Missing sheet: {expected}", "error")
            return "done:Sheet Error"

    upload_by = session["USER_DATA"][0]["id"]
    filename = UPLOAD_NAME
    total_inserted = 0

    # ---------------- Farmer Profile ----------------
    sheet_farmer = book.sheet_by_name([s for s in book.sheet_names() if s.strip().lower() == "farmer profile"][0])
    data_farmer = [[sheet_farmer.cell_value(r, c) for c in range(sheet_farmer.ncols)] for r in range(sheet_farmer.nrows)]

    header_farmer = data_farmer[2]  # headers are on row 3
    for row in data_farmer[3:]:
        if not any(str(cell).strip() for cell in row):
            continue  # skip empty rows

        # Pad/trim row to 53 fields
        row = (row + [""] * 53)[:53]

        (form_11_farmer_region, form_11_farmer_pcu, form_11_farmer_dip_name, form_11_farmer_commodity, form_11_farmer_type_of_enterprise,
         form_11_farmer_name_of_enterprise, form_11_farmer_location, form_11_farmer_beneficiaries_name,
         form_11_farmer_beneficiaries_male, form_11_farmer_beneficiaries_female, form_11_farmer_beneficiaries_pwd,
         form_11_farmer_beneficiaries_ip, form_11_farmer_beneficiaries_youth, form_11_farmer_beneficiaries_sc,
         form_11_farmer_loan_fsp, form_11_farmer_loan_type, form_11_farmer_loan_amount, form_11_farmer_loan_purpose,
         form_11_farmer_total_loan_amount, form_11_farmer_savings_fsp, form_11_farmer_savings_type,
         form_11_farmer_savings_amount, form_11_farmer_insurance_fsp, form_11_farmer_insurance_type,
         form_11_farmer_insurance_type_other, form_11_farmer_insurance_amount, form_11_farmer_creditguarantee,
         form_11_farmer_creditguarantee_amount, form_11_farmer_paidupcapital, form_11_farmer_with_puc,
         form_11_farmer_paidupcapital_amount, form_11_farmer_inkind_fsp, form_11_farmer_inkind_type,
         form_11_farmer_inkind_with, form_11_farmer_inkind_input, form_11_farmer_cashgrant_fsp,
         form_11_farmer_cashgrant_type, form_11_farmer_cashgrant_with, form_11_farmer_cashgrant_amount,
         form_11_farmer_cashforwork_fsp, form_11_farmer_cashforwork_type, form_11_farmer_cashforwork_with,
         form_11_farmer_cashforwork_amount, form_11_farmer_mortuary_fsp, form_11_farmer_mortuary_type,
         form_11_farmer_mortuary_with, form_11_farmer_mortuary_amount, form_11_farmer_digital_fsp,
         form_11_farmer_digital_type, form_11_farmer_digital_with, form_11_farmer_digital_amount,
         form_11_farmer_rapid_mg, form_11_farmer_rapid_type) = row

        querycsv = f"""
        INSERT INTO dcf_access_financing (
            upload_by, form_11_farmer_region, form_11_farmer_pcu, form_11_farmer_dip_name, form_11_farmer_commodity, form_11_farmer_type_of_enterprise,
            form_11_farmer_name_of_enterprise, form_11_farmer_location, form_11_farmer_beneficiaries_name,
            form_11_farmer_beneficiaries_male, form_11_farmer_beneficiaries_female, form_11_farmer_beneficiaries_pwd,
            form_11_farmer_beneficiaries_ip, form_11_farmer_beneficiaries_youth, form_11_farmer_beneficiaries_sc,
            form_11_farmer_loan_fsp, form_11_farmer_loan_type, form_11_farmer_loan_amount, form_11_farmer_loan_purpose,
            form_11_farmer_total_loan_amount, form_11_farmer_savings_fsp, form_11_farmer_savings_type,
            form_11_farmer_savings_amount, form_11_farmer_insurance_fsp, form_11_farmer_insurance_type,
            form_11_farmer_insurance_type_other, form_11_farmer_insurance_amount, form_11_farmer_creditguarantee,
            form_11_farmer_creditguarantee_amount, form_11_farmer_paidupcapital, form_11_farmer_with_puc,
            form_11_farmer_paidupcapital_amount, form_11_farmer_inkind_fsp, form_11_farmer_inkind_type,
            form_11_farmer_inkind_with, form_11_farmer_inkind_input, form_11_farmer_cashgrant_fsp,
            form_11_farmer_cashgrant_type, form_11_farmer_cashgrant_with, form_11_farmer_cashgrant_amount,
            form_11_farmer_cashforwork_fsp, form_11_farmer_cashforwork_type, form_11_farmer_cashforwork_with,
            form_11_farmer_cashforwork_amount, form_11_farmer_mortuary_fsp, form_11_farmer_mortuary_type,
            form_11_farmer_mortuary_with, form_11_farmer_mortuary_amount, form_11_farmer_digital_fsp,
            form_11_farmer_digital_type, form_11_farmer_digital_with, form_11_farmer_digital_amount,
            form_11_farmer_rapid_mg, form_11_farmer_rapid_type, filename
        ) VALUES (
            '{upload_by}', '{form_11_farmer_region}', '{form_11_farmer_pcu}', '{form_11_farmer_dip_name}', '{form_11_farmer_commodity}', '{form_11_farmer_type_of_enterprise}',
            '{form_11_farmer_name_of_enterprise}', '{form_11_farmer_location}', '{form_11_farmer_beneficiaries_name}',
            '{form_11_farmer_beneficiaries_male}', '{form_11_farmer_beneficiaries_female}', '{form_11_farmer_beneficiaries_pwd}',
            '{form_11_farmer_beneficiaries_ip}', '{form_11_farmer_beneficiaries_youth}', '{form_11_farmer_beneficiaries_sc}',
            '{form_11_farmer_loan_fsp}', '{form_11_farmer_loan_type}', '{form_11_farmer_loan_amount}', '{form_11_farmer_loan_purpose}',
            '{form_11_farmer_total_loan_amount}', '{form_11_farmer_savings_fsp}', '{form_11_farmer_savings_type}',
            '{form_11_farmer_savings_amount}', '{form_11_farmer_insurance_fsp}', '{form_11_farmer_insurance_type}',
            '{form_11_farmer_insurance_type_other}', '{form_11_farmer_insurance_amount}', '{form_11_farmer_creditguarantee}',
            '{form_11_farmer_creditguarantee_amount}', '{form_11_farmer_paidupcapital}', '{form_11_farmer_with_puc}',
            '{form_11_farmer_paidupcapital_amount}', '{form_11_farmer_inkind_fsp}', '{form_11_farmer_inkind_type}',
            '{form_11_farmer_inkind_with}', '{form_11_farmer_inkind_input}', '{form_11_farmer_cashgrant_fsp}',
            '{form_11_farmer_cashgrant_type}', '{form_11_farmer_cashgrant_with}', '{form_11_farmer_cashgrant_amount}',
            '{form_11_farmer_cashforwork_fsp}', '{form_11_farmer_cashforwork_type}', '{form_11_farmer_cashforwork_with}',
            '{form_11_farmer_cashforwork_amount}', '{form_11_farmer_mortuary_fsp}', '{form_11_farmer_mortuary_type}',
            '{form_11_farmer_mortuary_with}', '{form_11_farmer_mortuary_amount}', '{form_11_farmer_digital_fsp}',
            '{form_11_farmer_digital_type}', '{form_11_farmer_digital_with}', '{form_11_farmer_digital_amount}',
            '{form_11_farmer_rapid_mg}', '{form_11_farmer_rapid_type}', '{filename}'
        )
        """
        insert = db.do(querycsv)
        total_inserted += 1

    # ---------------- FO/MSMEs Profile ----------------
    sheet_fo = book.sheet_by_name([s for s in book.sheet_names() if s.strip().lower() == "fos-msmes profile"][0])
    data_fo = [[sheet_fo.cell_value(r, c) for c in range(sheet_fo.ncols)] for r in range(sheet_fo.nrows)]

    header_fo = data_fo[2]
    for row in data_fo[3:]:
        if not any(str(cell).strip() for cell in row):
            continue  # skip empty rows

        # Pad/trim row to 40 fields
        row = (row + [""] * 40)[:40]

        (form_11_fo_msme_regional, form_11_fo_msme_pcu, form_11_fo_dip_name, form_11_fo_commodity, form_11_fo_type_of_enterprise,
         form_11_fo_name_of_beneficiary, form_11_fo_msme_province, form_11_fo_asset_size,
         form_11_fo_male, form_11_fo_female, form_11_fo_pwd, form_11_fo_youth, form_11_fo_ip, form_11_fo_sc,
         form_11_fo_registration_type, form_11_others_specify, form_11_fo_lending_members,
         form_11_fo_loan_fsp, form_11_fo_loan_type, form_11_fo_loan_amount, form_11_fo_loan_purpose,
         form_11_fo_total_loan_amount, form_11_fo_equity_availed, form_11_fo_equity_amount, form_11_fo_equity_date,
         form_11_fo_savings_fsp, form_11_fo_savings_amount, form_11_fo_insurance_fsp, form_11_fo_insurance_amount,
         form_11_fo_credit_guarantee, form_11_fo_credit_guarantee_amount, form_11_fo_inkind_fsp, form_11_fo_inkind_grant,
         form_11_fo_cashgrant_fsp, form_11_fo_cashgrant_amount, form_11_fo_digital_fsp, form_11_fo_digital_yes,
         form_11_fo_digital_amount, form_11_fo_rapid_mg, form_11_fo_rapid_amount) = row

        querycsv = f"""
        INSERT INTO dcf_access_financing (
            upload_by, form_11_fo_msme_regional, form_11_fo_msme_pcu, form_11_fo_dip_name, form_11_fo_commodity, form_11_fo_type_of_enterprise,
            form_11_fo_name_of_beneficiary, form_11_fo_msme_province, form_11_fo_asset_size,
            form_11_fo_male, form_11_fo_female, form_11_fo_pwd, form_11_fo_youth, form_11_fo_ip, form_11_fo_sc,
            form_11_fo_registration_type, form_11_others_specify, form_11_fo_lending_members,
            form_11_fo_loan_fsp, form_11_fo_loan_type, form_11_fo_loan_amount, form_11_fo_loan_purpose,
            form_11_fo_total_loan_amount, form_11_fo_equity_availed, form_11_fo_equity_amount, form_11_fo_equity_date,
            form_11_fo_savings_fsp, form_11_fo_savings_amount, form_11_fo_insurance_fsp, form_11_fo_insurance_amount,
            form_11_fo_credit_guarantee, form_11_fo_credit_guarantee_amount, form_11_fo_inkind_fsp, form_11_fo_inkind_grant,
            form_11_fo_cashgrant_fsp, form_11_fo_cashgrant_amount, form_11_fo_digital_fsp, form_11_fo_digital_yes,
            form_11_fo_digital_amount, form_11_fo_rapid_mg, form_11_fo_rapid_amount, filename
        ) VALUES (
            '{upload_by}', '{form_11_fo_msme_regional}', '{form_11_fo_msme_pcu}', '{form_11_fo_dip_name}', '{form_11_fo_commodity}', '{form_11_fo_type_of_enterprise}',
            '{form_11_fo_name_of_beneficiary}', '{form_11_fo_msme_province}', '{form_11_fo_asset_size}',
            '{form_11_fo_male}', '{form_11_fo_female}', '{form_11_fo_pwd}', '{form_11_fo_youth}', '{form_11_fo_ip}', '{form_11_fo_sc}',
            '{form_11_fo_registration_type}', '{form_11_others_specify}', '{form_11_fo_lending_members}',
            '{form_11_fo_loan_fsp}', '{form_11_fo_loan_type}', '{form_11_fo_loan_amount}', '{form_11_fo_loan_purpose}',
            '{form_11_fo_total_loan_amount}', '{form_11_fo_equity_availed}', '{form_11_fo_equity_amount}', '{form_11_fo_equity_date}',
            '{form_11_fo_savings_fsp}', '{form_11_fo_savings_amount}', '{form_11_fo_insurance_fsp}', '{form_11_fo_insurance_amount}',
            '{form_11_fo_credit_guarantee}', '{form_11_fo_credit_guarantee_amount}', '{form_11_fo_inkind_fsp}', '{form_11_fo_inkind_grant}',
            '{form_11_fo_cashgrant_fsp}', '{form_11_fo_cashgrant_amount}', '{form_11_fo_digital_fsp}', '{form_11_fo_digital_yes}',
            '{form_11_fo_digital_amount}', '{form_11_fo_rapid_mg}', '{form_11_fo_rapid_amount}', '{filename}'
        )
        """
        insert = db.do(querycsv)
        total_inserted += 1

    if total_inserted > 0:
        flash(f"The file was imported successfully! {total_inserted} rows inserted.", "success")
    else:
        flash("The file contained no valid data.", "error")

    return "done"