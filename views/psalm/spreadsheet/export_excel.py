from flask import Flask, Blueprint, render_template, url_for, json, jsonify, send_file
import urllib.request
import pandas as pd
from modules.Connections import mysql
import Configurations as c


db = mysql(*c.DB_CRED)
db.err_page = 0

def exportcsv():
    query= db.select("SELECT name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,store_capacity_synthetic,potential_organic,potential_synthetic,other_info_organic, other_info_synthetic, store_capacity_pesticides, store_capacity_herbicides, potential_pesticides, potential_herbicides, other_info_pesticides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,area_capacity_storage,potential_exp_storage,other_info_storage,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry FROM form_c")

    #df = pd.read_json (r'http://10.0.254.2:5000/api/v2/sample/'+num_entries) # LOCAL HOST
    df = pd.DataFrame (query) # SERVER

    df.to_csv (r'exported_file.csv', index = 'profile__farmer_code')

    header_names = ['name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,store_capacity_synthetic,potential_organic,potential_synthetic,other_info_organic, other_info_synthetic, store_capacity_pesticides, store_capacity_herbicides, potential_pesticides, potential_herbicides, other_info_pesticides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,area_capacity_storage,potential_exp_storage,other_info_storage,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry']
   
    df=pd.read_csv('exported_file.csv',header=None, skiprows=1,names=header_names)
    writer = pd.ExcelWriter('exported_file.xlsx') 
    df.to_excel(writer, sheet_name='exported_file',index=False )

    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets['exported_file'].set_column(col_idx, col_idx, column_width)

    workbook  = writer.book
    worksheet = writer.sheets['exported_file']
    header_format = workbook.add_format({'bold': True,'text_wrap': True,'valign': 'top','fg_color': '#00cc66','border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
    writer.save()
    return send_file('exported_file.xlsx')
   

    

if __name__ == "__main__":
    app.run(debug=True)
