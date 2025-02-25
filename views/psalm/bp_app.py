from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file, jsonify
from modules.Connections import mysql
from decimal import Decimal
import pandas as pd
from tqdm import tqdm
from time import sleep

from flask_session import Session
from apis.api import user_management
from views.psalm.dashboard import display_data as displayData
from views.psalm.dashboard import filter_data as filterData
from views.psalm.formc_insert import insert_data as insertData
from views.psalm.dashboard import update_data as updateData
from views.psalm.spreadsheet import import_excel as import_csv
from views.psalm.spreadsheet import export_excel as export_csv
import Configurations as c
import xlrd
import json
from werkzeug.utils import secure_filename
import os
from modules.Req_Brorn_util import file_from_request

db = mysql(*c.DB_CRED)
db.err_page = 0
app = Blueprint("form_c",__name__,template_folder="pages")

def is_on_session(): return ('USER_DATA' in session)



	
@app.route('/formc')
def index():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("index.html")

@app.route('/acct_dis')
def acct_dis():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("acct_dis.html")

@app.route('/importcsv',methods = ['GET','POST'])
def importcsv():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	import_csv.importcsv(request)
	return redirect("/spreadsheet")

@app.route('/exportcsv',methods = ['POST'])


def exportcsv():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	if request.method == "POST":
		query= db.select('''SELECT form_c.id,
			form_c.name,
			form_c.position_firm,
			form_c.sex,
			form_c.age,
			form_c.contact_details,
			form_c.email_add,
			form_c.vc_stakeholders,
			form_c.industry_cluster,
			form_c.reg_businessname,
			form_c.business_addr,
			form_c.form_interprise,
			form_c.issued_by_business_reg,
			form_c.issued_by_product_reg,
			form_c.issued_by_cert_reg,
			form_c.issued_by_lic_op,
			form_c.issued_by_iso_cert,
			form_c.issued_by_gapgmp_cert,
			form_c.issued_by_organic,
			form_c.issued_by_halal,
			form_c.issued_by_other_cert,
			form_c.type_enterprise,
			form_c.store_capacity_organic,
			form_c.potential_organic,
			form_c.other_info_organic,
			form_c.store_capacity_synthetic,
			form_c.potential_synthetic,
			form_c.other_info_synthetic,
			form_c.store_capacity_pesticides,
			form_c.potential_pesticides,
			form_c.other_info_pesticides,
			form_c.store_capacity_herbicides,
			form_c.potential_herbicides,
			form_c.other_info_herbicides,
			form_c.store_capacity_vermicast_compost,
			form_c.potential_vermicast_compost,
			form_c.other_info_vermicast_compost,
			form_c.store_capacity_seedlings,
			form_c.potential_seedlings,
			form_c.other_info_seedlings,
			form_c.store_capacity_others_specific_products,
			form_c.potential_others_specific_products,
			form_c.other_info_others_specific_products,
			form_c.area_capacity_drying,
			form_c.potential_exp_drying,
			form_c.other_info_drying,
			form_c.area_capacity_storage,
			form_c.potential_exp_storage,
			form_c.other_info_storage,
			form_c.area_capacity_storage_hauling,
			form_c.potential_exp_storage_hauling,
			form_c.other_info_storage_hauling,
			form_c.current_capacity_semi_processing,
			form_c.potential_exp_semi_processing,
			form_c.other_info_semi_processing,
			form_c.current_capacity_final_product,
			form_c.potential_exp_final_product,
			form_c.other_info_final_product,
			form_c.volume_consolidation,
			form_c.potential_consolidation,
			form_c.other_info_consolidation,
			form_c.production_pack_label,
			form_c.potential_pack_label,
			form_c.other_info_pack_label,
			form_c.loan_portfo_micro_financing,
			form_c.potential_micro_financing,
			form_c.other_info_micro_financing,
			form_c.loan_portfo_insurance,
			form_c.potential_insurance,
			form_c.other_info_insurance,
			form_c.prodsales_product_service,
			form_c.prodsales_sales_vol,
			form_c.prodsales_unit_selling,
			form_c.prodsales_unit_measurement,
			form_c.prodsales_payment_terms,
			form_c.raw_materials,
			form_c.volume_supply,
			form_c.quality_requirement,
			form_c.unit_measurement_raw,
			form_c.distrib_point_local_cust,
			form_c.sales_vol_local_cust,
			form_c.payment_terms_local_cust,
			form_c.inhouse_num_workersmale,
			form_c.inhouse_num_workersfemale,
			form_c.inhouse_memb_ip_group,
			form_c.inhouse_ave_workdays,
			form_c.inhouse_ave_salary,
			form_c.sub_cont_num_workersmale,
			form_c.sub_cont_num_workersfemale,
			form_c.sub_cont_memb_ip_group,
			form_c.sub_cont_ave_workdays,
			form_c.sub_cont_ave_salary,
			form_c.piece_rate_num_workersmale,
			form_c.piece_rate_num_workersfemale,
			form_c.piece_rate_memb_ip_group,
			form_c.piece_rate_ave_workdays,
			form_c.piece_rate_ave_salary,
			form_c.form_interprise2,
			form_c.pricing,
			form_c.quality_raw,
			form_c.quality_final_prod,
			form_c.other_specifyc3,
			form_c.existing_comm,
			form_c.prov_supp_assis,
			form_c.business_prodc3,
			form_c.member_livelihood,
			form_c.what_cluster_industry,
			users.name as 'Uploaded by'
					FROM form_c
					INNER JOIN users ON `form_c`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))

	df_nested_list = pd.json_normalize(query)
	df = pd.DataFrame (df_nested_list)
	writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/exported_file.xlsx') 
	df.to_excel(writer, sheet_name='exported_file',index=False )
	df.columns =['ID','Name Of Respondent','Designation in the Firm','Sex','Age','Contact Details','Email Address','Stakeholder Category','Industry Cluster','Registered Business Name',' Business Address','Form of Enterprise','Administration: Business Registration','Administration: Product Registration','Administration: Certificate of Registration','Administration: License to Operate','Product Quality: ISO Certification','Product Quality: GAP/ GMP Certification ','Product Quality: Organic','Product Quality: Halal','Product Quality: Other Certification','Type of Enterprise/Business Size','Store Capacity Organic (Current Volume, ave./month)','Organic Potential/Target Capacity','Other Info Organic','Store Capacity Synthetic (Current Volume, ave./month)','Synthetic Potential/Target Capacity','Other Info Synthetic','Store Capacity Pesticides (Current Volume, ave./month)','Pesticides Potential/Target Capacity','Pesticides Other Info','Store Capacity Herbicides (Current Volume, ave./month)','Herbicides Potential/Target Capacity','Herbicides Other Info','Store Capacity Vermicast Compost (Current Volume, ave./month)','Vermicast Compost Potential/Target Capacity','Vermicast Compost Other Info','Store Capacity Seedlings (Current Volume, ave./month)','Seedlings Potential/Target Capacity','Seedlings Other Info','Store Capacity Others (Current Volume, ave./month)','Others Potential/Target Capacity','Others Other Info','Drying Area/Capacity Utilization (%)','Drying Potential for Expansion-demand based? (Y/N)','Drying Other Information','Storage Area/Capacity Utilization (%)','Storage Potential for Expansion-demand based? (Y/N)','Storage Other Information','Hauling Area/Capacity Utilization (%)','Hauling Potential for Expansion-demand based? (Y/N)','Hauling Other Information','Semi-Processing Current Capacity/ Production ','Semi-Processing Potential for Expansion? (Y/N)','Semi-Processing Other Information','Final Product Current Capacity/ Production ','Final Product Potential for Expansion? (Y/N)','Final Product Other Information','Trading Volume/ Capacity','Trading Potential for Expansion? (Y/N)','Trading Other Information','Markteting Production Cap./Month','Martketing Potential for Expansion? (Y/N)','Marketing Other Information','Micro-financing Loan Portfolio (specific to RAPID priority crops)','Micro-financing Potential for Expansion? (Y/N)','Micro-financing Other Information','Insurance Loan Portfolio (specific to RAPID priority crops)','Insurance Potential for Expansion? (Y/N)','Insurance Other Information','Production & Sales Product/Services( under VC only)','Production & Sales Sales Volume/month','Production & Sales Unit Selling Price','Production & Sales Unit Measurement(kgs/sack/pc, interest)','Production & Sales Payment Terms','Raw Materials','Volume/Supply Requirement','Quality Requirement(organic, color, packaging, etc.)','Payment Terms/ Arrangement','Clients','Sales Volume (ave. month)','Payment Terms (COD, consignment, others)','Number of Workers (Qty) MALE in-house','Number of Workers (Qty) FEMALE in-house','Number of IP Group in-house','Ave. # of workdays/mo. in-house','Ave. Salary/ Wage/month in-house','Number of Workers (Qty) MALE sub-contractor','Number of Workers (Qty) FEMALE sub-contractor','Number of IP Group sub-contractor','Ave. # of workdays/mo. sub-contractor','Ave. Salary/ Wage/month sub-contractor','Number of Workers (Qty) MALE pakyaw','Number of Workers (Qty) FEMALE pakyaw','Number of IP Group pakyaw','Ave. # of workdays/mo. pakyaw','Ave. Salary/ Wage/month pakyaw','Supply Availability','Pricing','Quality of Raw Materials','Quality of Final Product','Other, please specify','Do you have existing commercial partnership with suppliers?','Do you provide support/assistance to your current partners?','Are you satisfied with your current business/production performance? IF No, what do you think you need to do to improve it? Please specify your answer in the space provided:','Does your membership in the organization helps you in your livelihood?','What do you think the LGU, NGAs and other agencies should do to improve the local commodity cluster industry? (Cacao, Coffee, Coco, Process Fruits & nuts)','Uploaded by']
	for column in df:
		column_width = max(df[column].astype(str).map(len).max(), len(column))
		col_idx = df.columns.get_loc(column)
		writer.sheets['exported_file'].set_column(col_idx, col_idx, column_width);

	
	workbook  = writer.book
	worksheet = writer.sheets['exported_file']
	header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00cc66','border': 1})
	for col_num, value in enumerate(df.columns.values):
		worksheet.write(0, col_num, value, header_format)
	writer.save()
	return send_file(c.RECORDS+'/objects/_temp_/exported_file.xlsx')


@app.route('/insert', methods = ['POST'])
def insert():   
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	insertData.insert(request)
	return redirect("/cform")
	

@app.route('/update',methods=['POST','GET'])
def update():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	updateData.update(request)
	return redirect("/formcdashboard")

@app.route('/update_prof',methods=['POST','GET'])
def update_prof():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	if request.method == "POST":
		
		editfullname = request.form.get("editfullname")
		editemail = request.form.get("editemail")
		editphone = request.form.get("editphone")
		editaddress = request.form.get("editaddress")
		user_id = session["USER_DATA"][0]['id']
		# if (len(request.files.getlist('file'))>1):
		FILE_REQ = file_from_request(app)
		__f = FILE_REQ._save_file_from_request(request,"file",c.RECORDS+"objects/userpics/",False,False)
		print(__f)
		sql = "UPDATE users set name = '{}', email = '{}', mobile = '{}', address = '{}', profilepic = '{}' WHERE id = '{}'".format(editfullname, editemail, editphone, editaddress,__f['file_arr_str'] , user_id)
		# else:

		# result=db.do(sql)

		if(__f["status"]=="error"):
			if(__f['msg']=="No File Found in Form"):
				sql = "UPDATE users set name = '{}', email = '{}', mobile = '{}', address = '{}' WHERE id = '{}'".format(editfullname, editemail, editphone, editaddress, user_id)
				result=db.do(sql)
				flash("Profile updated successfully. You have been logged out. Please log in again.", "success")

			else:
				flash(f"An error occured !", "error")
		else:
			sql = "UPDATE users set name = '{}', email = '{}', mobile = '{}', address = '{}', profilepic = '{}' WHERE id = '{}'".format(editfullname, editemail, editphone, editaddress,__f['file_arr_str'] , user_id)
			result=db.do(sql)
			flash("Profile updated successfully. You have been logged out. Please log in again.", "success")
	return redirect("/logout")

@app.route('/dcfweb')
def dcfweb():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("dcfweb.html")


@app.route('/fmiweb')
def fmiweb():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("fmiweb.html")



@app.route("/viewprofile")
def viewprofile():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	if(is_on_session()):
		sesh = db.select("SELECT `id`,`name`,`job`,`email`,`mobile`,`address`,`profilepic`,`rcu`,`pcu` FROM `users` WHERE `id`='{}' ;".format(request.args['_id']))[0]
		print(sesh)
		user_rank=user_management.user_rankings(sesh['id'])
		prof_a_inputed_data = user_rank['profiling_a']['inputed']
		prof_a_total_data = user_rank['profiling_a']['total']
		try:
			prof_a_percentage = (prof_a_inputed_data / prof_a_total_data) * 100
		except Exception as e:
			prof_a_percentage = 0

		prof_b_inputed_data = user_rank['prof_b']['inputed']
		prof_b_total_data = user_rank['prof_b']['total']

		try:
			prof_b_percentage = (prof_b_inputed_data / prof_b_total_data) * 100
		except Exception as e:
			prof_b_percentage = 0

		prof_c_inputed_data = user_rank['prof_c']['inputed']
		prof_c_total_data = user_rank['prof_c']['total']
		try:
			prof_c_percentage = (prof_c_inputed_data / prof_c_total_data) * 100
		except Exception as e:
			prof_c_percentage = 0

		dcf1_inputed_data = user_rank['dcf1']['inputed']
		dcf1_total_data = user_rank['dcf1']['total']

		try:
			dcf1_percentage = (dcf1_inputed_data / dcf1_total_data) * 100
		except Exception as e:
			dcf1_percentage = 0

		dcf2_inputed_data = user_rank['dcf2']['inputed']
		dcf2_total_data = user_rank['dcf2']['total']

		try:
			dcf2_percentage = (dcf2_inputed_data / dcf2_total_data) * 100
		except Exception as e:
			dcf2_percentage = 0

		dcf3_inputed_data = user_rank['dcf3']['inputed']
		dcf3_total_data = user_rank['dcf3']['total']

		try:
			dcf3_percentage = (dcf3_inputed_data / dcf3_total_data) * 100
		except Exception as e:
			dcf3_percentage = 0

		dcf4_inputed_data = user_rank['dcf4']['inputed']
		dcf4_total_data = user_rank['dcf4']['total']

		try:
			dcf4_percentage = (dcf4_inputed_data / dcf4_total_data) * 100
		except Exception as e:
			dcf4_percentage = 0

		dcf5_inputed_data = user_rank['dcf5']['inputed']
		dcf5_total_data = user_rank['dcf5']['total']

		try:
			dcf5_percentage = (dcf5_inputed_data / dcf5_total_data) * 100
		except Exception as e:
			dcf5_percentage = 0

		dcf6_inputed_data = user_rank['dcf6']['inputed']
		dcf6_total_data = user_rank['dcf6']['total']

		try:
			dcf6_percentage = (dcf6_inputed_data / dcf6_total_data) * 100
		except Exception as e:
			dcf6_percentage = 0

		dcf7_inputed_data = user_rank['dcf7']['inputed']
		dcf7_total_data = user_rank['dcf7']['total']

		try:
			dcf7_percentage = (dcf7_inputed_data / dcf7_total_data) * 100
		except Exception as e:
			dcf7_percentage = 0

		dcf9_inputed_data = user_rank['dcf9']['inputed']
		dcf9_total_data = user_rank['dcf9']['total']

		try:
			dcf9_percentage = (dcf9_inputed_data / dcf9_total_data) * 100
		except Exception as e:
			dcf9_percentage = 0

		dcf10_inputed_data = user_rank['dcf10']['inputed']
		dcf10_total_data = user_rank['dcf10']['total']

		try:
			dcf10_percentage = (dcf10_inputed_data / dcf10_total_data) * 100
		except Exception as e:
			dcf10_percentage = 0

		dcf11_inputed_data = user_rank['dcf11']['inputed']
		dcf11_total_data = user_rank['dcf11']['total']

		try:
			dcf11_percentage = (dcf11_inputed_data / dcf11_total_data) * 100
		except Exception as e:
			dcf11_percentage = 0

		return render_template("viewprofile.html",user_data=sesh,prof_a_percentage = round(prof_a_percentage, 3),prof_b_percentage = round(prof_b_percentage, 3),prof_c_percentage = round(prof_c_percentage, 3),dcf1_percentage = round(dcf1_percentage, 3),dcf2_percentage = round(dcf2_percentage, 3),dcf3_percentage = round(dcf3_percentage, 3),dcf4_percentage = round(dcf4_percentage, 3),dcf5_percentage = round(dcf5_percentage, 3),dcf6_percentage = round(dcf6_percentage, 3),dcf7_percentage = round(dcf7_percentage, 3),dcf9_percentage = round(dcf9_percentage, 3),dcf10_percentage = round(dcf10_percentage, 3),dcf11_percentage = round(dcf11_percentage, 3),user_rank=user_rank)
	else:
		return redirect("/login?force_url=1")


@app.route("/menuv2")
def menuv2():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	if(is_on_session()):
		return redirect("/mis-v4/core-main")
		# DEPRICATED MENU
		sesh = session["USER_DATA"][0]
		user_rank=user_management.user_rankings(sesh['id'])
		prof_a_inputed_data = user_rank['profiling_a']['inputed']
		prof_a_total_data = user_rank['profiling_a']['total']
		try:
			prof_a_percentage = (prof_a_inputed_data / prof_a_total_data) * 100
		except Exception as e:
			prof_a_percentage = 0

		prof_b_inputed_data = user_rank['prof_b']['inputed']
		prof_b_total_data = user_rank['prof_b']['total']

		try:
			prof_b_percentage = (prof_b_inputed_data / prof_b_total_data) * 100
		except Exception as e:
			prof_b_percentage = 0

		prof_c_inputed_data = user_rank['prof_c']['inputed']
		prof_c_total_data = user_rank['prof_c']['total']
		try:
			prof_c_percentage = (prof_c_inputed_data / prof_c_total_data) * 100
		except Exception as e:
			prof_c_percentage = 0

		dcf1_inputed_data = user_rank['dcf1']['inputed']
		dcf1_total_data = user_rank['dcf1']['total']

		try:
			dcf1_percentage = (dcf1_inputed_data / dcf1_total_data) * 100
		except Exception as e:
			dcf1_percentage = 0

		dcf2_inputed_data = user_rank['dcf2']['inputed']
		dcf2_total_data = user_rank['dcf2']['total']

		try:
			dcf2_percentage = (dcf2_inputed_data / dcf2_total_data) * 100
		except Exception as e:
			dcf2_percentage = 0

		dcf3_inputed_data = user_rank['dcf3']['inputed']
		dcf3_total_data = user_rank['dcf3']['total']

		try:
			dcf3_percentage = (dcf3_inputed_data / dcf3_total_data) * 100
		except Exception as e:
			dcf3_percentage = 0

		dcf4_inputed_data = user_rank['dcf4']['inputed']
		dcf4_total_data = user_rank['dcf4']['total']

		try:
			dcf4_percentage = (dcf4_inputed_data / dcf4_total_data) * 100
		except Exception as e:
			dcf4_percentage = 0

		dcf5_inputed_data = user_rank['dcf5']['inputed']
		dcf5_total_data = user_rank['dcf5']['total']

		try:
			dcf5_percentage = (dcf5_inputed_data / dcf5_total_data) * 100
		except Exception as e:
			dcf5_percentage = 0

		dcf6_inputed_data = user_rank['dcf6']['inputed']
		dcf6_total_data = user_rank['dcf6']['total']

		try:
			dcf6_percentage = (dcf6_inputed_data / dcf6_total_data) * 100
		except Exception as e:
			dcf6_percentage = 0

		dcf7_inputed_data = user_rank['dcf7']['inputed']
		dcf7_total_data = user_rank['dcf7']['total']

		try:
			dcf7_percentage = (dcf7_inputed_data / dcf7_total_data) * 100
		except Exception as e:
			dcf7_percentage = 0

		dcf9_inputed_data = user_rank['dcf9']['inputed']
		dcf9_total_data = user_rank['dcf9']['total']

		try:
			dcf9_percentage = (dcf9_inputed_data / dcf9_total_data) * 100
		except Exception as e:
			dcf9_percentage = 0

		dcf10_inputed_data = user_rank['dcf10']['inputed']
		dcf10_total_data = user_rank['dcf10']['total']

		try:
			dcf10_percentage = (dcf10_inputed_data / dcf10_total_data) * 100
		except Exception as e:
			dcf10_percentage = 0

		dcf11_inputed_data = user_rank['dcf11']['inputed']
		dcf11_total_data = user_rank['dcf11']['total']

		try:
			dcf11_percentage = (dcf11_inputed_data / dcf11_total_data) * 100
		except Exception as e:
			dcf11_percentage = 0


		return render_template("menuv2.html",user_data=sesh,prof_a_percentage = round(prof_a_percentage, 3),prof_b_percentage = round(prof_b_percentage, 3),prof_c_percentage = round(prof_c_percentage, 3),dcf1_percentage = round(dcf1_percentage, 3),dcf2_percentage = round(dcf2_percentage, 3),dcf3_percentage = round(dcf3_percentage, 3),dcf4_percentage = round(dcf4_percentage, 3),dcf5_percentage = round(dcf5_percentage, 3),dcf6_percentage = round(dcf6_percentage, 3),dcf7_percentage = round(dcf7_percentage, 3),dcf9_percentage = round(dcf9_percentage, 3),dcf10_percentage = round(dcf10_percentage, 3),dcf11_percentage = round(dcf11_percentage, 3),user_rank=user_management.user_rankings(sesh['id']))
	else:
		return redirect("/login?force_url=1")
	
@app.route('/fundtrackerweb')
def fundtrackerweb():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("fundtrackerweb.html")



@app.route("/formcdashboard")
def formcdashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	disp = displayData.display__()
	# disp = displayData.display()
	# return disp
	return render_template("formcdashboard.html",user_data=session["USER_DATA"][0],**disp)

@app.route("/formcdashboardfilter",methods=['POST','GET'])
def formcdashboardfilter():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	filt = filterData.data_filter(request)
	return render_template("formcdashboardfilter.html",user_data=session["USER_DATA"][0],**filt)

@app.route("/menu")
def menu():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	if(is_on_session()):
		sesh = session["USER_DATA"][0]
		user_rank=user_management.user_rankings(sesh['id'])
		prof_a_inputed_data = user_rank['profiling_a']['inputed']
		prof_a_total_data = user_rank['profiling_a']['total']
		prof_a_percentage = (prof_a_inputed_data / prof_a_total_data) * 100

		prof_c_inputed_data = user_rank['prof_c']['inputed']
		prof_c_total_data = user_rank['prof_c']['total']
		prof_c_percentage = (prof_c_inputed_data / prof_c_total_data) * 100

		return render_template("menu.html",user_data=sesh,prof_a_percentage = round(prof_a_percentage, 3),prof_c_percentage = round(prof_c_percentage, 3),user_rank=user_management.user_rankings(sesh['id']))
	else:
		return redirect("/login?force_url=1")
	
@app.route("/change_password", methods=["POST"])
def change_password():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	current_password = request.form.get("currpass_user")
	confirm_password = request.form.get("confpass_user")
	user_id = session["USER_DATA"][0]['id']
	sql = "SELECT password FROM users WHERE id = '{}'".format(user_id)
	session_pass = db.select(sql)[0]['password']
	if current_password == session_pass:
		update = "UPDATE users SET password = '{}' WHERE id = '{}'".format(confirm_password, user_id)
		db.do(update)
		flash("Password changed successfully. You have been logged out. Please log in again with your new password.", "success")
	else:
		flash(f"Password Incorrect!", "error")

	return redirect("/menuv2")

@app.route("/cform")
def cform():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("formc.html",user_data=session["USER_DATA"][0])


@app.route("/spreadsheet")
def spreadsheet():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	SQL ="""
	SELECT form_c.filename, COUNT(form_c.filename) AS _COUNT, users.name
	FROM `form_c`
	JOIN `users` ON form_c.upload_by = users.id
	WHERE form_c.upload_by = {}
	GROUP BY form_c.filename;
	""".format(session["USER_DATA"][0]['id'])
	uploaded_file_by_user = db.select(SQL)
	return render_template("spreadsheet.html",user_data=session["USER_DATA"][0],uploaded_file_by_user=uploaded_file_by_user)

@app.route('/delete/<string:filename_>', methods = ['POST','GET'])
def delete(filename_):
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	filename_ = filename_.replace("@@","#")
	sql="DELETE FROM form_c WHERE filename = '{}'; ".format(filename_)
	print(sql)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The file was deleted successfully!", "success")
			print(str(delete))
	return redirect("/spreadsheet")

@app.route('/download_file/<filename_>', methods=['GET'], endpoint='download_file')
@app.route('/download/<filename_>', methods=['GET'], endpoint='download_file')
def download_file(filename_):
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	path = "assets/objects/spreadsheets_c/queued/" + filename_
	print(path)
	return send_file(path, as_attachment=True)

@app.route('/download_file_/<filename_>', methods=['GET'], endpoint='download_file_')
@app.route('/download_/<filename_>', methods=['GET'], endpoint='download_file_')
def download_file_(filename_):
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	path = "assets/objects/spreadsheets_c/queued/" + filename_.replace("@@","#")
	print(path)
	return send_file(path, as_attachment=True)


# =======================================

def position_data_filter():
	_filter = "WHERE 1 "
	JOB = session["USER_DATA"][0]["job"].lower()

	if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = "WHERE 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = "WHERE  upload_by in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"]) 
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

