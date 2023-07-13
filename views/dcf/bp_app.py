from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file
from decimal import Decimal
import pandas as pd
from tqdm import tqdm
from time import sleep
import xlrd
import json
from werkzeug.utils import secure_filename
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

db = mysql(*c.DB_CRED)
db.err_page = 0
app = Blueprint("dcf",__name__,template_folder="pages")

def is_on_session(): return ('USER_DATA' in session)

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
	return redirect("/dcf_spreadsheet")
#-------------------------------------------------------------------------------


@app.route('/dcf', methods=['GET', 'POST'])
def dcfexport_data():
    if request.method == 'POST':
        export_type = request.form.get('export_type')
        if export_type == 'form1export':
            def form1export():
                if request.method == "POST":
                    query= db.select("SELECT form_1_rcus,form_1_number_of_dips,form_1_anchor_firm,form_1_size_of_anchor,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_namefo,form_1_totalmsme,form_1_total_farmerbene,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalcost_prodinvest,form_1_total_matching_grant,form_1_capbuilding,form_1_supply_chain_manager,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms FROM dcf_prep_review_aprv_status")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form1_exported_file', index=False)
                    new_column_names = 'RCUs, Number Of DIPs, Anchor Firm, Size Of Anchor, Commodity, Scope/Provinces, For development(indicate date), Date: CN Approved, Date:Full BPs and DIPs Finalized/Approved by RCUs and endorsed to NPCO for Review, Date of the Parallel Review with NPCO/RGMS-IFAD-RTWG, Date of submission of the revised DIPs based on the comments from the parallel review, Date of RTWG Approval, Date: NPCO cursory review of RCUs compliance to parallel review comments and DIP endorsement to NOTUS Uploading, Date: Uploading to IFAD NOTUS c/o NPCO, Date: IFAD NO Issuance, Total # of FOs, Total # of MSMEs, Total # of farmer beneficiaries, Total Hectarage Covered, Hectares for Rehab, Total Cost of Rehab, Hectares for Expansion, Total Cost of Expansion, Total Cost of Productive Investments(equipment/facilities/warehouse), Total Matching Grant(AA+AB), Capacity Building (Organizational+Technical trainings: post-production and etc.), Supply Chain Manager, Total Project Cost (Y+AC+AD+AE), FMI, FMI Kms'
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
                    query= db.select("SELECT form_2_rcus,form_2_pcu,form_2_commodity,form_2_dip_alignment,form_2_yes,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_remarks_status,form_2_activity_agreements,form_2_date_conducted FROM dcf_implementing_unit")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form2_exported_file', index=False)
                    new_column_names = 'RCUs,PCU, Commodity, DIP Alignment: (If Yes, select Yes and type the name of the Anchor Firm/DIP Name and Select No for no DIP alignment), Name of Owner or Manager of the anchor Firm, Sex of the Owner or Manager of the anchor Firm,Sector of Owner or manager of the anchor firm, Business Address of Owner or manager of the anchor firm,Name of Partner FOs engaged (Full Official Name with Abbreviation),Chairperson or Manager of Partner FO,Sex of the Chairperson or Manager of the anchor Firm, Sector of Chairperson or manager of the anchor firm,Office Address/ Province of FO,Total number of FO members,Male,Female, PWD,Youth,IP,SC,Address of FO Members, Hectares Covered,Date of CPA Signing,CPA Expiration Date,Days Remaining,Date Renewed, Notable CPA incentives(Optional entry), Remarks/Status, Activity/Agreements (Outputs vis-à-vis signed CPA),Date conducted/implemented'
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
                    query= db.select("SELECT form_3_types_of_bdsp,form_3_contact_person,form_3_training_number,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered FROM dcf_bdsp_reg")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form3_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form3_exported_file', index=False)
                    new_column_names = 'Types of BDSP,Contact Person,Training Number,Sex,Office/Main Address,Email Address,Brief Description of Company Institution and/or Consultant Background,Phone number,Field of Expertise,Preferred Region to work in for RAPID,Preferred Province to work in for RAPID,Name,Education,Expertise,Prior RAPID Engagements?,Date Registered,RAPID Implementing Unit,Type/Nature of Engagements,Suppliers Evaluation(Refer to ISO/Procurement ratings),other engagement outside RAPID,Willing to conduct on-line lecture/training/seminar?,Willing to develop modular video training materials?,Willing to join other providers as organize pool of service providers?,Willing to be a mentor/coach on demand basis?,Willing to be part of long-term engagement for extension service facilitation?,Philgeps Registered'
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
                    query= db.select("SELECT cbb_implementing_unit,cbb_training_number,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_total_number_of_participants,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_of_beneficiaries_per_type,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI FROM dcf_capacity_building")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form4_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form4_exported_file', index=False)
                    new_column_names = 'Implementing Unit,Training Number, Activity Title,Types of Training , Topic Of Training,  -approved alignment,Name of DIP, ACTIVITY DURATION (Day/Month/Year) Start,ACTIVITY DURATION (Day/Month/Year) End,Total Number of Participants, Commodity,Venue,Name of Resource Person/Facilitator/BDSP(First Name/Middle Name/Last Name),RAPID Actual Budget Actual (CY 2022 Onwards e.g. 34000.00),Name of Partner/Organization,Counterpart Amount(monetize & estimates),Total number of beneficiaries per type,Total Number Per Gender male,Total Number Per Gender female,Total Number Gender, Total Number Per Sector-PWD,Total Number Per Sector-Youth,Total Number Per Sector-IP,Total Number Per Sector-SC,Total Number Sector, Results of activity (Average) Pre-test,Results of activity (Average) Post-Test, Client Feedback Survey Rating, Client Feedback Survey Comments/ Areas of Improvement'
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
                    query= db.select("SELECT mgit_implementing_unit_rcu,mgit_implementing_unit_pcu,mgit_name_of_dip,mgit_msme_recipient,mgit_total_member_recipient,mgit_commodity,mgit_total_number_fo_gender_male,mgit_total_number_fo_gender_female,mgit_total_number_fo_sectoral_pwd,mgit_total_number_fo_sectoral_youth,mgit_total_number_fo_sectoral_IP,mgit_total_number_fo_sectoral_SC,mgit_type_of_investment,mgit_total_mgas_based_approved_DIP,mgit_total_mgas_signed,mgit_total_mgas_not_yet_signed,mgit_total_matching_grant_based_on_approved_business,mgit_pmga_first_availment,mgit_mgar_period_date,mgit_remaining_matching_grant_balance,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_budget_approved_in_the_DIP,mgit_actual_cost_of_procurement,mgit_summary_of_actual_tools_procured,mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_date_of_distribution,mgit_remarks_on_the_deliverd_tools FROM dcf_matching_grant")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form5_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form5_exported_file', index=False)
                    new_column_names = 'Implementing Unit RCU,Implementing Unit PCU, Name Of DIP,Name of FO/MSME RECIPIENT(type name of FO / MSME), total # of FO Member Recipients, Commodity,Total number of FO members by Gender Male, Total number of FO members by Gender Female,Total number of FO members by sectoral group PWD,Total number of FO members by sectoral group Youth, Total number of FO members by sectoral group IP,Total number of FO members by sectoral group SC,Type of Investment,TOTAL OF MGAs based on approved DIP,Total of MGAs Signed,Total of MGAs not yet signed,TOTAL MATCHING GRANT BASED ON APPROVED BUSINESS PLAN (IN PHP),PREVIOUS MATCHING GRANT AVAILMENT (IN PHP) - FIRST AVAILMENT,MATCHING GRANT AVAILMENT AS OF THIS REPORTING PERIOD(in PHP) and date,REMAINING MATCHING GRANT BALANCE (in PHP), INCLUSIVE TIMELINE OF IMPLEMENTATION (based on MGA) Start,INCLUSIVE TIMELINE OF IMPLEMENTATION (based on MGA) End,Time elapse,Total budget as approved in the DIP,actual cost of procurement,summary of actual tools procured,Inclusive timeline of implementation (based on MGA) Start,Inclusive timeline of implementation (based on MGA) End,time elapse,DATE of distribution/training,Remarks delivered tools'
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
                    query = db.select("SELECT form_6_implementing_unit,form_6_type_of_assisstance,form_6_type_of_activity,form_6_dip_alignment,form_6_activity_duration_start,form_6_activity_duration_end,form_6_venue,form_6_resource_person,form_6_rapid_actual_budget,form_6_name_of_partner_organization_1,form_6_name_of_partner_organization_2,form_6_beneficiary_participant,form_6_commodity,form_6_type_of_beneficiary,form_6_male,form_6_female,form_6_total_1,form_6_pwd,form_6_youth,form_6_ip,form_6_sc,form_6_total_2,form_6_product_developed,form_6_date_launched_to_market,form_6_improved_product,form_6_type_of_product_improvement,form_6_name_of_product_developed,form_6_,form_6_commodity1,form_6_commodity2,form_6_date_issuance,form_6_expiration_date,form_6_product_certified,form_6_rating,form_6_comment_ares_of_improvement FROM dcf_product_development")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form6_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form6_exported_file', index=False)
                    new_column_names = 'Implementing Unit,Type of Assistance,Type of Activity,DIP Alignment,Activity Duration Start Date,Activity Duration End Date,Venue,Name of Resource Person/Facilitator/BDSP,RAPID Actual Budget,Name of Partner/Organization,Name of Partner/Organization, Name of Beneficiary/Participant,Commodity,Type of Beneficiary,Male,Female ,Total,PWD,Youth,IP,SC,Total,Name of Product Developed,Date Launched to Market,Name of Improved Product,Type of Product Improvement,Name the System/Process Established/Improved,Date of Establishment/ Adoption,Name/Title of Certifications Facilitated,Name/Title of Certifications Acquired,Date of Issuance,Expiration Date,Product Certified,Rating,Comments/Areas of Improvement'
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
                    query = db.select("SELECT form_7_implementing_unit,form_7_title_trade_promotion,form_7_type_of_trade_promotion,form_7_dip_indicate,form_7_start_date,form_7_end_date,form_7_name_of_po,form_7_amount,form_7_venue,form_7_rapid_actual_budget,form_7_name_of_beneficiary,form_7_commodity,form_7_msme,form_7_fo,form_7_farmer,form_7_male,form_7_female,form_7_pwd,form_7_youth,form_7_ip,form_7_sc,form_7_type_of_products,form_7_name_of_buyer,form_7_cash_sales,form_7_booked_sales,form_7_under_negotiations,form_7_total_autosum FROM dcf_trade_promotion")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form7_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form7_exported_file', index=False)
                    new_column_names = 'Implementing Unit,Title of Trade Promotion Services Provided,Type of Trade Promotion Services organized/participated,DIP (indicate NO if none),Start Date,End Date,Name of Partner/Organization,Amount,Venue,RAPID Actual Budget,Name of Beneficiary (Name of farmer Registered business/FO name),Commodity,MSME,FO,Farmer,Male,Female,PWD,Youth,IP,SC,Type of Product(s),Name of Buyer/Company Matched with Assisted MSMEs/FOs,Cash Sales,Booked Sales,Under Negotiations,Total'
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
                    query = db.select("SELECT form_9_implementing_unit,form_9_title_trade_promotion,form_9_type_of_training,form_9_start_date,form_9_end_date,form_9_venue,form_9_rapid_actual_budget,form_9_name_of_resource_person,form_9_name_of_participant_org,form_9_counterpart_amount,form_9_name_of_participant,form_9_organization,form_9_designation,form_9_male,form_9_female,form_9_pwd,form_9_youth,form_9_ip,form_9_sc,form_9_pre_test1,form_9_post_test1,form_9_activity_output,form_9_pre_test2,form_9_post_test2,form_9_rating,form_9_comments FROM dcf_enablers_activity")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form9_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form9_exported_file', index=False)
                    new_column_names = 'Implementing Unit,Activity Title,Type of Training/Activity,Start Date,End Date,Venue,RAPID actual budget,Name of Resource Person/Facilitator/BDSP,Name of Partner/Organization,Counterpart Amount,Name of Participant,Organization,Designation,Male,Female,PWD,Youth,IP,SC,Pre-test,Post-test,Activity Output,Pre-test,Post-test,Rating,Comments/Areas of Improvement'
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
                    query = db.select("SELECT form_10_nc_location,form_10_name_of_nc,form_10_title_of_rapid_activity,form_10_type_of_assistance,form_10_date,form_10_type_of_beneficiary,form_10_sex_male,form_10_sex_female,form_10_commodity FROM dcf_negosyo_center")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form10_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form10_exported_file', index=False)
                    new_column_names = 'NC Location,Name of NC,Title of RAPID Activity,Type of Assistance Provided,Date,Type of beneficiary,Male,Female,Commodity'
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
                    query = db.select("SELECT form_11_dip_alignment,form_11_activity_title,form_11_name_of_beneficiary,form_11_industry_cluster,form_11_msme_regional,form_11_msme_province,form_11_male,form_11_female,form_11_pwd,form_11_youth,form_11_ip,form_11_sc,form_11_date_submitted,form_11_date_approved,form_11_name_of_fsp,form_11_location_address,form_11_amount_of_equity,form_11_date_released FROM dcf_access_financing")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame(df_nested_list)
                    df = df.astype(str)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form11_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form11_exported_file', index=False)
                    new_column_names = 'DIP Alignment,Activity Title,Name of Beneficiary (Registered Business/FO Name),Industry Cluster,Region,Province,Male,Female,PWD,Youth,IP,SC,Date Submitted to FSP,Date Approved,Name of FSP,Location/Address,Amount of Equity Financing Approved/Accessed,Date Released'
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


# if __name__ == "__main__":
#     app.run(debug=True)
