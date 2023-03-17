from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form10(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        form_10_nc_location=request.form['form_10_nc_location']
        form_10_name_of_nc=request.form['form_10_name_of_nc']
        form_10_title_of_rapid_activity=request.form['form_10_title_of_rapid_activity']
        form_10_type_of_assistance=request.form['form_10_type_of_assistance']
        form_10_date=request.form['form_10_date']
        form_10_type_of_beneficiary=request.form['form_10_type_of_beneficiary']
        form_10_sex_male=request.form['form_10_sex_male']
        form_10_sex_female=request.form['form_10_sex_female']
        form_10_commodity=request.form['form_10_commodity']


        form10_data = db.do("INSERT INTO dcf_negosyo_center (upload_by, form_10_nc_location,form_10_name_of_nc,form_10_title_of_rapid_activity,form_10_type_of_assistance,form_10_date,form_10_type_of_beneficiary,form_10_sex_male,form_10_sex_female,form_10_commodity) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by, form_10_nc_location,form_10_name_of_nc,form_10_title_of_rapid_activity,form_10_type_of_assistance,form_10_date,form_10_type_of_beneficiary,form_10_sex_male,form_10_sex_female,form_10_commodity))
        #return str(form5_data)
     
        if(form10_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form10_data)
        else:
            flash(f"Record Saved!", "success")

    return(form10_data)