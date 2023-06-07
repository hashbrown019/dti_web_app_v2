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

def importcsvform1(request):
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
                f.save(os.path.join(c.RECORDS+"/objects/spreadsheets_dcf/queued/",UPLOAD_NAME ))
                excel_upload_open(os.path.join(c.RECORDS+"/objects/spreadsheets_dcf/queued/",UPLOAD_NAME ))
        except IndexError:
            flash(f"Invalid file template!", "error")
            
            
    return redirect("/dcfspreadsheet")

def excel_upload_open(path):  
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    header = data[4]
    
    for row in data[5:]:
        upload_by = session["USER_DATA"][0]['id']
        form_1_rcus = row[0]                                                                      
        form_1_number_of_dips = row[1]                                                                                                     
        form_1_anchor_firm = row[3]                                                               
        form_1_size_of_anchor = row[5]                                                               
        form_1_commodity = row[6]                                                   
        form_1_scope_provinces = row[7]                                                         
        form_1_for_development = row[8]                                                   
        form_1_cn_approved = row[9]                                                                                                       
        form_1_finalized_approved = row[10]                                                  
        form_1_date_of_parallel_review = row[11]                                                     
        form_1_date_of_submission = row[12]                                                                                                  
        form_1_date_of_rtwg = row[13]                                                                                   
        form_1_date_of_npco_cursory = row[14]                                                                                      
        form_1_date_of_uploading_to_ifad = row[15]                                                                                           
        form_1_date_of_ifad_no_inssuance = row[16]                                                                                                                                             
        form_1_totalmsme = row[17]                                                                                           
        form_1_total_farmerbene = row[18]                                                                                     
        form_1_totalfo = row[19]                                                                                             
        form_1_namefo = row[20]                                                                                                                                            
        form_1_totalhectarage_cov = row[21]                                                                                                                                        
        form_1_hect_rehab = row[22]                                                   
        form_1_total_cost_rehab = row[23]                                            
        form_1_hect_exp = row[24]                                          
        form_1_cost_exp = row[25]                                                                                            
        form_1_totalcost_prodinvest = row[26]                                                                                           
        form_1_total_matching_grant = row[27]                                         
        form_1_capbuilding = row[28]                                                                                     
        form_1_supply_chain_manager = row[29]                                             
        form_1_totalproject_cost = row[30]                                                                           
        form_1_fmi = row[31]                                               
        form_1_fmi_kms = row[32]                                                                                       
        filename = UPLOAD_NAME

        querycsv = ("INSERT INTO dcf_prep_review_aprv_status ( upload_by,form_1_rcus,form_1_number_of_dips,form_1_anchor_firm,form_1_size_of_anchor,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalcost_prodinvest,form_1_total_matching_grant,form_1_capbuilding,form_1_supply_chain_manager,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms,filename) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".
        format(upload_by, form_1_rcus,form_1_number_of_dips,form_1_anchor_firm,form_1_size_of_anchor,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_cn_approved,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_namefo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_totalcost_prodinvest,form_1_total_matching_grant,form_1_capbuilding,form_1_supply_chain_manager,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms,filename))
        insert=db.do(querycsv)
        
    if(insert["response"]=="error"):
        flash(f"An error occured !", "error")
        print(str(insert))
    else:
        flash(f"The file was imported successfully!", "success")  
    return "done"
