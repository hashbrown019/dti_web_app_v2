from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form4(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        cbb_implementing_unit = request.form['cbb_implementing_unit']
        cbb_training_number = request.form['cbb_training_number']
        cbb_activity_title = request.form['cbb_activity_title']
        cbb_types_of_training = request.form.get('cbb_types_of_training')
        cbb_topic_of_training = request.form['cbb_topic_of_training']
        cbb_dip_approved_alignment = request.form['cbb_dip_approved_alignment']
        cbb_name_of_dip = request.form['cbb_name_of_dip']
        cbb_date_start = request.form.get('cbb_date_start')
        cbb_date_end = request.form.get('cbb_date_end')
        cbb_total_number_of_participants = request.form['cbb_total_number_of_participants']
        cbb_commodity = request.form['cbb_commodity']
        cbb_venue = request.form.get('cbb_venue')
        cbb_name_of_resource_person = request.form.get('cbb_name_of_resource_person')
        cbb_rapid_actual_budget = request.form.get('cbb_rapid_actual_budget')
        cbb_dip_capbuild_activities_NPO = request.form.get('cbb_dip_capbuild_activities_NPO')
        cbb_dip_capbuild_activities_CA = request.form.get('cbb_dip_capbuild_activities_CA')
        cbb_total_number_of_beneficiaries_per_type = request.form.get('cbb_total_number_of_beneficiaries_per_type')
        cbb_total_number_per_gender_male = request.form.get('cbb_total_number_per_gender_male')
        cbb_total_number_per_gender_female = request.form.get('cbb_total_number_per_gender_female')
        cbb_total_number_per_gender_total = request.form.get('cbb_total_number_per_gender_total')
        cbb_total_number_per_sector_pwd = request.form.get('cbb_total_number_per_sector_pwd')
        cbb_total_number_per_sector_youth = request.form.get('cbb_total_number_per_sector_youth')
        cbb_total_number_per_sector_ip = request.form.get('cbb_total_number_per_sector_ip')
        cbb_total_number_per_sector_sc = request.form.get('cbb_total_number_per_sector_sc')
        cbb_total_number_per_sector_total = request.form.get('cbb_total_number_per_sector_total')
        cbb_results_of_activity_pre_test = request.form.get('cbb_results_of_activity_pre_test')
        cbb_results_of_activity_post_test = request.form.get('cbb_results_of_activity_post_test')
        cbb_client_feedback_survey_rating = request.form.get('cbb_client_feedback_survey_rating')
        cbb_client_feedback_survey_comments_AOI = request.form.get('cbb_client_feedback_survey_comments_AOI')
        
        form4_data = db.do("INSERT INTO dcf_capacity_building (upload_by, cbb_implementing_unit,cbb_training_number,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_total_number_of_participants,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_of_beneficiaries_per_type,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format( upload_by, cbb_implementing_unit,cbb_training_number,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_total_number_of_participants,cbb_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_of_beneficiaries_per_type,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI))
        #return str(form4_data)
     
        if(form4_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form4_data)
        else:
            flash(f"Record Saved!", "success")

    return(form4_data)