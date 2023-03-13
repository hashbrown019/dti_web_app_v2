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
from views.dcf.form_insert import insert_form1 as insertData1
from views.dcf.form_insert import insert_form3 as insertData3
from views.dcf.form_insert import insert_form2 as insertData2
from views.dcf.dashboard import dashboard_count as displayData
import Configurations as c 
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0
app = Blueprint("dcf",__name__,template_folder="pages")

def is_on_session(): return ('USER_DATA' in session)

@app.route('/dcf_dashboard')
def dcf_dashboard():
    disp = displayData.display__()
    return render_template("dcf_dashboard.html",user_data=session["USER_DATA"][0],**disp)

@app.route('/dcf_forms')
def dcf_forms():
    return redirect("/dcf_forms")

@app.route('/dcf/<form>')
def form1(form):
    return render_template('includes/forms/{}.html'.format(form),user_data=session["USER_DATA"][0])


@app.route('/dcf_spreadsheet')
def dcf_spreadsheet():
    return render_template("dcf_spreadsheet.html",user_data=session["USER_DATA"][0])

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

@app.route("/dcfspreadsheet")
def dcfspreadsheet():
    SQL ="""
SELECT dcf_prep_review_aprv_status.filename, COUNT(dcf_prep_review_aprv_status.filename) AS _COUNT, users.name
FROM `dcf_prep_review_aprv_status`
JOIN `users` ON dcf_prep_review_aprv_status.upload_by = users.id
WHERE dcf_prep_review_aprv_status.upload_by = {}
GROUP BY dcf_prep_review_aprv_status.filename;
""".format(session["USER_DATA"][0]['id'])
    uploaded_file_by_user = db.select(SQL)
    return render_template("dcf_spreadsheet.html",user_data=session["USER_DATA"][0],uploaded_file_by_user=uploaded_file_by_user)

@app.route('/form1export',methods = ['POST'])

def form1export():
    if request.method == "POST":
        query= db.select("SELECT form_1_rcus,form_1_number_of_dips, form_1_anchor_firm, form_1_size_of_anchor, form_1_commodity, form_1_scope_provinces,form_1_for_development, form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review, form_1_date_of_submission, form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad, form_1_date_of_ifad_no_inssuance,form_1_totalmsme, form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov, form_1_hect_rehab, form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_facilities, form_1_warehouse, form_1_total_matching_grant, form_1_organizational, form_1_technical_trainings, form_1_post_production, form_1_others,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad, form_1_ae,form_1_fmi,form_1_fmi_kms FROM dcf_prep_review_aprv_status")

    df_nested_list = pd.json_normalize(query)
    df = pd.DataFrame (df_nested_list)
    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx') 
    df.to_excel(writer, sheet_name='dcf_form1_exported_file',index=False )
    new_column_names = 'RCUs,Number Of DIPs, Anchor Firm, Size Of Anchor, Commodity, Scope/Provinces,For development (indicate date), Date: CN Approved,Date: Full BPs and DIPs Finalized/Approved by RCUs and endorsed to NPCO for Review,Date of the Parallel Review with NPCO/RGMS-IFAD-RTWG, Date of submission of the revised DIPs based on the comments from the parallel review, Date of RTWG Approval,Date: NPCO cursory review of RCUs compliance to parallel review comments; and DIP endorsement to NOTUS Uploading,Date: Uploading to IFAD NOTUS c/o NPCO, Date: IFAD NO Issuance,Total # of MSMEs, Total # of farmer beneficiaries,Total # of FOs,Input Name of FO,Total Hectarage Covered, Hectares for Rehab, Total Cost of Rehab,Hectares for Expansion,Total Cost of Expansion,Equipment,Facilities, Warehouse, Total Matching Grant (AA+AB), Organizational, Technical Trainings, Post-Production, Others,Supply Chain Manager,Y,AC,AD, AE,FMI,FMI Kms'
    new_column_names_list = new_column_names.split(',')
    df.columns = new_column_names_list
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['dcf_form1_exported_file'].set_column(col_idx, col_idx, column_width);

    
    workbook  = writer.book
    worksheet = writer.sheets['dcf_form1_exported_file']
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.save()
    return send_file(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx')

@app.route('/form2export',methods = ['POST'])

def form2export():
    if request.method == "POST":
        query= db.select("SELECT form_2_rcus,form_2_pcu,form_2_commodity,form_2_dip_alignment,form_2_yes,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_remarks_status,form_2_activity_agreements,form_2_date_conducted FROM dcf_implementing_unit")

    df_nested_list = pd.json_normalize(query)
    df = pd.DataFrame (df_nested_list)
    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx') 
    df.to_excel(writer, sheet_name='dcf_form2_exported_file',index=False )
    new_column_names = 'RCUs,Number Of DIPs, Anchor Firm, Size Of Anchor, Commodity, Scope/Provinces,For development (indicate date), Date: CN Approved,Date: Full BPs and DIPs Finalized/Approved by RCUs and endorsed to NPCO for Review,Date of the Parallel Review with NPCO/RGMS-IFAD-RTWG, Date of submission of the revised DIPs based on the comments from the parallel review, Date of RTWG Approval,Date: NPCO cursory review of RCUs compliance to parallel review comments; and DIP endorsement to NOTUS Uploading,Date: Uploading to IFAD NOTUS c/o NPCO, Date: IFAD NO Issuance,Total # of MSMEs, Total # of farmer beneficiaries,Total # of FOs,Input Name of FO,Total Hectarage Covered, Hectares for Rehab, Total Cost of Rehab,Hectares for Expansion,Total Cost of Expansion,Equipment,Facilities, Warehouse, Total Matching Grant (AA+AB), Organizational, Technical Trainings, Post-Production, Others,Supply Chain Manager,Y,AC,AD, AE,FMI,FMI Kms'
    new_column_names_list = new_column_names.split(',')
    df.columns = new_column_names_list
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['dcf_form2_exported_file'].set_column(col_idx, col_idx, column_width);

    
    workbook  = writer.book
    worksheet = writer.sheets['dcf_form2_exported_file']
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.save()
    return send_file(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx')

@app.route('/', methods=['GET', 'POST'])
def dcfexport_data():
    if request.method == 'POST':
        export_type = request.form.get('export_type')
        if export_type == 'form1export':
            def form1export():
                if request.method == "POST":
                    query= db.select("SELECT form_1_rcus,form_1_number_of_dips, form_1_anchor_firm, form_1_size_of_anchor, form_1_commodity, form_1_scope_provinces,form_1_for_development, form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review, form_1_date_of_submission, form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad, form_1_date_of_ifad_no_inssuance,form_1_totalmsme, form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov, form_1_hect_rehab, form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_facilities, form_1_warehouse, form_1_total_matching_grant, form_1_organizational, form_1_technical_trainings, form_1_post_production, form_1_others,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad, form_1_ae,form_1_fmi,form_1_fmi_kms FROM dcf_prep_review_aprv_status")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame (df_nested_list)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form1_exported_file',index=False )
                    new_column_names = 'RCUs,Number Of DIPs, Anchor Firm, Size Of Anchor, Commodity, Scope/Provinces,For development (indicate date), Date: CN Approved,Date: Full BPs and DIPs Finalized/Approved by RCUs and endorsed to NPCO for Review,Date of the Parallel Review with NPCO/RGMS-IFAD-RTWG, Date of submission of the revised DIPs based on the comments from the parallel review, Date of RTWG Approval,Date: NPCO cursory review of RCUs compliance to parallel review comments; and DIP endorsement to NOTUS Uploading,Date: Uploading to IFAD NOTUS c/o NPCO, Date: IFAD NO Issuance,Total # of MSMEs, Total # of farmer beneficiaries,Total # of FOs,Input Name of FO,Total Hectarage Covered, Hectares for Rehab, Total Cost of Rehab,Hectares for Expansion,Total Cost of Expansion,Equipment,Facilities, Warehouse, Total Matching Grant (AA+AB), Organizational, Technical Trainings, Post-Production, Others,Supply Chain Manager,Y,AC,AD, AE,FMI,FMI Kms'
                    new_column_names_list = new_column_names.split(',')
                    df.columns = new_column_names_list
                    for column in df:
                        column_width = max(df[column].astype(str).map(len).max(), len(column))
                        col_idx = df.columns.get_loc(column)
                        writer.sheets['dcf_form1_exported_file'].set_column(col_idx, col_idx, column_width);
                        workbook  = writer.book
                        worksheet = writer.sheets['dcf_form1_exported_file']
                        header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
                    for col_num, value in enumerate(df.columns.values):
                        worksheet.write(0, col_num, value, header_format)
                    writer.save()
                    return send_file(c.RECORDS+'/objects/_temp_/dcf_form1_exported_file.xlsx')
            return form1export()
        elif export_type == 'form2export':
            def form2export():
                if request.method == "POST":
                    query= db.select("SELECT form_2_rcus,form_2_pcu,form_2_commodity,form_2_dip_alignment,form_2_yes,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_remarks_status,form_2_activity_agreements,form_2_date_conducted FROM dcf_implementing_unit")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame (df_nested_list)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form2_exported_file',index=False )
                    new_column_names = 'RCUs,PCU, Commodity, DIP Alignment: (If Yes, select Yes and type the name of the Anchor Firm/DIP Name and Select No for no DIP alignment), Name of Owner or Manager of the anchor Firm, Sex of the Owner or Manager of the anchor Firm,Sector of Owner or manager of the anchor firm, Business Address of Owner or manager of the anchor firm,Name of Partner FOs engaged (Full Official Name with Abbreviation),Chairperson or Manager of Partner FO,Sex of the Chairperson or Manager of the anchor Firm, Sector of Chairperson or manager of the anchor firm,Office Address/ Province of FO,Total number of FO members,Male,Female, PWD,Youth,IP,SC,Address of FO Members, Hectares Covered,Date of CPA Signing,CPA Expiration Date,Days Remaining,Date Renewed, Notable CPA incentives(Optional entry), Remarks/Status, Activity/Agreements (Outputs vis-à-vis signed CPA),Date conducted/implemented'
                    new_column_names_list = new_column_names.split(',')
                    df.columns = new_column_names_list
                for column in df:
                    column_width = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['dcf_form2_exported_file'].set_column(col_idx, col_idx, column_width);
                workbook  = writer.book
                worksheet = writer.sheets['dcf_form2_exported_file']
                header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                writer.save()
                return send_file(c.RECORDS+'/objects/_temp_/dcf_form2_exported_file.xlsx')
            return form2export()
        elif export_type == 'form3export':
            def form3export():
                if request.method == "POST":
                    query= db.select("SELECT form_3_types_of_bdsp,form_3_contact_person,form_3_training_number,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered FROM dcf_bdsp_reg")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame (df_nested_list)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form3_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form3_exported_file',index=False )
                    new_column_names = 'Types of BDSP,Contact Person, Training Number,Sex , Office/Main Address, Email Address,Brief Description of Company Institution and/or Consultant Background, Phone number,Field of Expertise,Preferred Region to work in for RAPID,Preferred Province to work in for RAPID, Name,Education,Expertise,Prior RAPID Engagements?,Date Registered, RAPID Implementing Unit,Type/Nature of Engagements,Suppliers Evaluation (Refer to ISO/Procurement ratings),other engagement outside RAPID,Willing to conduct on-line lecture/training/seminar?, Willing to develop modular video training materials?,Willing to join other providers as organize pool of service providers?,Willing to be a mentor/coach on demand basis?,Willing to be part of long-term engagement for extension service facilitation?,Philgeps Registered'
                    new_column_names_list = new_column_names.split(',')
                    df.columns = new_column_names_list
                for column in df:
                    column_width = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['dcf_form3_exported_file'].set_column(col_idx, col_idx, column_width);
                workbook  = writer.book
                worksheet = writer.sheets['dcf_form3_exported_file']
                header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                writer.save()
                return send_file(c.RECORDS+'/objects/_temp_/dcf_form3_exported_file.xlsx')
            return form3export()
        
        elif export_type == 'form4export':
            def form4export():
                if request.method == "POST":
                    query= db.select("SELECT cbb_implementing_unit,cbb_training_number,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_total_number_of_participants,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_of_beneficiaries_per_type,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI FROM dcf_capacity_building")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame (df_nested_list)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form4_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form4_exported_file',index=False )
                    new_column_names = 'Implementing Unit,Training Number, Activity Title,Types of Training , Topic Of Training, DIP-approved alignment,Name of DIP, ACTIVITY DURATION (Day/Month/Year) Start,ACTIVITY DURATION (Day/Month/Year) End,Total Number of Participants, Commodity,Venue,Name of Resource Person/Facilitator/BDSP(First Name/Middle Name/Last Name),RAPID Actual Budget Actual (CY 2022 Onwards e.g. 34000.00),Name of Partner/Organization,Counterpart Amount(monetize & estimates),Total number of beneficiaries per type,Total Number Per Gender male,Total Number Per Gender female,Total Number Gender, Total Number Per Sector-PWD,Total Number Per Sector-Youth,Total Number Per Sector-IP,Total Number Per Sector-SC,Total Number Sector, Results of activity (Average) Pre-test,Results of activity (Average) Post-Test, Client Feedback Survey Rating, Client Feedback Survey Comments/ Areas of Improvement'
                    new_column_names_list = new_column_names.split(',')
                    df.columns = new_column_names_list
                for column in df:
                    column_width = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['dcf_form4_exported_file'].set_column(col_idx, col_idx, column_width);
                workbook  = writer.book
                worksheet = writer.sheets['dcf_form4_exported_file']
                header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                writer.save()
                return send_file(c.RECORDS+'/objects/_temp_/dcf_form4_exported_file.xlsx')
            return form4export()
        
        elif export_type == 'form5export':
            def form5export():
                if request.method == "POST":
                    query= db.select("SELECT mgit_implementing_unit_rcu,mgit_implementing_unit_pcu,mgit_name_of_dip,mgit_msme_recipient,mgit_total_member_recipient,mgit_commodity,mgit_total_number_fo_gender_male,mgit_total_number_fo_gender_female,mgit_total_number_fo_sectoral_pwd,mgit_total_number_fo_sectoral_youth,mgit_total_number_fo_sectoral_IP,mgit_total_number_fo_sectoral_SC,mgit_type_of_investment,mgit_total_mgas_based_approved_DIP,mgit_total_mgas_signed,mgit_total_mgas_not_yet_signed,mgit_total_matching_grant_based_on_approved_business,mgit_pmga_first_availment,mgit_mgar_period_date,mgit_remaining_matching_grant_balance,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_budget_approved_in_the_DIP,mgit_actual_cost_of_procurement,mgit_summary_of_actual_tools_procured,mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_date_of_distribution,mgit_remarks_on_the_deliverd_tools FROM dcf_matching_grant")
                    df_nested_list = pd.json_normalize(query)
                    df = pd.DataFrame (df_nested_list)
                    writer = pd.ExcelWriter(c.RECORDS+'/objects/_temp_/dcf_form5_exported_file.xlsx') 
                    df.to_excel(writer, sheet_name='dcf_form5_exported_file',index=False )
                    new_column_names = 'Implementing Unit RCU,Implementing Unit PCU, Name Of DIP,Name of FO/MSME RECIPIENT(type name of FO / MSME), total # of FO Member Recipients, Commodity,Total number of FO members by Gender Male, Total number of FO members by Gender Female,Total number of FO members by sectoral group PWD,Total number of FO members by sectoral group Youth, Total number of FO members by sectoral group IP,Total number of FO members by sectoral group SC,Type of Investment,TOTAL OF MGAs based on approved DIP,Total of MGAs Signed,Total of MGAs not yet signed,TOTAL MATCHING GRANT BASED ON APPROVED BUSINESS PLAN (IN PHP),PREVIOUS MATCHING GRANT AVAILMENT (IN PHP) - FIRST AVAILMENT,MATCHING GRANT AVAILMENT AS OF THIS REPORTING PERIOD(in PHP) and date,REMAINING MATCHING GRANT BALANCE (in PHP), INCLUSIVE TIMELINE OF IMPLEMENTATION (based on MGA) Start,INCLUSIVE TIMELINE OF IMPLEMENTATION (based on MGA) End,Time elapse,Total budget as approved in the DIP,actual cost of procurement,summary of actual tools procured,Inclusive timeline of implementation (based on MGA) Start,Inclusive timeline of implementation (based on MGA) End,time elapse,DATE of distribution/training,Remarks delivered tools'
                    new_column_names_list = new_column_names.split(',')
                    df.columns = new_column_names_list
                for column in df:
                    column_width = max(df[column].astype(str).map(len).max(), len(column))
                    col_idx = df.columns.get_loc(column)
                    writer.sheets['dcf_form5_exported_file'].set_column(col_idx, col_idx, column_width);
                workbook  = writer.book
                worksheet = writer.sheets['dcf_form5_exported_file']
                header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00ace6','border': 1})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                writer.save()
                return send_file(c.RECORDS+'/objects/_temp_/dcf_form5_exported_file.xlsx')
            return form5export()

    else:
        return redirect('dcfspreadsheet.html')


# if __name__ == "__main__":
#     app.run(debug=True)
