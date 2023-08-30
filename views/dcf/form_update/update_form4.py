from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform4(request):

    if request.method == 'POST':
        id = request.form['id']
        cbb_implementing_unit = request.form['cbb_implementing_unit']
        cbb_activity_title = request.form['cbb_activity_title']
        cbb_types_of_training = request.form.get('cbb_types_of_training')
        cbb_topic_of_training = request.form['cbb_topic_of_training']
        cbb_dip_approved_alignment = request.form['cbb_dip_approved_alignment']
        cbb_name_of_dip = request.form['cbb_name_of_dip']
        cbb_date_start = request.form.get('cbb_date_start')
        cbb_date_end = request.form.get('cbb_date_end')
        cbb_total_number_of_participants = request.form['cbb_total_number_of_participants']
        cbb_commodity = request.form.get('cbb_commodity', None)
        cbb_commodity_others = request.form.get('cbb_commodity_others', None)

        if cbb_commodity == 'PFN' and cbb_commodity_others:
            chosen_commodity = cbb_commodity_others
        else:
            chosen_commodity = cbb_commodity
        cbb_venue =', '.join(request.form.getlist('cbb_venue[]'))
        cbb_name_of_resource_person = ', '.join(request.form.getlist('cbb_name_of_resource_person[]'))
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

        sql = """UPDATE dcf_capacity_building
               SET cbb_implementing_unit='{}',cbb_activity_title='{}',cbb_types_of_training='{}',cbb_topic_of_training='{}',cbb_dip_approved_alignment='{}',cbb_name_of_dip='{}',cbb_date_start='{}',cbb_date_end='{}',cbb_total_number_of_participants='{}',cbb_commodity='{}',cbb_venue='{}',cbb_name_of_resource_person='{}',cbb_rapid_actual_budget='{}',cbb_dip_capbuild_activities_NPO='{}',cbb_dip_capbuild_activities_CA='{}',cbb_total_number_of_beneficiaries_per_type='{}',cbb_total_number_per_gender_male='{}',cbb_total_number_per_gender_female='{}',cbb_total_number_per_gender_total='{}',cbb_total_number_per_sector_pwd='{}',cbb_total_number_per_sector_youth='{}',cbb_total_number_per_sector_ip='{}',cbb_total_number_per_sector_sc='{}',cbb_total_number_per_sector_total='{}',cbb_results_of_activity_pre_test='{}',cbb_results_of_activity_post_test='{}',cbb_client_feedback_survey_rating='{}',cbb_client_feedback_survey_comments_AOI='{}'
               WHERE id={}
            """.format(cbb_implementing_unit,cbb_activity_title,cbb_types_of_training,cbb_topic_of_training,cbb_dip_approved_alignment,cbb_name_of_dip,cbb_date_start,cbb_date_end,cbb_total_number_of_participants,chosen_commodity,cbb_venue,cbb_name_of_resource_person,cbb_rapid_actual_budget,cbb_dip_capbuild_activities_NPO,cbb_dip_capbuild_activities_CA,cbb_total_number_of_beneficiaries_per_type,cbb_total_number_per_gender_male,cbb_total_number_per_gender_female,cbb_total_number_per_gender_total,cbb_total_number_per_sector_pwd,cbb_total_number_per_sector_youth,cbb_total_number_per_sector_ip,cbb_total_number_per_sector_sc,cbb_total_number_per_sector_total,cbb_results_of_activity_pre_test,cbb_results_of_activity_post_test,cbb_client_feedback_survey_rating,cbb_client_feedback_survey_comments_AOI, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)