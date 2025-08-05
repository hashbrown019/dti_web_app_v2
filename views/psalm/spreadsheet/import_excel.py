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

def importcsv(request):
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
                f.save(os.path.join(c.RECORDS+"/objects/spreadsheets_c/queued/",UPLOAD_NAME ))
                excel_upload_open(os.path.join(c.RECORDS+"/objects/spreadsheets_c/queued/",UPLOAD_NAME ))
        except IndexError:
            flash(f"Invalid file template!", "error")
            
            
    return redirect("/spreadsheet")

def excel_upload_open(path):  
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    header = data[4]
    
    for row in data[6:]:
        upload_by = session["USER_DATA"][0]['id']
        dip_name = row[1]
        non_dip = row[2]
        name = row[3]
        position_firm = row[4]
        sex = row[5]
        age = row[6]
        contact_details = row[7]
        email_add = row[8]
        vc_stakeholders = row[9]
        industry_cluster = row[10]
        reg_businessname = row[11]
        business_addr = row[12]
        form_interprise = row[13]
        issued_by_business_reg = row[14]
        issued_by_product_reg = row[15]
        issued_by_cert_reg = row[16]
        issued_by_lic_op = row[17]
        issued_by_iso_cert = row[18]
        issued_by_gapgmp_cert = row[19]
        issued_by_organic = row[20]
        issued_by_halal = row[21]
        issued_by_other_cert = row[22]
        type_enterprise = row[23]
        store_capacity_organic = row[24]
        potential_organic = row[25]
        other_info_organic = row[26]
        store_capacity_synthetic = row[27]
        potential_synthetic = row[28]
        other_info_synthetic = row[29]
        store_capacity_pesticides = row[30]
        potential_pesticides = row[31]
        other_info_pesticides = row[32]
        store_capacity_herbicides = row[33]
        potential_herbicides = row[34]
        other_info_herbicides = row[35]
        store_capacity_vermicast_compost = row[36]
        potential_vermicast_compost = row[37]
        other_info_vermicast_compost = row[38]
        store_capacity_seedlings = row[39]
        potential_seedlings = row[40]
        other_info_seedlings = row[41]
        store_capacity_others_specific_products = row[42]
        potential_others_specific_products = row[43]
        other_info_others_specific_products = row[44]
        area_capacity_drying = row[45]
        potential_exp_drying = row[46]
        other_info_drying = row[47]
        area_capacity_storage = row[48]
        potential_exp_storage = row[49]
        other_info_storage = row[50]
        area_capacity_storage_hauling = row[51]
        potential_exp_storage_hauling = row[52]
        other_info_storage_hauling = row[53]
        current_capacity_semi_processing = row[54]
        potential_exp_semi_processing = row[55]
        other_info_semi_processing = row[56]
        current_capacity_final_product = row[57]
        potential_exp_final_product = row[58]
        other_info_final_product = row[59]
        volume_consolidation = row[60]
        potential_consolidation = row[61]
        other_info_consolidation = row[62]
        production_pack_label = row[63]
        potential_pack_label = row[64]
        other_info_pack_label = row[65]
        loan_portfo_micro_financing = row[66]
        potential_micro_financing = row[67]
        other_info_micro_financing = row[68]
        loan_portfo_insurance = row[69]
        potential_insurance = row[70]
        other_info_insurance = row[71]
        prodsales_product_service = row[72]
        prodsales_sales_vol = row[73]
        prodsales_unit_selling = row[74]
        prodsales_unit_measurement = row[75]
        prodsales_payment_terms = row[76]
        raw_materials = row[77]
        volume_supply = row[78]
        quality_requirement = row[79]
        unit_measurement_raw = row[80]
        distrib_point_local_cust = row[81]
        sales_vol_local_cust = row[82]
        payment_terms_local_cust = row[83]
        inhouse_num_workersmale = row[84]
        inhouse_num_workersfemale = row[85]
        inhouse_memb_ip_group = row[86]
        inhouse_ave_workdays = row[87]
        inhouse_ave_salary = row[88]
        sub_cont_num_workersmale = row[89]
        sub_cont_num_workersfemale = row[90]
        sub_cont_memb_ip_group = row[91]
        sub_cont_ave_workdays = row[92]
        sub_cont_ave_salary = row[93]
        piece_rate_num_workersmale = row[94]
        piece_rate_num_workersfemale = row[95]
        piece_rate_memb_ip_group = row[96]
        piece_rate_ave_workdays = row[97]
        piece_rate_ave_salary = row[98]
        form_interprise2 = row[99]
        pricing = row[100]
        quality_raw = row[101]
        quality_final_prod = row[102]
        other_specifyc3 = row[103]
        existing_comm = row[104]
        prov_supp_assis = row[105]
        business_prodc3 = row[106]
        member_livelihood = row[110]
        what_cluster_industry = row[111]
        filename = UPLOAD_NAME

        querycsv = ("INSERT INTO form_c ( upload_by, dip_name, non_dip, name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,store_capacity_synthetic,potential_organic,potential_synthetic,other_info_organic, other_info_synthetic, store_capacity_pesticides, store_capacity_herbicides, potential_pesticides, potential_herbicides, other_info_pesticides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,area_capacity_storage,potential_exp_storage,other_info_storage,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry,filename) VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}', '{}', '{}')".
        format(upload_by, dip_name, non_dip, name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,store_capacity_synthetic,potential_organic,potential_synthetic,other_info_organic, other_info_synthetic, store_capacity_pesticides, store_capacity_herbicides, potential_pesticides, potential_herbicides, other_info_pesticides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,area_capacity_storage,potential_exp_storage,other_info_storage,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry,filename))
        insert=db.do(querycsv)
        
    if(insert["response"]=="error"):
        flash(f"An error occured !", "error")
        print(str(insert))
    else:
        flash(f"The file was imported successfully!", "success")  
    return "done"
