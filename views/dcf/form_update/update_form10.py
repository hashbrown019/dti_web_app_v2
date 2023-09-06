from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform10(request):

    if request.method == 'POST':
        id = request.form['id']
        form_10_nc_location=request.form['form_10_nc_location']
        form_10_name_of_nc=request.form['form_10_name_of_nc']
        form_10_title_of_rapid_activity=request.form['form_10_title_of_rapid_activity']
        form_10_type_of_assistance=request.form['form_10_type_of_assistance']
        form_10_date=request.form['form_10_date']
        form_10_type_of_beneficiary=request.form['form_10_type_of_beneficiary']
        form_10_sex_male=request.form['form_10_sex_male']
        form_10_sex_female=request.form['form_10_sex_female']
        form_10_commodity=request.form['form_10_commodity']

        sql = """UPDATE dcf_negosyo_center
               SET form_10_nc_location='{}',form_10_name_of_nc='{}',form_10_title_of_rapid_activity='{}',form_10_type_of_assistance='{}',form_10_date='{}',form_10_type_of_beneficiary='{}',form_10_sex_male='{}',form_10_sex_female='{}',form_10_commodity='{}',date_modified=CURRENT_TIMESTAMP
               WHERE id={}
            """.format(form_10_nc_location,form_10_name_of_nc,form_10_title_of_rapid_activity,form_10_type_of_assistance,form_10_date,form_10_type_of_beneficiary,form_10_sex_male,form_10_sex_female,form_10_commodity, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)