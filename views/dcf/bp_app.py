from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file, jsonify
from decimal import Decimal
import pandas as pd
from tqdm import tqdm
from time import sleep
import xlrd
import json
from werkzeug.utils import secure_filename
import jinja2
import os
from views.dcf.form_insert import insert_form4 as insertData4
from views.dcf.form_insert import insert_form5 as insertData5
from views.dcf.form_insert import insert_form6 as insertData6
from views.dcf.form_insert import insert_form7 as insertData7
from views.dcf.form_insert import insert_form9 as insertData9
from views.dcf.form_insert import insert_form10 as insertData10
from views.dcf.form_insert import insert_form11 as insertData11
from views.dcf.form_insert import insert_form1 as insertData1
from views.dcf.form_insert import insert_form3 as insertData3
from views.dcf.form_insert import insert_form2 as insertData2
from views.dcf.dashboard import dashboard_count as displayCount
from views.dcf.dashboard import display_dataform as display_dataform
from views.dcf.form_update import update_form1 as update_dataform1
from views.dcf.form_update import update_form2 as update_dataform2
from views.dcf.form_update import update_form3 as update_dataform3
from views.dcf.form_update import update_form4 as update_dataform4
from views.dcf.form_update import update_form5 as update_dataform5
from views.dcf.form_update import update_form6 as update_dataform6
from views.dcf.form_update import update_form7 as update_dataform7
from views.dcf.form_update import update_form9 as update_dataform9
from views.dcf.form_update import update_form10 as update_dataform10
from views.dcf.form_update import update_form11 as update_dataform11
import Configurations as c 
from modules.Connections import mysql
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form1
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form2
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form3
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form4
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form5
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form6
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form7
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form9
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form10
from views.dcf.spreadsheet import dcf_import_excel as importcsv_form11
from modules.Req_Brorn_util import file_from_request







db = mysql(*c.DB_CRED)
db.err_page = 0
app = Blueprint("dcf",__name__,template_folder="pages")

def is_on_session(): return ('USER_DATA' in session)


@app.route('/sample/<item>')
@c.login_auth_web()
def sample(item):
	return display_dataform.displayform()[item]


@app.route('/dcf_dashboard')
def dcf_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	count = displayCount.display__()
	form_disp = display_dataform.displayform()
	return render_template("dcf_dashboard.html",user_data=session["USER_DATA"][0],**count,**form_disp)



@app.route('/form1_dashboard')
def form1_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form1_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form1_fulldashboard')
def form1_fulldashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form1_fulldashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form2_dashboard')
def form2_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form2_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form3_dashboard')
def form3_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form3_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form4_dashboard')
def form4_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form4_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form5_dashboard')
def form5_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form5_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form6_dashboard')
def form6_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form6_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form7_dashboard')
def form7_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form7_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form8_dashboard')
def form8_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form8_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form9_dashboard')
def form9_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form9_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form10_dashboard')
def form10_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form10_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/form11_dashboard')
def form11_dashboard():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	form_disp = display_dataform.displayform()
	return render_template("form_dashboard/form11_dashboard.html",user_data=session["USER_DATA"][0],**form_disp)

@app.route('/updateform1',methods=['POST','GET'])
def updateform1():
	update_dataform1.updateform1(request)
	return redirect("/form1_dashboard")

@app.route('/updateform2',methods=['POST','GET'])
def updateform2():
	update_dataform2.updateform2(request)
	return redirect("/form2_dashboard")


@app.route('/updateform3',methods=['POST','GET'])
def updateform3():
	update_dataform3.updateform3(request)
	return redirect("/form3_dashboard")


@app.route('/updateform4',methods=['POST','GET'])
def updateform4():
	update_dataform4.updateform4(request)
	return redirect("/form4_dashboard")

@app.route('/updateform5',methods=['POST','GET'])
def updateform5():
	update_dataform5.updateform5(request)
	return redirect("/form5_dashboard")

@app.route('/updateform6',methods=['POST','GET'])
def updateform6():
	update_dataform6.updateform6(request)
	return redirect("/form6_dashboard")


@app.route('/updateform7',methods=['POST','GET'])
def updateform7():
	update_dataform7.updateform7(request)
	return redirect("/form7_dashboard")


@app.route('/updateform9',methods=['POST','GET'])
def updateform9():
	update_dataform9.updateform9(request)
	return redirect("/form9_dashboard")


@app.route('/updateform10',methods=['POST','GET'])
def updateform10():
	update_dataform10.updateform10(request)
	return redirect("/form10_dashboard")

@app.route('/updateform11',methods=['POST','GET'])
def updateform11():
	update_dataform11.updateform11(request)
	return redirect("/form11_dashboard")

@app.route('/dcf_forms')
def dcf_forms():
	return redirect("/dcf_forms")
 
@app.route('/dcf/<form>')
def form1(form):
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template('includes/forms/{}.html'.format(form),user_data=session["USER_DATA"][0])

@app.route('/dcf/<viewform>')
def viewform1(viewform):
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template('includes/viewform_modal/{}.html'.format(viewform),user_data=session["USER_DATA"][0])

@app.route('/dcf_spreadsheet')
def dcf_spreadsheet():
	if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
	return render_template("dcf_spreadsheet.html",user_data=session["USER_DATA"][0])

#INSERT DATA -------------------------------------------------------

@app.route('/insert_form4', methods = ['POST'])
def insert_form4():
	insertData4.insert_form4(request)
	return redirect("/dcf/form4")

@app.route('/insert_form5', methods = ['POST'])
def insert_form5():
	insertData5.insert_form5(request)
	return redirect("/dcf/form5")

@app.route('/insert_form1', methods = ['POST'])
def insert_form1():
	insertData1.insert_form1(request)
	return redirect("/dcf/form1")

@app.route('/insert_form3', methods = ['POST'])
def insert_form3():
	insertData3.insert_form3(request)
	return redirect("/dcf/form3")


@app.route('/insert_form2', methods = ['POST'])
def insert_form2():
	insertData2.insert_form2(request)
	return redirect("/dcf/form2")

@app.route('/insert_form6', methods = ['POST'])
def insert_form6():
	insertData6.insert_form6(request)
	return redirect("/dcf/form6")

@app.route('/insert_form7', methods = ['POST'])
def insert_form7():
	insertData7.insert_form7(request)
	return redirect("/dcf/form7")

@app.route('/insert_form9', methods = ['POST'])
def insert_form9():
	insertData9.insert_form9(request)
	return redirect("/dcf/form9")

@app.route('/insert_form10', methods = ['POST'])
def insert_form10():
	insertData10.insert_form10(request)
	return redirect("/dcf/form10")

@app.route('/insert_form11', methods = ['POST'])
def insert_form11():
	insertData11.insert_form11(request)
	return redirect("/dcf/form11")

#-------------------------------------------------------

#DELETE ROW DATA -------------------------------------------------------

@app.route('/delete_form1/<string:id>', methods = ['POST','GET'])
def delete_form1(id):
	sql='DELETE FROM dcf_prep_review_aprv_status WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form1_dashboard")

@app.route('/delete_form2/<string:id>', methods = ['POST','GET'])
def delete_form2(id):
	sql='DELETE FROM dcf_implementing_unit WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form2_dashboard")

@app.route('/delete_form3/<string:id>', methods = ['POST','GET'])
def delete_form3(id):
	sql='DELETE FROM dcf_bdsp_reg WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form3_dashboard")

@app.route('/delete_form4/<string:id>', methods = ['POST','GET'])
def delete_form4(id):
	sql='DELETE FROM dcf_capacity_building WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form4_dashboard")

@app.route('/delete_form5/<string:id>', methods = ['POST','GET'])
def delete_form5(id):
	sql='DELETE FROM dcf_matching_grant WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form5_dashboard")

@app.route('/delete_form6/<string:id>', methods = ['POST','GET'])
def delete_form6(id):
	sql='DELETE FROM dcf_product_development WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form6_dashboard")

@app.route('/delete_form7/<string:id>', methods = ['POST','GET'])
def delete_form7(id):
	sql='DELETE FROM dcf_trade_promotion WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form7_dashboard")

@app.route('/delete_form9/<string:id>', methods = ['POST','GET'])
def delete_form9(id):
	sql='DELETE FROM dcf_enablers_activity WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form9_dashboard")

@app.route('/delete_form10/<string:id>', methods = ['POST','GET'])
def delete_form10(id):
	sql='DELETE FROM dcf_negosyo_center WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form10_dashboard")

@app.route('/delete_form11/<string:id>', methods = ['POST','GET'])
def delete_form11(id):
	sql='DELETE FROM dcf_access_financing WHERE id = {0}'.format(id)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			flash(f"An error occured !", "error") 
			print(str(delete))
	else:
			flash(f"The data was deleted successfully!", "success")
			print(str(delete))
	return redirect("/form11_dashboard")


@app.route('/importcsvform1',methods = ['GET','POST'])
def importcsvform1():
	importcsv_form1.importcsvform1(request)
	return redirect("/form1_dashboard")

@app.route('/importcsvform2',methods = ['GET','POST'])
def importcsvform2():
	importcsv_form2.importcsvform2(request)
	return redirect("/form2_dashboard")

@app.route('/importcsvform3',methods = ['GET','POST'])
def importcsvform3():
	importcsv_form3.importcsvform3(request)
	return redirect("/form3_dashboard")

@app.route('/importcsvform4',methods = ['GET','POST'])
def importcsvform4():
	importcsv_form4.importcsvform4(request)
	return redirect("/form4_dashboard")

@app.route('/importcsvform5',methods = ['GET','POST'])
def importcsvform5():
	importcsv_form5.importcsvform5(request)
	return redirect("/form5_dashboard")

@app.route('/importcsvform6',methods = ['GET','POST'])
def importcsvform6():
	importcsv_form6.importcsvform6(request)
	return redirect("/form6_dashboard")

@app.route('/importcsvform7',methods = ['GET','POST'])
def importcsvform7():
	importcsv_form7.importcsvform7(request)
	return redirect("/form7_dashboard")

@app.route('/importcsvform9',methods = ['GET','POST'])
def importcsvform9():
	importcsv_form9.importcsvform9(request)
	return redirect("/form9_dashboard")

@app.route('/importcsvform10',methods = ['GET','POST'])
def importcsvform10():
	importcsv_form10.importcsvform10(request)
	return redirect("/form10_dashboard")

@app.route('/importcsvform11',methods = ['GET','POST'])
def importcsvform11():
	importcsv_form11.importcsvform11(request)
	return redirect("/form11_dashboard")

#-------------------------------------------------------------------------------


@app.route('/dcf', methods=['GET', 'POST'])
def dcfexport_data():
	if request.method == 'POST':
		export_type = request.form.get('export_type')
		print("---------------------------")
		print(export_type)
		if export_type == 'form1export':
			def form1export():
				if request.method == "POST":
					query= db.select('''SELECT dcf_prep_review_aprv_status.id,
						dcf_prep_review_aprv_status.form_1_rcus,
						dcf_prep_review_aprv_status.form_1_name_dip,
						dcf_prep_review_aprv_status.form_1_anchor_firm,
						dcf_prep_review_aprv_status.form_1_size_of_anchor,
						dcf_prep_review_aprv_status.form_1_msmes,
						dcf_prep_review_aprv_status.form_1_scope_provinces,
						CONCAT(dcf_prep_review_aprv_status.form_1_commodity, ' ', dcf_prep_review_aprv_status.form_1_commodity_others) AS 'Commodity'  ,
						dcf_prep_review_aprv_status.form_1_for_development,
						dcf_prep_review_aprv_status.form_1_finalized_approved,
						dcf_prep_review_aprv_status.form_1_date_of_parallel_review,
						dcf_prep_review_aprv_status.form_1_date_of_submission,
						dcf_prep_review_aprv_status.form_1_date_of_rtwg,
						dcf_prep_review_aprv_status.form_1_date_of_npco_cursory,
						dcf_prep_review_aprv_status.form_1_date_of_ifad_no_inssuance,
						dcf_prep_review_aprv_status.total_large_enterprise,
						dcf_prep_review_aprv_status.total_medium_enterprise,
						dcf_prep_review_aprv_status.total_small_enterprise,
						dcf_prep_review_aprv_status.total_micro_enterprise,
						dcf_prep_review_aprv_status.form_1_totalmale,
						dcf_prep_review_aprv_status.form_1_maleyouth,
						dcf_prep_review_aprv_status.form_1_maleip,
						dcf_prep_review_aprv_status.form_1_malepwd,
						dcf_prep_review_aprv_status.form_1_totalfemale,
						dcf_prep_review_aprv_status.form_1_femaleyouth,
						dcf_prep_review_aprv_status.form_1_femaleip,
						dcf_prep_review_aprv_status.form_1_femalepwd,
						dcf_prep_review_aprv_status.form_1_totalyouth,
						dcf_prep_review_aprv_status.form_1_totalip,
						dcf_prep_review_aprv_status.form_1_totalpwd,
						dcf_prep_review_aprv_status.form_1_totalcooperatives,
						dcf_prep_review_aprv_status.form_1_totalassociations,
						dcf_prep_review_aprv_status.form_1_totalmsme,
						dcf_prep_review_aprv_status.form_1_total_farmerbene,
						dcf_prep_review_aprv_status.form_1_totalfo,
						dcf_prep_review_aprv_status.form_1_hect_rehab,
						dcf_prep_review_aprv_status.form_1_total_cost_rehab,
						dcf_prep_review_aprv_status.form_1_hect_exp,
						dcf_prep_review_aprv_status.form_1_cost_exp,
						dcf_prep_review_aprv_status.form_1_totalhectarage_cov,
						dcf_prep_review_aprv_status.form_1_euqipment,
						dcf_prep_review_aprv_status.form_1_Facilities_warehouse,
						dcf_prep_review_aprv_status.form_1_totalcost_prodinvest,
						dcf_prep_review_aprv_status.form_1_total_rehab,
						dcf_prep_review_aprv_status.form_1_total_exp,
						dcf_prep_review_aprv_status.form_1_totalcost_prodinvest2,
						dcf_prep_review_aprv_status.form_1_partners_counterpart,
						dcf_prep_review_aprv_status.form_1_total_matching_grant,
						dcf_prep_review_aprv_status.form1_total_mg_cost,
						dcf_prep_review_aprv_status.form_1_organizational,
						dcf_prep_review_aprv_status.form_1_technical_trainings,
						dcf_prep_review_aprv_status.form_1_post_production,
						dcf_prep_review_aprv_status.form_1_others,
						dcf_prep_review_aprv_status.form_1_total_capbuild,
						dcf_prep_review_aprv_status.form_1_total_capbuild_counterpart,
						dcf_prep_review_aprv_status.form_1_supply_chain_manager,
						dcf_prep_review_aprv_status.supply_chain_manager_counterpart,
						dcf_prep_review_aprv_status.form_1_fmi,
						dcf_prep_review_aprv_status.form_1_fmi_kms,
						dcf_prep_review_aprv_status.fmi_part_counter,
						dcf_prep_review_aprv_status.form_1_y,
						dcf_prep_review_aprv_status.form_1_ac,
						dcf_prep_review_aprv_status.form_1_ad,
						dcf_prep_review_aprv_status.form1_total_fmi,
						dcf_prep_review_aprv_status.form_1_totalproject_cost,
						dcf_prep_review_aprv_status.partner_counterpart_MG,
						dcf_prep_review_aprv_status.partner_counterpart_CB,
						dcf_prep_review_aprv_status.partner_counterpart_SCM,
						dcf_prep_review_aprv_status.partner_counterpart_FMI,
						dcf_prep_review_aprv_status.partner_counterpart_total,
						dcf_prep_review_aprv_status.total_dip_cost_MG,
						dcf_prep_review_aprv_status.total_dip_cost_CB,
						dcf_prep_review_aprv_status.total_dip_cost_SCM,
						dcf_prep_review_aprv_status.total_dip_cost_FMI,
						dcf_prep_review_aprv_status.total_dip_cost_total,
						dcf_prep_review_aprv_status.date_created,
						dcf_prep_review_aprv_status.date_modified,
						users.name as 'Uploaded by'
						FROM dcf_prep_review_aprv_status
						INNER JOIN users ON `dcf_prep_review_aprv_status`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form1_exported_file', index=False)
					new_column_names = 'ID,RCUs,Name of DIP,Anchor Firms,Size of Anchor Firm,MSMEs,Scope/Provinces,Commodity,Start date of DIP development,Submission Date of Full BPs/DIPs to NPCO for Technical review,DIP Technical/Parallel Review Date (with NPCO/RGMS/IFAD Consultant/RTWG),Submission Date of revised DIPs (based on comments during the Technical/Parallel Review) to RTWG for approval,Date of RTWG Approval,DIP Submission Date to IFAD/NPCO for Final Approval,NPCO/IFAD (No Objection Issuance) Date,# of Large Enterprises,# of Medium Enterprises,# of Small Enterprises,# of Micro Enterprises,Total # of Male,# of Male-Youth,# of Male - IP,# of Male - PWD,Total # of Female,# of Female-Youth,# of Female - IP,# of Female - PWD,Total # of Youth,Total # of IP,Total # of PWD,Total # of Cooperatives,Total # of Associations,Total # of MSMEs,Total # of Smallholder Farming Households,Total # of Fos,Hectares for Rehab,Total Cost of Rehab,Hectares for Expansion,Total Cost of Expansion,Total Hectarage Covered,Equipment,Facilities/Warehouse,Total,Total cost of Rehab,Total Cost of Expansion,Total Cost of Productive Investments,Partners Total Counterpart,Total Project Cost (Project funds),Total MG Cost,Organizational,Technical Trainings,Post-Production,Others,Total Project Cost (Project funds),Partners Total Counterpart,Supply Chain Manager Project Cost,Supply Chain Manager Partner Counterpart,FMI Project Cost,FMI KMS,FMI Partner Counterpart,Total Matching Grant,Total Capacity Building,Supply Chain Manager,FMI,Total,Matching Grants,Capacity Building,Supply Chain Manager,FMI,Total,Matching Grants,Capacity Building,Supply Chain Manager,FMI,Total,Date Created,Date Modified, Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form1_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx')
			return form1export()
		elif export_type == 'form2export':
			def form2export():
				if request.method == "POST":
					query= db.select('''SELECT dcf_implementing_unit.id,
					dcf_implementing_unit.form_2_rcus,
					dcf_implementing_unit.form_2_pcu,
					CONCAT(dcf_implementing_unit.form_2_commodity,
					 ' ',
					 dcf_implementing_unit.form_2_commodity_others) AS 'Commodity',
					CONCAT(dcf_implementing_unit.form_2_dip_alignment,
					 ' ',
					 dcf_implementing_unit.form_2_dip_alignment_yes) AS 'dip_alignment',
					dcf_implementing_unit.form_2_name_owner_manager,
					dcf_implementing_unit.form_2_sex_owner_manager,
					dcf_implementing_unit.form_2_sector_owner_manager,
					dcf_implementing_unit.form_2_businessname,
					dcf_implementing_unit.form_2_business_owner_manager,
					dcf_implementing_unit.form_2_partner_fo_engaged,
					dcf_implementing_unit.form_2_chairperson_manager,
					dcf_implementing_unit.form_2_sex_chairperson_manager,
					dcf_implementing_unit.form_2_sector_chairperson_manager,
					dcf_implementing_unit.form_2_office_address_province,
					dcf_implementing_unit.form_2_total_number_fo,
					dcf_implementing_unit.form_2_male,
					dcf_implementing_unit.form_2_female,
					dcf_implementing_unit.form_2_pwde,
					dcf_implementing_unit.form_2_youth,
					dcf_implementing_unit.form_2_ip,
					dcf_implementing_unit.form_2_sc,
					dcf_implementing_unit.form_2_hectares_covered,
					dcf_implementing_unit.form_2_cpa_date_signing,
					dcf_implementing_unit.form_2_cpa_date_expiration,
					dcf_implementing_unit.form_2_days_remaining,
					dcf_implementing_unit.form_2_date_renewed,
					dcf_implementing_unit.form_2_notable_cpa_incentives,
					CONCAT(dcf_implementing_unit.form_2_remarks_status,
					 ' ',
					 dcf_implementing_unit.form_2_remarks_status_why) AS 'remark_status',
					dcf_implementing_unit.form_2_activity_agreements,
					dcf_implementing_unit.form_2_date_conducted,
					dcf_implementing_unit.date_created,
					dcf_implementing_unit.date_modified,
					users.name as 'Uploaded by' 
					FROM dcf_implementing_unit
					INNER JOIN users ON `dcf_implementing_unit`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form2_exported_file', index=False)
					new_column_names = 'ID,RCUs,PCUs,Commodity,DIP Alignment,Name of Owner or Manager of the anchor Firm/MSMEs,Sex of the Owner or Manager of the anchor Firm/MSMEs,Sector of Owner or manager of the anchor firm/MSMEs,Business Name,Business Address of Owner or manager of the anchor firm/MSMEs,Name of Partner FOs Engaged,Chairperson or Manager of Partner FO,Sex of the Chairperson or Manager of Partner FO,Sector of Chairperson or Manager of Partner FO,Office Address/ Province of FO,Total number of FO members,Total number of FO members Male,Total number of FO members Female,Total number of FO members - PWD,Total number of FO members - Youth,Total number of FO members - IP,Total number of FO members - SC,Hectares Covered,Date of CPA Signing,CPA Expiration Date,Days Remaining,Date Renewed,Notable CPA incentives (Optional entry),Remarks/Status,Activity/Agreements (Outputs vis-à-vis signed CPA),Date conducted/implemented,Date Created,Date Modified, Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form2_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx')
			return form2export()
		elif export_type == 'form3export':
			def form3export():
				if request.method == "POST":
					query= db.select('''SELECT dcf_bdsp_reg.id,
					dcf_bdsp_reg.form_3_types_of_bdsp,
					dcf_bdsp_reg.form_3_contact_person,
					dcf_bdsp_reg.form_3_sex,
					dcf_bdsp_reg.form_3_office_addr,
					dcf_bdsp_reg.form_3_email,
					dcf_bdsp_reg.form_3_breif_description,
					dcf_bdsp_reg.phone,
					dcf_bdsp_reg.form_3_choices,
					dcf_bdsp_reg.form_3_preferred_region,
					dcf_bdsp_reg.form_3_preferred_province,
					dcf_bdsp_reg.form_3_name,
					dcf_bdsp_reg.form_3_education,
					dcf_bdsp_reg.form_3_expertise,
					dcf_bdsp_reg.form_3_prior_rapid_engagements,
					dcf_bdsp_reg.form_3_rapid_implementing_unit,
					dcf_bdsp_reg.form_3_nature_engagements,
					dcf_bdsp_reg.form_3_suppliers_evaluation,
					dcf_bdsp_reg.form_3_other_engagement_outside_rapid,
					dcf_bdsp_reg.form_3_lecture_training_seminar,
					dcf_bdsp_reg.form_3_training_materials,
					dcf_bdsp_reg.form_3_organize_pool,
					dcf_bdsp_reg.form_3_demand_basis,
					dcf_bdsp_reg.form_3_extension_service_facilitation,
					dcf_bdsp_reg.form_3_philgeps_registered,
					dcf_bdsp_reg.date_created,
					dcf_bdsp_reg.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_bdsp_reg
					INNER JOIN users ON `dcf_bdsp_reg`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form3_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form3_exported_file', index=False)
					new_column_names = 'ID,Types of BDSP, Contact Person, Sex, Office/Main Address, Email Address, Brief Description of Company Institution and/or Consultant Background, Tel/Cellphone number,Field of Expertise, Preferred Region to work in for RAPID, Preferred Province to work in for RAPID, Name, Education, Expertise, Prior RAPID Engagements?, RAPID Implementing Unit, Type/Nature of Engagements, Suppliers Evaluation (Refer to ISO/Procurement ratings),	Other engagement outside RAPID, Willing to conduct on-line lecture/training/seminar?, Willing to develop modular video training materials?, Willing to join other providers as organize pool of service providers?, Willing to be a mentor/coach on demand basis?, Willing to be part of long-term engagement for extension service facilitation?, Philgeps Registered,Date Created, Date Modified, Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form3_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form3_exported_file.xlsx')
			return form3export()
		
		elif export_type == 'form4export':
			def form4export():
				if request.method == "POST":
					query= db.select('''SELECT dcf_capacity_building.id,
					dcf_capacity_building.cbb_implementing_unit,
					dcf_capacity_building.cbb_activity_title,
					dcf_capacity_building.cbb_types_of_training,
					dcf_capacity_building.cbb_topic_of_training,
					dcf_capacity_building.cbb_dip_approved_alignment,
					dcf_capacity_building.cbb_name_of_dip,
					dcf_capacity_building.cbb_date_start,
					dcf_capacity_building.cbb_date_end,
					dcf_capacity_building.cbb_total_number_of_participants,
					CONCAT(dcf_capacity_building.cbb_commodity,
					 ' ',
					 dcf_capacity_building.cbb_commodity_others) AS 'Commodity',
					dcf_capacity_building.cbb_venue,
					dcf_capacity_building.cbb_name_of_resource_person,
					dcf_capacity_building.cbb_rapid_actual_budget,
					dcf_capacity_building.cbb_dip_capbuild_activities_NPO,
					dcf_capacity_building.cbb_dip_capbuild_activities_CA,
					dcf_capacity_building.cbb_total_number_per_gender_male,
					dcf_capacity_building.cbb_total_number_per_gender_female,
					dcf_capacity_building.cbb_total_number_per_gender_total,
					dcf_capacity_building.cbb_total_number_per_sector_pwd,
					dcf_capacity_building.cbb_total_number_per_sector_youth,
					dcf_capacity_building.cbb_total_number_per_sector_ip,
					dcf_capacity_building.cbb_total_number_per_sector_sc,
					dcf_capacity_building.cbb_total_number_per_sector_total,
					dcf_capacity_building.cbb_results_of_activity_pre_test,
					dcf_capacity_building.cbb_results_of_activity_post_test,
					dcf_capacity_building.cbb_client_feedback_survey_rating,
					dcf_capacity_building.cbb_client_feedback_survey_comments_AOI,
					dcf_capacity_building.date_created,
					dcf_capacity_building.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_capacity_building
					INNER JOIN users ON `dcf_capacity_building`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form4_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form4_exported_file', index=False)
					new_column_names = 'ID,Implementing Unit, Activity Title, Types of Training, Topic Of Training, DIP approved alignment, Name of DIPs, ACTIVITY DURATION (start date), ACTIVITY DURATION (end date), Total Number of Participants, Commodity, Venue, Name of Resource Person/Facilitator/BDSP (First Name Middle Name Last Name), RAPID Actual Budget Actual (CY 2022 Onwards e.g. 34000.00),Name of Partner/Organization, Counterpart Amount(monetize & estimates), Male, Female, Total, PWD, Youth, IP, SC, Total, Pre-Test, Post-Test, Rating, Comments/ Areas of Improvement,Date Created, Date Modified, Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form4_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form4_exported_file.xlsx')
			return form4export()
		
		elif export_type == 'form5export':
			def form5export():
				if request.method == "POST":
					query= db.select('''SELECT  dcf_matching_grant.id,
					CONCAT(dcf_matching_grant.mgit_implementing_unit,
					 ' ',
					 dcf_matching_grant.mgit_implementing_unit_rcu,
					 ',
					 ' ,
					 dcf_matching_grant.mgit_implementing_unit_pcu) AS 'Implementing_unit',
					dcf_matching_grant.mgit_name_of_dip,
					dcf_matching_grant.mgit_msme_recipient,
					dcf_matching_grant.mgit_total_member_recipient,
					dcf_matching_grant.mgit_commodity,
					dcf_matching_grant.mgit_total_number_fo_gender_male,
					dcf_matching_grant.mgit_total_number_fo_gender_female,
					dcf_matching_grant.mgit_total_number_fo_sectoral_pwd,
					dcf_matching_grant.mgit_total_number_fo_sectoral_youth,
					dcf_matching_grant.mgit_total_number_fo_sectoral_IP,
					dcf_matching_grant.mgit_total_number_fo_sectoral_SC,
					dcf_matching_grant.mgit_type_of_investment,
					dcf_matching_grant.mgit_total_mgas_based_approved_DIP,
					dcf_matching_grant.mgit_total_mgas_signed,
					dcf_matching_grant.mgit_total_mgas_not_yet_signed,
					dcf_matching_grant.mgit_total_matching_grant_based_on_approved_business,
					dcf_matching_grant.mgit_pmga_first_availment,
					dcf_matching_grant.mgit_mgar_period_date,
					dcf_matching_grant.mgit_remaining_matching_grant_balance,
					dcf_matching_grant.mgit_inclusive_timeline_implementation_start,
					dcf_matching_grant.mgit_inclusive_timeline_implementation_end,
					dcf_matching_grant.mgit_time_elapse,
					dcf_matching_grant.mgit_total_budget_approved_in_the_DIP,
					dcf_matching_grant.mgit_actual_cost_of_procurement,
					dcf_matching_grant.mgit_summary_of_actual_tools_procured,
					dcf_matching_grant.mgit_inclusive_timeline_implementation_start1,
					dcf_matching_grant.mgit_inclusive_timeline_implementation_end1,
					dcf_matching_grant.mgit_time_elapse1,
					dcf_matching_grant.mgit_date_of_distribution,
					dcf_matching_grant.mgit_remarks_on_the_deliverd_tools,
					dcf_matching_grant.date_created,
					dcf_matching_grant.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_matching_grant
					INNER JOIN users ON `dcf_matching_grant`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form5_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form5_exported_file', index=False)
					new_column_names = 'ID,Implementing Unit, Name Of DIP,Name of FO/MSME RECIPIENT(type name of FO / MSME), total # of FO Member Recipients, Commodity,Total number of FO members by Gender Male, Total number of FO members by Gender Female,Total number of FO members by sectoral group PWD,Total number of FO members by sectoral group Youth, Total number of FO members by sectoral group IP,Total number of FO members by sectoral group SC,Type of Investment,TOTAL OF MGAs based on approved DIP,Total of MGAs Signed,Total of MGAs not yet signed,TOTAL MATCHING GRANT BASED ON APPROVED BUSINESS PLAN (IN PHP),PREVIOUS MATCHING GRANT AVAILMENT (IN PHP) - FIRST AVAILMENT,MATCHING GRANT AVAILMENT AS OF THIS REPORTING PERIOD(in PHP) and date,REMAINING MATCHING GRANT BALANCE (in PHP), INCLUSIVE TIMELINE OF IMPLEMENTATION (based on MGA) Start,INCLUSIVE TIMELINE OF IMPLEMENTATION (based on MGA) End,Time elapse,Total budget as approved in the DIP,actual cost of procurement,summary of actual tools procured,Inclusive timeline of implementation (based on MGA) Start,Inclusive timeline of implementation (based on MGA) End,time elapse,DATE of distribution/training,Remarks delivered tools,Date Created,Date Modified,Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form5_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form5_exported_file.xlsx')
			return form5export()
		
		elif export_type == 'form6export':
			def form6export():
				if request.method == "POST":
					query = db.select('''SELECT dcf_product_development.id,
					dcf_product_development.form_6_implementing_unit,
					dcf_product_development.form_6_type_of_assisstance,
					dcf_product_development.form_6_type_of_activity,
					dcf_product_development.form_6_dip_alignment,
					dcf_product_development.form_6_activity_duration_start,
					dcf_product_development.form_6_activity_duration_end,
					dcf_product_development.form_6_venue,
					dcf_product_development.form_6_resource_person,
					dcf_product_development.form_6_rapid_actual_budget,
					dcf_product_development.form_6_name_of_partner_organization_1,
					dcf_product_development.form_6_name_of_partner_organization_2,
					dcf_product_development.form_6_beneficiary_participant,
					dcf_product_development.form_6_commodity,
					dcf_product_development.form_6_type_of_beneficiary,
					dcf_product_development.form_6_sex,
					dcf_product_development.form_6_sector,
					dcf_product_development.form_6_product_developed,
					dcf_product_development.form_6_date_launched_to_market,
					dcf_product_development.form_6_improved_product,
					dcf_product_development.form_6_type_of_product_improvement,
					dcf_product_development.form_6_name_of_product_developed,
					dcf_product_development.form_6_,
					CONCAT(dcf_product_development.form_6_certification,
					 ' ',
					 dcf_product_development.form6_otherss1) AS 'certification1',
					CONCAT(dcf_product_development.form_6_certification2,
					 ' ',
					dcf_product_development.form6_otherss2) AS 'certification2',
					dcf_product_development.form_6_date_issuance,
					dcf_product_development.form_6_expiration_date,
					dcf_product_development.form_6_product_certified,
					dcf_product_development.form_6_rating,
					dcf_product_development.form_6_comment_ares_of_improvement,
					dcf_product_development.date_created,
					dcf_product_development.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_product_development
					INNER JOIN users ON `dcf_product_development`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form6_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form6_exported_file', index=False)
					new_column_names = 'ID,Implementing Unit,Type of Assistance,Type of Activity,DIP Alignment,Activity Duration Start Date,Activity Duration End Date,Venue,Name of Resource Person/Facilitator/BDSP,RAPID Actual Budget,Name of Partner/Organization,Name of Partner/Organization,Name of Beneficiary/Participant,Commodity,Type of Beneficiary,Sex,Sector,Name of Product Developed,Date Launched to Market,Name of Improved Product,Type of Product Improvement,Name the System/Process Established/Improved,Date of Establishment/ Adoption,Name/Title of Certifications Facilitated,Name/Title of Certifications Acquired,Date of Issuance,Expiration Date,Product Certified,Rating,Comments/Areas of Improvement,Date Created,Date Modified,Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form6_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form6_exported_file.xlsx')

			return form6export()
		
		elif export_type == 'form7export':
			def form7export():
				if request.method == "POST":
					query = db.select('''SELECT dcf_trade_promotion.id,
					dcf_trade_promotion.form_7_implementing_unit,
					dcf_trade_promotion.form_7_title_trade_promotion,
					dcf_trade_promotion.form_7_type_of_trade_promotion,
					dcf_trade_promotion.form_7_dip_indicate,
					dcf_trade_promotion.form_7_start_date,
					dcf_trade_promotion.form_7_end_date,
					dcf_trade_promotion.form_7_name_of_po,
					dcf_trade_promotion.form_7_amount,
					dcf_trade_promotion.form_7_venue,
					dcf_trade_promotion.form_7_rapid_actual_budget,
					dcf_trade_promotion.form_7_name_of_beneficiary,
					CONCAT(dcf_trade_promotion.form_7_commodity,
					 ' ',
					 dcf_trade_promotion.form_7_commodity_others) AS 'Commodity',
					dcf_trade_promotion.form_7_beneficiary,
					dcf_trade_promotion.form_7_sex,
					dcf_trade_promotion.form_7_sector,
					dcf_trade_promotion.form_7_type_of_products,
					dcf_trade_promotion.form_7_name_of_buyer,
					dcf_trade_promotion.form_7_cash_sales,
					dcf_trade_promotion.form_7_booked_sales,
					dcf_trade_promotion.form_7_under_negotiations,
					dcf_trade_promotion.form_7_total_autosum,
					dcf_trade_promotion.date_created,
					dcf_trade_promotion.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_trade_promotion
					INNER JOIN users ON `dcf_trade_promotion`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form7_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form7_exported_file', index=False)
					new_column_names = 'ID,Implementing Unit,Title of Trade Promotion Services Provided,Type of Trade Promotion Services organized/participated,DIP (indicate NO if none),Start Date,End Date,Name of Partner/Organization,Amount,Venue,RAPID Actual Budget,Name of Beneficiary,Commodity,Type of Beneficiary,Sex,Sector,Type of Product(s),Name of Buyer/Company Matched with Assisted MSMEs/FOs,Cash Sales,Booked Sales,Under Negotiations,Total,Date Created,Date Modified,Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form7_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form7_exported_file.xlsx')

			return form7export()
		
		elif export_type == 'form9export':
			def form9export():
				if request.method == "POST":
					query = db.select('''SELECT dcf_enablers_activity.id,
					dcf_enablers_activity.form_9_implementing_unit,
					dcf_enablers_activity.form_9_title_trade_promotion,
					CONCAT(dcf_enablers_activity.form_9_type_of_training,
					 ' ',
					 dcf_enablers_activity.form_9_othertypetraining ) AS 'type_of_training',
					dcf_enablers_activity.form_9_start_date,
					dcf_enablers_activity.form_9_end_date,
					dcf_enablers_activity.form_9_venue,
					dcf_enablers_activity.form_9_rapid_actual_budget,
					dcf_enablers_activity.form_9_name_of_resource_person,
					dcf_enablers_activity.form_9_name_of_participant_org,
					dcf_enablers_activity.form_9_counterpart_amount,
					dcf_enablers_activity.form_9_name_of_participant,
					dcf_enablers_activity.form_9_sex,
					dcf_enablers_activity.form_9_sector,
					dcf_enablers_activity.form_9_organization,
					dcf_enablers_activity.form_9_designation,
					dcf_enablers_activity.form_9_pre_test1,
					dcf_enablers_activity.form_9_post_test1,
					dcf_enablers_activity.form_9_activity_output,
					dcf_enablers_activity.form_9_pre_test2,
					dcf_enablers_activity.form_9_post_test2,
					dcf_enablers_activity.form_9_rating,
					dcf_enablers_activity.form_9_comments,
					dcf_enablers_activity.date_created,
					dcf_enablers_activity.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_enablers_activity
					INNER JOIN users ON `dcf_enablers_activity`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form9_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form9_exported_file', index=False)
					new_column_names = 'ID,Implementing Unit,Activity Title,Type of Training/Activity,Start Date,End Date,Venue,RAPID actual budget,Name of Resource Person/Facilitator/BDSP,Name of Partner/Organization,Counterpart Amount,Name of Participant,Sex,Sector,Organization,Designation,Results of activity Pre-test,Results of activity Post-test,Activity Output,Results of activity (Average if applicable/ indicate NA option) Pre-test,Results of activity (Average if applicable/ indicate NA option) Post-test,Rating,Comments/Areas of Improvement,Date Created,Date Modified,Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form9_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form9_exported_file.xlsx')

			return form9export()
		
		elif export_type == 'form10export':
			def form10export():
				if request.method == "POST":
					query = db.select('''SELECT dcf_negosyo_center.id,
					dcf_negosyo_center.form_10_nc_location,
					dcf_negosyo_center.form_10_name_of_nc,
					dcf_negosyo_center.form_10_title_of_rapid_activity,
					dcf_negosyo_center.form_10_type_of_assistance,
					dcf_negosyo_center.form_10_date,
					dcf_negosyo_center.form_10_type_of_beneficiary,
					dcf_negosyo_center.form_10_sex_male,
					dcf_negosyo_center.form_10_sex_female,
					dcf_negosyo_center.form_10_commodity,
					dcf_negosyo_center.date_created,
					dcf_negosyo_center.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_negosyo_center
					INNER JOIN users ON `dcf_negosyo_center`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form10_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form10_exported_file', index=False)
					new_column_names = 'ID,NC Location,Name of NC,Title of RAPID Activity,Type of Assistance Provided,Date,Type of beneficiary,Male,Female,Commodity,Date Created,Date Modified, Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form10_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form10_exported_file.xlsx')

			return form10export()
		
		elif export_type == 'form11export':
			def form11export():
				if request.method == "POST":
					query = db.select('''SELECT dcf_access_financing.id,
					CONCAT(dcf_access_financing.form_11_dip_alignment,
					 ' ',
					 dcf_access_financing.form_11_dip_alignment_yes) AS 'form11_dip',
					dcf_access_financing.form_11_activity_title,
					dcf_access_financing.form_11_name_of_beneficiary,
					CONCAT(dcf_access_financing.form_11_industry_cluster,
					 ' ',
					 dcf_access_financing.form_11_industry_pfn) AS 'industry_cluster',
					dcf_access_financing.form_11_msme_regional,
					dcf_access_financing.form_11_msme_province,
					dcf_access_financing.form_11_male,
					dcf_access_financing.form_11_female,
					dcf_access_financing.form_11_pwd,
					dcf_access_financing.form_11_youth,
					dcf_access_financing.form_11_ip,
					dcf_access_financing.form_11_sc,
					dcf_access_financing.form_11_date_submitted,
					dcf_access_financing.form_11_date_approved,
					dcf_access_financing.form_11_name_of_fsp,
					dcf_access_financing.form_11_location_address,
					dcf_access_financing.form_11_amount_of_equity,
					dcf_access_financing.form_11_date_released,
					dcf_access_financing.date_created,
					dcf_access_financing.date_modified,
					users.name as 'Uploaded by'
					FROM dcf_access_financing
					INNER JOIN users ON `dcf_access_financing`.`upload_by` = `users`.`id` {}'''.format(position_data_filter()))
					df_nested_list = pd.json_normalize(query)
					df = pd.DataFrame(df_nested_list)
					df = df.astype(str)
					writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form11_exported_file.xlsx') 
					df.to_excel(writer, sheet_name='dcf_form11_exported_file', index=False)
					new_column_names = 'ID,DIP Alignment,Activity Title,Name of Beneficiary (Registered Business/FO Name),Industry Cluster,Region,Province,Male,Female,PWD,Youth,IP,SC,Date Submitted to FSP,Date Approved,Name of FSP,Location/Address,Amount of Equity Financing Approved/Accessed,Date Released,Date Created,Date Modified,Uploaded by'
					new_column_names_list = new_column_names.split(',')
					df.columns = new_column_names_list

					workbook = writer.book
					worksheet = writer.sheets['dcf_form11_exported_file']
					header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#00ace6', 'border': 1})
					
					for col_num, value in enumerate(df.columns.values):
						worksheet.write(0, col_num, value, header_format)
						column_width = max(df[value].astype(str).apply(len).max(), len(value)) + 1
						worksheet.set_column(col_num, col_num, column_width)
					
					writer.save()
					return send_file(c.RECORDS+'/objects/_temp_/dcf_form11_exported_file.xlsx')

			return form11export()
		
	else:
		return redirect('dcfspreadsheet.html')

# =========================================================================

@app.route('/get_data/<ids>/<dbs>', methods = ['POST','GET'])
def get_data(ids,dbs):
	res = db.select("SELECT * FROM `{}` WHERE `id`='{}';".format(dbs,ids))   
	return res


@app.route('/set_data/<table>', methods = ['POST','GET'])
def set_data(table):
	form_data = request.form
	col = "";val = "";args = ""

	is_exist = len(db.select("SELECT * FROM `{}` WHERE `id` ='{}' ;".format(table,request.form['id'])))
	if(is_exist==0):
		print("Adding")
		for data_ in form_data:
			col += ",`{}`".format(data_)
			val += ",'{}'".format(form_data[data_])
		sql = "INSERT INTO `{}` (`upload_by`,{}) VALUES ('{}',{})".format(table,col[1:], session["USER_DATA"][0]["id"], val[1:])
	else:
		print("Editing")
		for data_ in form_data:
			args += ",`{}`='{}'".format(data_,form_data[data_])
		sql = "UPDATE `{}` SET {},date_modified=CURRENT_TIMESTAMP WHERE `id`='{}';".format(table,args[1:],request.form['id'])
		pass

	last_row_id ="None"
	status = "Unfinished"
	msg = "Unfinished"
	try:
		last_row_id = db.do(sql)
		status = "success"
		msg = "Data was added to the database"
	except Exception as e:
		status = "failed"
		msg = "[{}]".format(e)
		last_row_id ="None"
	res__ = {"status":status,"msg":msg,"id":last_row_id}
	return jsonify(res__)

@app.route('/delete_record/<table>/<ids>', methods = ['POST','GET'])
def delete_record(table,ids):
	sql='DELETE FROM `{}` WHERE id = {}'.format(table,ids)
	delete=db.do(sql)
	if(delete["response"]=="error"):
			print(str(delete))
			flash(f"An error occured !", "error") 
	else:
			print(str(delete))
			flash(f"The data was deleted successfully!", "success")
	return redirect("/{}dashboard".format(FORM_NAME[table]))

FORM_NAME={
	'dcf_prep_review_aprv_status' : 'form1_',
	'dcf_implementing_unit' : 'form2_',
	'dcf_bdsp_reg' : 'form3_',
	'dcf_capacity_building' : 'form4_',
	'dcf_matching_grant' : 'form5_',
	'dcf_product_development' : 'form6_',
	'dcf_trade_promotion' : 'form7_',
	'form8' : 'form8_',
	'dcf_enablers_activity' : 'form9_',
	'dcf_negosyo_center' : 'form10_',
	'dcf_access_financing' : 'form11_',
	'form_c' : 'formc',
}
# if __name__ == "__main__":
#     app.run(debug=True)

def position_data_filter():
	_filter = "WHERE 1 "
	JOB = session["USER_DATA"][0]["job"].lower()

	if(JOB in "admin" or JOB in "super admin"):
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