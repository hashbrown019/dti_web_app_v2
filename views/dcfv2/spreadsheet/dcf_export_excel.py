from flask import Flask, Blueprint, render_template, url_for, json, jsonify, send_file
import urllib.request
import pandas as pd
from modules.Connections import mysql
import Configurations as c


db = mysql(*c.DB_CRED)
db.err_page = 0

def exportcsv():
    query= db.select("SELECT form_1_rcus,form_1_number_of_dips, form_1_anchor_firm, form_1_size_of_anchor, form_1_commodity, form_1_scope_provinces,form_1_for_development, form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review, form_1_date_of_submission, form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad, form_1_date_of_ifad_no_inssuance,form_1_totalmsme, form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov, form_1_hect_rehab, form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_facilities, form_1_warehouse, form_1_total_matching_grant, form_1_organizational, form_1_technical_trainings, form_1_post_production, form_1_others,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad, form_1_ae,form_1_fmi,form_1_fmi_kms FROM dcf_prep_review_aprv_status")

    #df = pd.read_json (r'http://10.0.254.2:5000/api/v2/sample/'+num_entries) # LOCAL HOST
    df = pd.DataFrame (query)

    df.to_csv (r'exported_file.csv', index = 'profile__farmer_code')

    header_names = ['RCUs,Number Of DIPs, Anchor Firm, Size Of Anchor, Commodity, Scope/Provinces,For development (indicate date), Date: CN Approved,Date: Full BPs and DIPs Finalized/Approved by RCUs and endorsed to NPCO for Review,Date of the Parallel Review with NPCO/RGMS-IFAD-RTWG, Date of submission of the revised DIPs based on the comments from the parallel review, Date of RTWG Approval,Date: NPCO cursory review of RCUs compliance to parallel review comments; and DIP endorsement to NOTUS Uploading,Date: Uploading to IFAD NOTUS c/o NPCO, Date: IFAD NO Issuance,Total # of MSMEs, Total # of farmer beneficiaries,Total # of FOs,Input Name of FO,Total Hectarage Covered, Hectares for Rehab, Total Cost of Rehab,Hectares for Expansion,Total Cost of Expansion,Equipment,Facilities, Warehouse, Total Matching Grant (AA+AB), Organizational, Technical Trainings, Post-Production, Others,Supply Chain Manager,Y,AC,AD, AE,FMI,FMI Kms']
   
    df=pd.read_csv('exported_file.csv',header=None, skiprows=1,names=header_names)
    writer = pd.ExcelWriter('exported_file.xlsx') 
    df.to_excel(writer, sheet_name='exported_file',index=False )

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['exported_file'].set_column(col_idx, col_idx, column_width)

    workbook  = writer.book
    worksheet = writer.sheets['exported_file']
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#007399','border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.save()
    return send_file('exported_file.xlsx')
   

    

if __name__ == "__main__":
    app.run(debug=True)
