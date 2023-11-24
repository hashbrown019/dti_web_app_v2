from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, Response,send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
from modules.Req_Brorn_util import string_websafe
import Configurations as c
import os, random, json, shutil, base64, sys, warnings, csv, xlrd
from controllers.outbound import outbound as outb
from controllers.inbound import inbound as inb
from controllers.inbound import data_cleaning as  d_c
from werkzeug.utils import secure_filename
from controllers.engine_excel_to_sql import form_excel_a_handler
import os, random, json
import pandas as pd
import openpyxl
from datetime import datetime
import pandas as pd
from tqdm import tqdm

app = Blueprint("doofen",__name__,template_folder='pages')

_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)

outbound = outb(app,rapid_mysql,session)
inbound = inb(app,rapid_mysql,session)
data_clean = d_c(app,rapid_mysql,session)
# app = Flask(__name__)
	
@app.route("/formb")
@c.login_auth_web()
def index():
	return redirect("/formb/dashboard")
	
@app.route("/formb/dashboard")
@c.login_auth_web()
def dashboard():
	return dashboardv2()
	# return render_template('index.html',USER_DATA=session["USER_DATA"][0],num_fo_sex=get_num_fo_sex())

@app.route("/formb/dashboardv2")
@c.login_auth_web()
def dashboardv2():
	return render_template('dashboard_main.html',USER_DATA=session["USER_DATA"][0],num_fo_sex=get_num_fo_sex())


@app.route("/formb/save_form",methods=["POST","GET"])
@c.login_auth_web()
def save_form():
	form_data = request.form
	col = "";val = "";args = ""

	is_exist = len(rapid_mysql.select("SELECT * FROM `form_b` WHERE `id` ='{}' ;".format(request.form['id'])))
	if(is_exist==0):
		print("Adding")
		for data_ in form_data:
			col += ",`{}`".format(data_)
			val += ",'{}'".format(form_data[data_])
		sql = "INSERT INTO `form_b` (`uploaded_by`,{}) VALUES ('{}',{})".format(col[1:], session["USER_DATA"][0]["id"], val[1:])
	else:
		print("Editing")
		for data_ in form_data:
			args += ",`{}`='{}'".format(data_,form_data[data_])
		sql = "UPDATE `form_b` SET {} WHERE `id`='{}';".format(args[1:],request.form['id'])
		pass

	# print(sql)
	last_row_id ="None"
	status = "Unfinished"
	msg = "Unfinished"
	try:
		last_row_id = rapid_mysql.do(sql)
		status = "success"
		msg = "Data was added to the database"
	except Exception as e:
		status = "failed"
		msg = "[{}]".format(e)
		last_row_id ="None"
	return jsonify({"status":status,"msg":msg,"id":last_row_id})
	# return jsonify([last_row_id])



@app.route("/formb/get_list_fo",methods=["POST","GET"])
@c.login_auth_web()
def get_list_fo():
	sql_form = '''
	SELECT 
		`form_b`.`id` as 'db_id',
		`form_b`.`organization_registered_name`,
		`form_b`.`office_business_adrress`,
		`form_b`.`types_of_organization`,
		`form_b`.`registering_agencies`,
		`users`.`name` as 'inputed_by',
		`users`.`rcu` as 'rcu'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	ORDER BY `form_b`.`id` DESC;'''.format(Filter.position_data_filter())
	resp = rapid_mysql.select(sql_form,False)
	return resp

@app.route("/formb/get_num_fo_sex",methods=["POST","GET"])
@c.login_auth_web()
def get_num_fo_sex():
	sql_form_male = '''
	SELECT 
		COUNT(`form_b`.`respondents_gender_male`) as 'male'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	AND `form_b`.`respondents_gender_male`='true'
	AND `respondents_designation_in_the_organization` in ('Chairperson','Chairwoman','Coop Chairperson','General Manager','Manager','President/Chairman')
	 ;'''.format(Filter.position_data_filter())
	male = rapid_mysql.select(sql_form_male,True)[0]['male']

	sql_form_female = '''
	SELECT 
		COUNT(`form_b`.`respondents_gender_female`) as 'female'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	AND `form_b`.`respondents_gender_female`='true'
	AND `respondents_designation_in_the_organization` in ('Chairperson','Chairwoman','Coop Chairperson','General Manager','Manager','President/Chairman')
	 ;'''.format(Filter.position_data_filter())
	female = rapid_mysql.select(sql_form_female,True)[0]['female']

	sql_form_female_board = '''
	SELECT SUM(`fo_board_female`) as 'total_female_board'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	 ;'''.format(Filter.position_data_filter())
	board_female = rapid_mysql.select(sql_form_female_board,True)[0]['total_female_board']

	sql_form_male_board = '''
	SELECT SUM(`fo_board_male`) as 'total_male_board'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	 ;'''.format(Filter.position_data_filter())
	board_male = rapid_mysql.select(sql_form_male_board,True)[0]['total_male_board']

	sql_form_female_mngmnt = '''
	SELECT SUM(`fo_management_female_checkbox`) as 'total_female_mngmnt'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	 ;'''.format(Filter.position_data_filter())
	mngmt_female = rapid_mysql.select(sql_form_female_mngmnt,True)[0]['total_female_mngmnt']


	sql_form_male_mngmnt = '''
	SELECT SUM(`fo_management_male_checkbox`) as 'total_male_mngmnt'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	 ;'''.format(Filter.position_data_filter())
	mngmt_male = rapid_mysql.select(sql_form_male_mngmnt,True)[0]['total_male_mngmnt']

	res = {
		"male":male,
		"female":female,
		'total_female_board':board_female,
		'total_male_board':board_male,
		'mngmt_male':mngmt_male,
		'mngmt_female':mngmt_female
	}


	return res


@app.route("/formb/get_list_fo_full",methods=["POST","GET"])
@c.login_auth_web()
def get_list_fo_full():
	sql_form = '''
	SELECT 
		`form_b`.`id` as 'db_id',
		`form_b`.*,
		`users`.`name` as 'inputed_by',
		`users`.`rcu` as 'rcu'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} ;'''.format(Filter.position_data_filter())
	resp = rapid_mysql.select(sql_form)
	
	file_name_exported = create_excel(resp,c.RECORDS+"objects/spreadsheets_b/exported/","formb")
	return send_file(c.RECORDS+"objects/spreadsheets_b/exported/"+file_name_exported['file_name'], as_attachment=True,download_name=file_name_exported['file_name'])
# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================
def create_excel(DATA,path,formname):
	print(" Using Dynamic Function")
	DATE_NOW = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
	USER_ID = session["USER_DATA"][0]["id"]
	# dict_= json.loads(res)
	# df_nested_list = pd.DataFrame.from_dict(DATA, orient="index")
	print(" *  Generating DATA FRAME ")
	df_nested_list = pd.json_normalize(DATA)
	# print(res[0])
	# print(df_nested_list)
	print(" *  Writing to spreadsheet ")
	FILE_NAME_EXPORTED = '{}_{}_{}.xlsx'.format(USER_ID,formname,DATE_NOW)
	__TO_DL_EXCEL = path + FILE_NAME_EXPORTED
	print(f" *  Writing path [{__TO_DL_EXCEL}]")

	writer = pd.ExcelWriter(__TO_DL_EXCEL) 
	print(" *  Saving spreadsheet. . .  ")
	df_nested_list.to_excel(writer, sheet_name='mobile_imports',index=False )
	writer.save()
	print(" *  Saving spreadsheet DOne ")
	return {"Status":"done","file_name":FILE_NAME_EXPORTED}
# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================
@app.route("/formb/get_ind_fo",methods=["POST","G ET"])
@c.login_auth_web()
def get_ind_fo():
	ids = request.form['id']
	sql_form = "SELECT * FROM `form_b` WHERE `id`={};".format(ids)
	ind = rapid_mysql.select(sql_form)
	return jsonify(ind)

@app.route("/formb/delete_item",methods=["POST","G ET"])
@c.login_auth_web()
def delete_item():
	ids = request.form['id']
	sql_form = "DELETE FROM `form_b` WHERE `id`={};".format(ids)
	ind = rapid_mysql.do(sql_form)
	return jsonify(ind)

@app.route("/formb/search_farmer_profile",methods=["POST","G ET"])
@c.login_auth_web()
def search_farmer_profile():
	search_item = request.form['search_item']
	data_m = '''
		SELECT 
			`id`,
			CONCAT(`f_name`,' ',`m_name`,' ',`l_name`) as 'fname',
		    `farmer_name` as 'complete_name',
			`farmer_code` as 'reference',
			`farmer_bday`,
			`addr_region`,
			`addr_prov`,
			`addr_city`,
			`addr_brgy`,
			`farmer_primary_crop`,
			`farmer_sex` as 'sex',
			`farmer_civil_status` as 'civil_status'
		FROM 
			`form_a_farmer_profiles` 
		WHERE 
			`f_name` LIKE '{}' OR
			`m_name` LIKE '{}' OR
			`l_name` LIKE '{}' OR
			`farmer_name` LIKE '{}';
	'''.format(search_item,search_item,search_item,search_item)

	data_ex = '''
		SELECT 
			`id`,
			 CONCAT(`frmer_prof_@_basic_Info_@_First_name`,' ',`frmer_prof_@_basic_Info_@_Middle_name`,' ',`frmer_prof_@_basic_Info_@_Last_name`) as 'fname',
			`file_name` as 'reference',
			`frmer_prof_@_basic_Info_@_birthday` as 'farmer_bday',
			`frmer_prof_@_frmer_addr_@_region` as 'addr_region',
			`frmer_prof_@_frmer_addr_@_province` as 'addr_prov',
			`frmer_prof_@_frmer_addr_@_city_municipality` as 'addr_city',
			`frmer_prof_@_frmer_addr_@_brgy` as 'addr_brgy',
			`frmer_prof_@_Farming_Basic_Info_@_primary_crop` as 'farmer_primary_crop',
			`frmer_prof_@_basic_Info_@_Sex` as 'sex',
			`frmer_prof_@_basic_Info_@_civil_status` as 'civil_status'
		FROM 
			`excel_import_form_a` 
		WHERE 
			`frmer_prof_@_basic_Info_@_First_name` LIKE '{}' OR
			`frmer_prof_@_basic_Info_@_Middle_name` LIKE '{}' OR
			`frmer_prof_@_basic_Info_@_Last_name` LIKE '{}';
	'''.format(search_item,search_item,search_item)

	ind = rapid_mysql.select(data_m) + rapid_mysql.select(data_ex)
	return jsonify(ind)


@app.route("/formb/excel_upload",methods=["POST","GET"])
@c.login_auth_web()
def excel_upload():
	today = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
	uploader = request.form['uploader']
	excel_ = request.files
	UPLOAD_NAME = "NONE"
	for excel in excel_:
		f = excel_[excel]
		UPLOAD_NAME = uploader+"#"+today+"#"+secure_filename(f.filename)
		f.save(os.path.join(c.RECORDS+"/objects/spreadsheets_b/queued/",UPLOAD_NAME ))

	# t1 = Process(target=_excel.excel_popu_individual,args=(UPLOAD_NAME,) )
	# t1.start()
	# t1.join()
	# return {"status":"success","msg":"Processing in Progress. Please Wait. Refresh page to view changes","success_files":UPLOAD_NAME}
	uploadstate = excel_popu_individual(UPLOAD_NAME)
	return uploadstate


def excel_popu_individual(_NAME_):
	msg = "Unfinished"
	status = "Unfinished"
	record_counter = 0
	# dir_path = c.RECORDS+"/objects/spreadsheets/_temp_/"
	dir_path = c.RECORDS+"/objects/spreadsheets_b/queued/"
	FROM_EXCEL_RPOFILES = {}
	# FROM_EXCEL_RPOFILES = []
	# loads_ = tqdm(os.listdir(dir_path))
	counter = 0
	# for path in loads_:os.listdir(dir_path)
	PATH__ = os.path.join(dir_path, _NAME_)
	if os.path.isfile(PATH__):
		# if (("._DELETED_FILE_" not in str(path)) or ("~$" not in str(path))):	
		file_name =  PATH__ 
		sheet =  "VC FORM B" 
		print("\n= Scanning [{}]".format(_NAME_))
		try:
			resp = readRows(file_name, sheet)
			resp__ = readRowsHeads(file_name, sheet)
			data = save_form_from_excel(resp)
			# f = open(c.RECORDS+"/temp.txt","w")
			# f.write(json.dumps(resp__))
			# f.close()
			# msg = resp
			msg = "Transaction finished. Please be patient as the data uploaded will take time to display in the list or in the dashboard."
			status = "success"
			counter = counter + 1
		except Exception as e:
			data = "none"
			msg = "[{}]".format(e)
			status = "failed"
			print(e)
		# if(counter >= 3):
		# 	break
	print(" * Done excel process")
	return {"status":status,"msg":msg,"success_files":FROM_EXCEL_RPOFILES,"data":data}

def readRows(file, s_):
	# wb = xlrd.open_workbook(file,encoding_override='utf-8')
	wb = xlrd.open_workbook(file)
	sheet = wb.sheet_by_name(s_)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	counter = 0
	return data[4:]

def readRowsHeads(file, s_):
	# wb = xlrd.open_workbook(file,encoding_override='utf-8')
	wb = xlrd.open_workbook(file)
	sheet = wb.sheet_by_name(s_)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	counter = 0
	return data[1:4]

def save_form_from_excel(data):
	val = ""
	counter = 0
	for data_ in data:
		comma = "," if(counter >0) else "";
		val += "{}('{}',".format(comma,session["USER_DATA"][0]["id"])
		counter_ = 0
		print(len(data_))
		for datum in data_:
			comma_ = "," if(counter_ >0) else "";
			val += '''{}"{}"'''.format(comma_,string_websafe.encode_websafe(datum))
			counter_ += 1
		val += ")"
		counter += 1
	val = val.replace('''\"''',"'")
	sql = '''
		INSERT INTO `form_b` (`uploaded_by`, `name_of_respondent`, `respondents_designation_in_the_organization`, `respondents_age`, `respondents_e-mail`, `respondents_mobile`, `respondents_gender_male`, `respondents_gender_female`, `organization_registered_name`, `office_business_adrress`, `gps_coordinates_lat`, `gps_coordinates_long`, `types_of_organization`, `types_of_organization_others`, `registering_agencies`, `registering_agencies_others`, `date_registered`, `total_no_of_years`, `community_level`, `municipal_level`, `provincial_level`, `regional_level`, `national_level`, `membership_to_an_apex_fo_no_checkbox`, `membership_to_an_apex_please_specify`, `membership_nat_internat_org_no_checkbox`, `membership_nat_internat_org_yes_checkbox`, `membership_nat_internat_org_specify`, `vmo_no_checkbox`, `vmo_yes_checkbox`, `vmo_please_specify`, `cacao_checkbox`, `coffee_checkbox`, `coconut_checkbox`, `pfn_checkbox`, `cacao_1`, `cacao_2`, `cacao_3`, `cacao_4`, `cacao_5`, `cacao_6`, `cacao_7`, `coffee_1`, `coffee_2`, `coffee_3`, `coffee_4`, `coffee_5`, `coffee_6`, `coffee_7`, `coconut_1`, `coconut_2`, `coconut_3`, `coconut_4`, `coconut_5`, `coconut_6`, `coconut_7`, `pfn_1`, `pfn_2`, `pfn_3`, `pfn_4`, `pfn_5`, `pfn_6`, `pfn_7`, `nfm_non_priority_1`, `nfm_non_priority_2`, `nfm_non_priority_3`, `nfm_non_priority_4`, `nfm_non_priority_5`, `nfm_non_priority_6`, `nfm_non_priority_7`, `total_seom_1`, `total_seom_2`, `total_seom_3`, `total_seom_4`, `total_seom_5`, `total_seom_6`, `total_seom_7`, `operational_capacity_building`, `operational_agricultural_advisory`, `input_supplier_checkbox`, `equipment_servicing_checkbox`, `trading_buy_sell_checkbox`, `consumer_stor_checkbox`, `processing_checkbox`, `others_ps_checkbox`, `enterprise_others_ps_checkbox_specify`, `operational_credit_checkbox`, `operational_savings_checkbox`, `operational_remittances_checkbox`, `operational_atm_checkbox`, `operational_others_ps_checkbox`, `operational_finance_others_ps_checkbox_specify`, `operational_other_services`, `operational_crop_commodity_1`, `operational_marketing_product_fomr_1`, `operatinal_volume_delivery_1`, `operational_farm_gate_price_1`, `operational_total_sale_1`, `operational_crop_commodity_2`, `operational_marketing_product_fomr_2`, `operational_volume_delivery_2`, `operational_farm_gate_price_2`, `operational_total_sale_2`, `operational_crop_commodity_3`, `operational_marketing_product_fomr_3`, `operational_volume_delivery_3`, `operational_farm_gate_price_3`, `operational_total_sale_3`, `operational_yes_checkbox_1`, `operational_no_checkbox_1`, `operational_corp_1`, `operational_ph_equipment_facility_1`, `operational_location_1`, `operational_post_product_fomr_1`, `operational_corp_2`, `operational_ph_equipment_facility_2`, `operational_location_2`, `operational_post_product_fomr_2`, `operational_corp_3`, `operational_ph_equipment_facility_3`, `operational_post_product_fomr_3`, `operational_number_of_workers_r1`, `operationalnumber_of_workers_l1`, `operational_ip_member_r1`, `operationalip_member_l1`, `operational_youth_member_r1`, `operational_youth_member_l1`, `operational_ave_of_workdays_r1`, `operational_ave_of_workdays_l1`, `operational_ave_salary_wage_1`, `operational_number_of_workers_r12`, `operationalnumber_of_workers_l2`, `operational_ip_member_r2`, `operationalip_member_l2`, `operational_youth_member_r2`, `operational_youth_member_l2`, `operational_ave_of_workdays_r2`, `operational_ave_of_workdays_l2`, `operational_ave_salary_wage_2`, `operational_number_of_workers_r3`, `operationalnumber_of_workers_l3`, `operational_ip_member_r3`, `operationalip_member_l3`, `operational_youth_member_r3`, `operational_youth_member_l3`, `operational_ave_of_workdays_r3`, `operational_ave_of_workdays_l3`, `operational_ave_salary_wage_3`, `operational_number_of_workers_r4`, `operationalnumber_of_workers_l4`, `operational_ip_member_r4`, `operationalip_member_l4`, `operational_youth_member_r4`, `operational_youth_member_l4`, `operational_ave_of_workdays_r4`, `operational_ave_of_workdays_l4`, `operational_ave_salary_wage_4`, `external_support_yes_checkbox`, `external_support_no_checkbox`, `operational_type_of_support_1`, `operational_partner_1`, `operational_type_of_support_2`, `operational_partner_2`, `operational_type_of_support_3`, `operational_partner_3`, `operational_membership_fee_checkbox`, `operational_ammount_per_checkbox`, `operational_sales_financing_checkbox`, `opertaional_grand_govermenrt_checkbox`, `operational_oders_source_checkbox`, `fo_general_assembly_annual_checkbox`, `fo_general_assembly_biannual_checkbox`, `fo_general_assembly_yes_checkbox`, `fo_general_assembly_no_checkbox`, `fo_board_male`, `fo_board_female`, `fo_board_1year_checkbox`, `fo_board_2year_checkbox`, `fo_board_3year_checkbox`, `fo_board_monhtly_checkbox`, `fo_board_biannual_checkbox`, `fo_board_quarterly_checkbox`, `fo_board_annual_checkbox`, `fo_board_yes_checkbox`, `fo_board_no_checkbox`, `fo_management_male_checkbox`, `fo_management_female_checkbox`, `election_checkbox`, `fo_management_election`, `appointment_checkbox`, `fo_management_appiontment`, `fo_good_governance_constitution_yes_checkbox`, `fo_good_governance_constitution_no_checkbox`, `fo_good_governance_collectively_yes_checkbox`, `fo_good_governance_collectively_no_checkbox`, `fo_good_governance_decisions_yes_checkbox`, `fo_good_governance_decisions_no_checkbox`, `fo_good_governance_objectives_yes_checkbox`, `fo_good_governance_objectives_no_checkbox`, `fo_good_governance_ofunctions_yes_checkbox`, `fo_good_governance_ofunctions_no_checkbox`, `fo_good_governance_systematic_yes_checkbox`, `fo_good_governance_systematic_no_checkbox`, `fo_good_gevernance_information_yes_checkbox`, `fo_good_gevernance_information_no_checkbox`, `fo_planning_action_plan_checkbox`, `fo_planning_business_plan_checkbox`, `fo_planning_none_checkbox`, `fo_planning_facilitated_activity`, `fo_planning_participated_activity`, `fo_planning_years_cover`, `fo_planning_gender_concerns_yes_checkbox`, `fo_planning_gender_concerns_no_checkbox`, `admin_business_checkbox`, `admin_issued_by1`, `admin_business_expiration_date1`, `admin_product_checkbox`, `admin_issued_by2`, `admin_product_expiration_date2`, `admin_certificate_checkbox`, `admin_issued_by3`, `admin_expiration_date_3`, `admin_license_checkbox`, `admin_issued_by4`, `admin_expiration_date_4`, `admin_product_quality_iso_certification`, `admin_product_quality_iso_issued_5`, `admin_product_quality_expiration,date_5`, `admin_gap_checkbox`, `admin_issued_by6`, `admin_expiration_date6`, `admin_organic_checkbox`, `admin_issued_by7`, `admin_expiration_date7`, `admin_halal_checkbox`, `admin_issued_by8`, `admin_expiration_date8`, `admin_other_certification`, `admin_issued_by9`, `admin_expiration_date9`, `admin_manual_yes_checkbox`, `admin_manual_no_checkbox`, `admin_list_yes_checkbox`, `admin_list_no_checkbox`, `admin_staff_yes_checkbox`, `admin_staff_no_checkbox`, `admin_organizational_yes_checkbox`, `admin_organizational_no_checkbox`, `admin_general_yes_checkbox`, `admin_general_no_checkbox`, `admin_financial_yes_checkbox`, `admin_financial_no_checkbox`, `admin_financial_management_yes_checkbox`, `admin_financial_management_no_checkbox`, `admin_bank_book_yes_checkbox`, `admin_bank_book_no_checkbox`, `admin_cash_book_yes_checkbox`, `admin_cash_book_no_checkbox`, `admin_record_keeper_yes_checkbox`, `admin_record_keeper_no_checkbox`, `admin_bank_account_yes_checkbox`, `admin_bank_account_no_checkbox`, `admin_annual_audit_yes_checkbox`, `admin_annual_audit_no_checkbox`, `admin_registered_audit_yes_checkbox`, `admin_registered_audit_no_checkbox`, `admin_choice_auditor_yes_checkbox`, `admin_choice_auditor_no_checkbox`, `admin_board_choose_yes_checkbox`, `admin_board_choose_no_checkbox`, `admin_annual_budget_yes_checkbox`, `admin_annual_budget_no_checkbox`, `admin_fmc_yes_checkbox`, `admin_fmc_no_checkbox`, `admin_software_fmc_checkbox`, `admin_fmaa_yes_checkbox`, `admin_fmma_no_checkbox`, `admin_action_plan_none_checkbox`, `admin_staff_managing_yes_checkbox`, `admin_staff_managing_no_checkbox`, `admin_technical_number`, `admin_technical_paid`, `admin_technical_specific`, `admin_non_technical_number`, `admin_none_technical_number`, `capacity_inputs_and_equipment`, `capacity_inputs_requirment_yes_checkbox`, `capacity_inputs_requirment_no_checkbox`, `capacity_identify_your_suppliers`, `capacity_trainging_yes_checkbox`, `capacity_trainin_no_checkbox`, `capacity_training_productivity_checkbox`, `capacity_training_financial_checkbox`, `capacity_training_product_development_checkbox`, `capacity_training_organizational_management_checkbox`, `capacity_organization_training_yes_checkbox`, `capacity_organization_training_no_checkbox`, `capacity_training_in_what_area`, `capacity_undertake_yes_checkbox`, `capacity_undertake_no_checkbox`, `capacity_production_level`, `capacity_markets_buyers`, `capacity_products_from_members`, `capacity_marketing_activities`, `capacity_org_storage_yes_checkbox`, `capacity_org_storage_no_checkbox`, `capacity_description_1`, `capacity_location_include_1`, `capacity_size_area_1`, `capacity_capacity_volume_1`, `capacity_storage_feeper_day_1`, `capacity_manpower_paidworkers_1`, `capacity_description_2`, `capacity_location_include_2`, `capacity_size_area_2`, `capacity_capacity_volume_2`, `capacity_storage_feeper_day_2`, `capacity_manpower_paidworkers_2`, `capacity_description_3`, `capacity_location_include_3`, `capacity_size_area_3`, `capacity_capacity_volume_3`, `capacity_storage_feeper_day_3`, `capacity_manpower_paidworkers_3`, `capacity_org_market_yes_checkbox`, `capacity_org_market_no_checkbox`, `capacity_credit_loan_yes_checkbox`, `capacity_credit_loan_no_checkbox`, `capacity_credit_short_term_checkbox`, `capacity_credit_medium_term_checkbox`, `capacity_credit_long_term_checkbox`, `capacity_facilitating_avail_receive`, `capacity_facilitating_credit_arrangment`, `capacity_facilitating_credit_used_for`, `capacity_insurance_yes_checkbox`, `capacity_facilitating_asset`, `capacity_insurance_no_checkbox`, `capacity_facilitating_no_why`, `partnership_existing_yes_checkbox`, `partnership_existing_no_checkbox`, `partnership_organization_name1`, `partnership_sector_goverment_checkbox`, `partnership_sector_ngo_checkbox`, `partnership_sector_cso_checkbox`, `partnership_sector_priave_sector_checkbox`, `partnership_sector_academe_checkbox`, `partnership_area_coordanation_checkbox`, `partnership_area_training_checkbox`, `partnership_area_financial_support_checkbox`, `partnership_area_reseacrch_checkbox`, `partnership_area_business_transactions_checkbox`, `partnership_document_moa_mou_checkbox`, `partnership_document_commercial_checkbox`, `partnership_document_ops_checkbox`, `partnership_document_1`, `partnership_period_cover_1`, `partnership_organization_name2`, `partnership_goverment1_checkbox`, `partnership_ngo1_checkbox`, `partnership_cso1_checkbox`, `partnership_priave_sector1_checkbox`, `partnership_academe1_checkbox`, `partnership_coordanation1_checkbox`, `partnership_training1_checkbox`, `partnership_financial_support1_checkbox`, `partnership_reseacrch1_checkbox`, `partnership_business_transactions1_checkbox`, `partnership_moa_mou1_checkbox`, `partnership_commercial1_checkbox`, `partnership_ops1_checkbox`, `partnership_document_others_2`, `partnership_period_cover_2`, `respondentd_signature`, `respondents_interviewed`, `partnership_signature_of_respondent_date`, `partnership_interviewed_date`, `partnership_interviewed_time_ended`, `partnership_genral_assembly`, `partnership_input_and_equipment_supply`, `partnertship_board`, `partnertship_training_and_capacity_building`, `partnertship_management_committee`, `partnertship_collecting_bulking_marketing`, `partnertship_board_good_governance`, `partnertship_storage_facilities`, `partnertship_communication`, `partnertship_processing_packaging`, `partnertship_planning`, `partnertship_market_information_system`, `partnertship_availability_of_official`, `partnertship_with_other_organizations`, `partnertship_availability_of_management_and_planning_documents`, `partnertship_maturity_level`, `partnertship_financial_management_and_annual_audit_1`, `partnertship_financial_management_and_annual_audit_2`, `partnertship_financial_management_and_annual_audit_3`, `partnertship_efficiency_and_risk_management_1`, `partnertship_efficiency_and_risk_management_2`, `partnertship_efficiency_and_risk_management_3`, `partnertship_monitoring_and_evaluation_1`, `partnertship_monitoring_and_evaluation_2`, `partnertship_monitoring_and_evaluation_3`, `partnertship_human_resources_management_1`, `partnertship_human_resources_management_2`, `partnertship_human_resources_management_3`, `partnertship_remarks`, `SOURCE`) 
		VALUES {}
	'''.format(val)
	# print(sql)
	sql = sql.replace("\n","").replace("\t","")
	status = "Unfinished"
	msg = "Unfinished"
	last_row_id = "none"
	try:
		last_row_id = rapid_mysql.do(sql)
		status = "success"
		msg = "Data was added to the database"
	except Exception as e:
		status = "failed"
		msg = "[{}]".format(e)
	# return {"status":status,"msg":msg,"id":last_row_id}
	print({"status":status,"msg":val,"id":last_row_id,"sql":sql})
	return {"status":status,"msg":val,"id":last_row_id,"sql":sql}



class Filter:
	def position_data_filter():
		_filter = "WHERE 1 "
		JOB = session["USER_DATA"][0]["job"].lower()

		if(JOB in "admin" or JOB in "super admin"):
			session["USER_DATA"][0]["office"] = "NPCO"
			_filter = "WHERE 1 "
		else:
			session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
			_filter = "WHERE  `uploaded_by` in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
		return _filter

	def strct_dic(dict_):
		new_dict_ = {};
		for data in dict_:new_dict_[data['key']] = data['total']
		return json.loads(json.dumps(new_dict_))

	def strct_clean(dict_):
		new_dict_ = {};
		for data in dict_:new_dict_[data['key']] = data['total']
		return Filter.clean(json.loads(json.dumps(new_dict_)))

	def clean(dict_):
		new_dict_ = {};
		for key in dict_:
			KEY = key.lower().replace(" ","").replace(".","").replace("/","").replace("\\","").replace("-","").replace("*","").replace(",","").replace("(","").replace(")","").replace("&","")
			if(KEY not in new_dict_):
				new_dict_[KEY] = 0
			new_dict_[KEY] = new_dict_[KEY]+dict_[key]
			
		return json.loads(json.dumps(new_dict_))



# if __name__ == "__main__":	
# 		app.run(debug=True)

