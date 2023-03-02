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
        files = request.files
        for file in files:
            f = files[file]
            global UPLOAD_NAME
            UPLOAD_NAME = str(uploader)+"#"+str(today)+"#"+secure_filename(f.filename)
            f.save(os.path.join(c.RECORDS+"/objects/spreadsheets_c/queued/",UPLOAD_NAME ))
            excel_upload_open(os.path.join(c.RECORDS+"/objects/spreadsheets_c/queued/",UPLOAD_NAME ))
            
            
    return redirect("/spreadsheet")

def excel_upload_open(path):  
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    header = data[4]
    
    for row in data[6:]:
        upload_by = session["USER_DATA"][0]['id']
        name = row[1]                                                                      
        position_firm = row[2]                                                                                                     
        sex = row[3]                                                               
        age = row[4]                                                               
        contact_details = row[5]                                                   
        email_add = row[6]                                                         
        vc_stakeholders = row[7]                                                   
        industry_cluster = row[8]                                                                                                       
        reg_businessname = row[9]                                                  
        business_addr = row[10]                                                     
        form_interprise = row[11]                                                                                                  
        issued_by_business_reg = row[12]                                                                                   
        issued_by_product_reg = row[13]                                                                                      
        issued_by_cert_reg = row[14]                                                                                           
        issued_by_lic_op = row[15]                                                                                                                                             
        issued_by_iso_cert = row[16]                                                                                           
        issued_by_gapgmp_cert = row[17]                                                                                     
        issued_by_organic = row[18]                                                                                             
        issued_by_halal = row[19]                                                                                                                                            
        issued_by_other_cert = row[20]                                                                                                                                        
        type_enterprise = row[21]                                                   
        store_capacity_organic = row[22]                                            
        store_capacity_synthetic = row[25]                                          
        potential_organic = row[23]                                                 
        potential_synthetic = row[26]                                               
        other_info_organic = row[24]                                                
        other_info_synthetic = row[27]                                              
        store_capacity_pesticides = row[28]                                         
        store_capacity_herbicides = row[31]                                         
        potential_pesticides = row[29]                                              
        potential_herbicides = row[32]                                              
        other_info_pesticides = row[30]                                             
        other_info_herbicides = row[33]                                             
        store_capacity_vermicast_compost = row[34]                                  
        potential_vermicast_compost = row[35]                                       
        other_info_vermicast_compost = row[36]                                      
        store_capacity_seedlings = row[37]                                          
        potential_seedlings = row[38]                                               
        other_info_seedlings = row[39]                                                                                       
        store_capacity_others_specific_products = row[40]                           
        potential_others_specific_products = row[41]                                
        other_info_others_specific_products = row[42]                               
        area_capacity_drying = row[43]                                              
        potential_exp_drying = row[44]                                              
        other_info_drying = row[45]
        area_capacity_storage = row[46]                                     
        potential_exp_storage = row[47]                                     
        other_info_storage = row[48]                                                  
        area_capacity_storage_hauling = row[49]                                     
        potential_exp_storage_hauling = row[50]                                     
        other_info_storage_hauling = row[51]                                        
        current_capacity_semi_processing = row[52]                                  
        potential_exp_semi_processing = row[53]                                     
        other_info_semi_processing = row[54]                                        
        current_capacity_final_product = row[55]                                    
        potential_exp_final_product = row[56]                                       
        other_info_final_product = row[51]                                          
        volume_consolidation = row[58]                                              
        potential_consolidation = row[59]                                           
        other_info_consolidation = row[60]                                          
        production_pack_label = row[61]                                             
        potential_pack_label = row[62]                                              
        other_info_pack_label = row[63]                                             
        loan_portfo_micro_financing = row[64]                                       
        potential_micro_financing = row[65]                                         
        other_info_micro_financing = row[66]                                        
        loan_portfo_insurance = row[67]                                             
        potential_insurance = row[68]                                               
        other_info_insurance = row[69]                                              
        prodsales_product_service = row[70]                                         
        prodsales_sales_vol = row[71]                                               
        prodsales_unit_selling = row[72]                                            
        prodsales_unit_measurement = row[73]                                        
        prodsales_payment_terms = row[74]                                                                                                                                         
        raw_materials = row[75]                                                     
        volume_supply = row[76]                                                     
        quality_requirement = row[77]                                               
        unit_measurement_raw = row[78]                                                                                           
        distrib_point_local_cust = row[80]                                          
        sales_vol_local_cust = row[81]                                              
        payment_terms_local_cust = row[82]                                                                                                                                                                                                                           
        inhouse_num_workersmale = row[83]
        inhouse_num_workersfemale = row[84]                                                  
        inhouse_memb_ip_group = row[85]                                                 
        inhouse_ave_workdays = row[86]                                                  
        inhouse_ave_salary = row[87]                                                    
        sub_cont_num_workersmale = row[88]
        sub_cont_num_workersfemale = row[89]                                                   
        sub_cont_memb_ip_group = row[90]                                                
        sub_cont_ave_workdays = row[91]                                                 
        sub_cont_ave_salary = row[92]                                                   
        piece_rate_num_workersmale = row[93]
        piece_rate_num_workersfemale = row[94]                                                 
        piece_rate_memb_ip_group = row[95]                                              
        piece_rate_ave_workdays = row[96]                                               
        piece_rate_ave_salary = row[97]                                                                                                      
        form_interprise2 = row[98]                                                                                                  
        pricing = row[99]                                                                                                                    
        quality_raw = row[100]                                                                                                             
        quality_final_prod = row[101]                                                                                               
        other_specifyc3 = row[102]                                                       
        existing_comm = row[103]                                                                                                           
        prov_supp_assis = row[104]                                                                                                     
        business_prodc3 = row[105]                                                                                                                                                                                                                                                               
        member_livelihood = row[108]                                                                           
        what_cluster_industry = row[109]
        filename = UPLOAD_NAME

        querycsv = ("INSERT INTO form_c ( upload_by, name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,store_capacity_synthetic,potential_organic,potential_synthetic,other_info_organic, other_info_synthetic, store_capacity_pesticides, store_capacity_herbicides, potential_pesticides, potential_herbicides, other_info_pesticides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,area_capacity_storage,potential_exp_storage,other_info_storage,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry,filename) VALUES ('{}', '{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}','{}', '{}', '{}')".
        format(upload_by, name,position_firm, sex, age, contact_details, email_add,vc_stakeholders, industry_cluster,reg_businessname,business_addr, form_interprise, issued_by_business_reg,issued_by_product_reg,issued_by_cert_reg, issued_by_lic_op,issued_by_iso_cert, issued_by_gapgmp_cert,issued_by_organic,issued_by_halal,issued_by_other_cert, type_enterprise, store_capacity_organic,store_capacity_synthetic,potential_organic,potential_synthetic,other_info_organic, other_info_synthetic, store_capacity_pesticides, store_capacity_herbicides, potential_pesticides, potential_herbicides, other_info_pesticides,other_info_herbicides,store_capacity_vermicast_compost,potential_vermicast_compost,other_info_vermicast_compost, store_capacity_seedlings,potential_seedlings,other_info_seedlings,store_capacity_others_specific_products,potential_others_specific_products,other_info_others_specific_products, area_capacity_drying, potential_exp_drying, other_info_drying,area_capacity_storage_hauling,potential_exp_storage_hauling,other_info_storage_hauling,area_capacity_storage,potential_exp_storage,other_info_storage,current_capacity_semi_processing,potential_exp_semi_processing,other_info_semi_processing,current_capacity_final_product, potential_exp_final_product,other_info_final_product,volume_consolidation, potential_consolidation, other_info_consolidation,production_pack_label,potential_pack_label, other_info_pack_label,loan_portfo_micro_financing,potential_micro_financing, other_info_micro_financing,loan_portfo_insurance,potential_insurance,other_info_insurance, prodsales_product_service, prodsales_sales_vol,prodsales_unit_selling,prodsales_unit_measurement,prodsales_payment_terms, raw_materials, volume_supply, quality_requirement,unit_measurement_raw, distrib_point_local_cust,sales_vol_local_cust, payment_terms_local_cust,inhouse_num_workersmale, inhouse_num_workersfemale, inhouse_memb_ip_group,inhouse_ave_workdays, inhouse_ave_salary, sub_cont_num_workersmale,sub_cont_num_workersfemale,sub_cont_memb_ip_group,sub_cont_ave_workdays,sub_cont_ave_salary,piece_rate_num_workersmale,piece_rate_num_workersfemale, piece_rate_memb_ip_group,piece_rate_ave_workdays, piece_rate_ave_salary,form_interprise2,pricing,quality_raw,quality_final_prod, other_specifyc3, existing_comm, prov_supp_assis, business_prodc3,member_livelihood,what_cluster_industry,filename))
        insert=db.do(querycsv)
        
    if(insert["response"]=="error"):
        flash(f"An error occured !", "error")
        print(str(insert))
    else:
        flash(f"The file was imported successfully!", "success")  
    return "done"
