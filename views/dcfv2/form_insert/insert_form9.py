from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form9(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        form_9_implementing_unit = request.form['form_9_implementing_unit']
        form_9_title_trade_promotion = request.form['form_9_title_trade_promotion']
        form_9_type_of_training = request.form.get('form_9_type_of_training', None)
        form_9_othertypetraining = request.form.get('form_9_othertypetraining', None)
        if form_9_type_of_training == 'other' and form_9_othertypetraining:
            chosen_type = form_9_othertypetraining
        else:
            chosen_type = form_9_type_of_training
        form_9_start_date = request.form['form_9_start_date']
        form_9_end_date = request.form['form_9_end_date']
        form_9_venue = request.form['form_9_venue']
        form_9_rapid_actual_budget = request.form['form_9_rapid_actual_budget']
        form_9_name_of_resource_person = request.form['form_9_name_of_resource_person']
        form_9_name_of_participant_org = ', '.join(request.form.getlist('form_9_name_of_participant_org[]'))
        form_9_counterpart_amount = ', '.join(request.form.getlist('form_9_counterpart_amount[]'))
        form_9_name_of_participant = ', '.join(request.form.getlist('form_9_name_of_participant[]'))
        form_9_organization = ', '.join(request.form.getlist('form_9_organization[]'))
        form_9_designation =', '.join(request.form.getlist('form_9_designation[]'))
        form_9_sex = ', '.join(request.form.getlist('form_9_sex[]'))
        form_9_sector =', '.join(request.form.getlist('form_9_sector[]'))
        form_9_pre_test1 = request.form['form_9_pre_test1']
        form_9_post_test1 = request.form['form_9_post_test1']
        form_9_activity_output = request.form['form_9_activity_output']
        form_9_pre_test2 = request.form['form_9_pre_test2']
        form_9_post_test2 = request.form['form_9_post_test2']
        form_9_rating = request.form['form_9_rating']
        form_9_comments = request.form['form_9_comments']

        form9_data = db.do("INSERT INTO dcf_enablers_activity (upload_by, form_9_implementing_unit,form_9_title_trade_promotion,form_9_type_of_training,form_9_start_date,form_9_end_date,form_9_venue,form_9_rapid_actual_budget,form_9_name_of_resource_person,form_9_name_of_participant_org,form_9_counterpart_amount,form_9_name_of_participant,form_9_organization,form_9_designation,form_9_sex,form_9_sector,form_9_pre_test1,form_9_post_test1,form_9_activity_output,form_9_pre_test2,form_9_post_test2,form_9_rating,form_9_comments) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by, form_9_implementing_unit,form_9_title_trade_promotion,chosen_type,form_9_start_date,form_9_end_date,form_9_venue,form_9_rapid_actual_budget,form_9_name_of_resource_person,form_9_name_of_participant_org,form_9_counterpart_amount,form_9_name_of_participant,form_9_organization,form_9_designation,form_9_sex,form_9_sector,form_9_pre_test1,form_9_post_test1,form_9_activity_output,form_9_pre_test2,form_9_post_test2,form_9_rating,form_9_comments))
        #return str(form5_data)
     
        if(form9_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form9_data)
        else:
            flash(f"Record Saved!", "success")

    return(form9_data)