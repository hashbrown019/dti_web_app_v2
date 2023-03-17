from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form11(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        form_11_dip_alignment=request.form['form_11_dip_alignment']
        form_11_dip_alignment_yes=request.form['form_11_dip_alignment_yes']
        form_11_activity_title=request.form['form_11_activity_title']
        form_11_name_of_beneficiary=request.form['form_11_name_of_beneficiary']
        form_11_industry_cluster=request.form['form_11_industry_cluster']
        form_11_industry_pfn=request.form['form_11_industry_pfn']
        form_11_msme_regional=request.form['form_11_msme_regional']
        form_11_msme_province=request.form['form_11_msme_province']
        form_11_male=request.form['form_11_male']
        form_11_female=request.form['form_11_female']
        form_11_pwd=request.form['form_11_pwd']
        form_11_youth=request.form['form_11_youth']
        form_11_ip=request.form['form_11_ip']
        form_11_sc=request.form['form_11_sc']
        form_11_date_submitted=request.form['form_11_date_submitted']
        form_11_date_approved=request.form['form_11_date_approved']
        form_11_name_of_fsp=request.form['form_11_name_of_fsp']
        form_11_location_address=request.form['form_11_location_address']
        form_11_amount_of_equity=request.form['form_11_amount_of_equity']
        form_11_date_released=request.form['form_11_date_released']


        form11_data = db.do("INSERT INTO dcf_access_financing (upload_by, form_11_dip_alignment,form_11_dip_alignment_yes,form_11_activity_title,form_11_name_of_beneficiary,form_11_industry_cluster,form_11_industry_pfn,form_11_msme_regional,form_11_msme_province,form_11_male,form_11_female,form_11_pwd,form_11_youth,form_11_ip,form_11_sc,form_11_date_submitted,form_11_date_approved,form_11_name_of_fsp,form_11_location_address,form_11_amount_of_equity,form_11_date_released) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by, form_11_dip_alignment,form_11_dip_alignment_yes,form_11_activity_title,form_11_name_of_beneficiary,form_11_industry_cluster,form_11_industry_pfn,form_11_msme_regional,form_11_msme_province,form_11_male,form_11_female,form_11_pwd,form_11_youth,form_11_ip,form_11_sc,form_11_date_submitted,form_11_date_approved,form_11_name_of_fsp,form_11_location_address,form_11_amount_of_equity,form_11_date_released))
        #return str(form5_data)
     
        if(form11_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form11_data)
        else:
            flash(f"Record Saved!", "success")

    return(form11_data)