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
		query= db.select("SELECT name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,potential_organic,other_info_organic,store_capacity_synthetic,potential_synthetic, other_info_synthetic, store_capacity_pesticides,potential_pesticides,other_info_pesticides, store_capacity_herbicides, potential_herbicides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage,potential_exp_storage,other_info_storage,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry FROM form_c")

	df_nested_list = pd.json_normalize(query)
	df = pd.DataFrame (df_nested_list)
	writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/exported_file.xlsx') 
	df.to_excel(writer, sheet_name='exported_file',index=False )
	df.columns =['Name Of Respondent','Designation in the Firm','Sex','Age','Contact Details','Email Address','Stakeholder Category','Industry Cluster','Registered Business Name',' Business Address','Form of Enterprise','Administration: Business Registration','Administration: Product Registration','Administration: Certificate of Registration','Administration: License to Operate','Product Quality: ISO Certification','Product Quality: GAP/ GMP Certification ','Product Quality: Organic','Product Quality: Halal','Product Quality: Other Certification','Type of Enterprise/Business Size','Store Capacity Organic (Current Volume, ave./month)','Organic Potential/Target Capacity','Other Info Organic','Store Capacity Synthetic (Current Volume, ave./month)','Synthetic Potential/Target Capacity','Other Info Synthetic','Store Capacity Pesticides (Current Volume, ave./month)','Pesticides Potential/Target Capacity','Pesticides Other Info','Store Capacity Herbicides (Current Volume, ave./month)','Herbicides Potential/Target Capacity','Herbicides Other Info','Store Capacity Vermicast Compost (Current Volume, ave./month)','Vermicast Compost Potential/Target Capacity','Vermicast Compost Other Info','Store Capacity Seedlings (Current Volume, ave./month)','Seedlings Potential/Target Capacity','Seedlings Other Info','Store Capacity Others (Current Volume, ave./month)','Others Potential/Target Capacity','Others Other Info','Drying Area/Capacity Utilization (%)','Drying Potential for Expansion-demand based? (Y/N)','Drying Other Information','Storage Area/Capacity Utilization (%)','Storage Potential for Expansion-demand based? (Y/N)','Storage Other Information','Hauling Area/Capacity Utilization (%)','Hauling Potential for Expansion-demand based? (Y/N)','Hauling Other Information','Semi-Processing Current Capacity/ Production ','Semi-Processing Potential for Expansion? (Y/N)','Semi-Processing Other Information','Final Product Current Capacity/ Production ','Final Product Potential for Expansion? (Y/N)','Final Product Other Information','Trading Volume/ Capacity','Trading Potential for Expansion? (Y/N)','Trading Other Information','Markteting Production Cap./Month','Martketing Potential for Expansion? (Y/N)','Marketing Other Information','Micro-financing Loan Portfolio (specific to RAPID priority crops)','Micro-financing Potential for Expansion? (Y/N)','Micro-financing Other Information','Insurance Loan Portfolio (specific to RAPID priority crops)','Insurance Potential for Expansion? (Y/N)','Insurance Other Information','Production & Sales Product/Services( under VC only)','Production & Sales Sales Volume/month','Production & Sales Unit Selling Price','Production & Sales Unit Measurement(kgs/sack/pc, interest)','Production & Sales Payment Terms','Raw Materials','Volume/Supply Requirement','Quality Requirement(organic, color, packaging, etc.)','Payment Terms/ Arrangement','Clients','Sales Volume (ave. month)','Payment Terms (COD, consignment, others)','Number of Workers (Qty) MALE in-house','Number of Workers (Qty) FEMALE in-house','Number of IP Group in-house','Ave. # of workdays/mo. in-house','Ave. Salary/ Wage/month in-house','Number of Workers (Qty) MALE sub-contractor','Number of Workers (Qty) FEMALE sub-contractor','Number of IP Group sub-contractor','Ave. # of workdays/mo. sub-contractor','Ave. Salary/ Wage/month sub-contractor','Number of Workers (Qty) MALE pakyaw','Number of Workers (Qty) FEMALE pakyaw','Number of IP Group pakyaw','Ave. # of workdays/mo. pakyaw','Ave. Salary/ Wage/month pakyaw','Supply Availability','Pricing','Quality of Raw Materials','Quality of Final Product','Other, please specify','Do you have existing commercial partnership with suppliers?','Do you provide support/assistance to your current partners?','Are you satisfied with your current business/production performance? IF No, what do you think you need to do to improve it? Please specify your answer in the space provided:','Does your membership in the organization helps you in your livelihood?','What do you think the LGU, NGAs and other agencies should do to improve the local commodity cluster industry? (Cacao, Coffee, Coco, Process Fruits & nuts)']
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
		user_rank_=user_management.user_rankings(sesh['id'])
		prof_a_inputed_data = user_rank_['profiling_a']['inputed']
		prof_a_total_data = user_rank_['profiling_a']['total']
		prof_a_percentage = (prof_a_inputed_data / prof_a_total_data) * 100

		prof_c_inputed_data = user_rank_['prof_c']['inputed']
		prof_c_total_data = user_rank_['prof_c']['total']
		prof_c_percentage = (prof_c_inputed_data / prof_c_total_data) * 100

		return render_template("viewprofile.html",user_data=sesh,prof_a_percentage = round(prof_a_percentage, 3),prof_c_percentage = round(prof_c_percentage, 3),user_rank=user_rank_)
	else:
		return redirect("/login?force_url=1")


@app.route("/menuv2")
def menuv2():
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

		return render_template("menuv2.html",user_data=sesh,prof_a_percentage = round(prof_a_percentage, 3),prof_c_percentage = round(prof_c_percentage, 3),user_rank=user_management.user_rankings(sesh['id']))
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
	sql='DELETE FROM form_c WHERE filename = {0}'.format(filename_)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The file was deleted successfully!", "success")
			print(str(delete))
	return render_template("spreadsheet.html",user_data=session["USER_DATA"][0])

@app.route('/download/<string:filename_>', methods=['GET'], endpoint='download_file')
def download_file(filename_):
	path = "assets/objects/spreadsheets_c/queued/" + filename_
	return send_file(path, as_attachment=True)


# =======================================

def position_data_filter():
	_filter = "WHERE 1 "
	JOB = session["USER_DATA"][0]["job"].lower()

	if(JOB in "admin" or JOB in "super admin"):
		session["USER_DATA"][0]["office"] = "NPCO"
		_filter = "WHERE 1 "
	else:
		session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
		_filter = "WHERE  USER_ID in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"]) 

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

