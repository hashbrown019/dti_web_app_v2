from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform9(request):

    if request.method == 'POST':
        id = request.form['id']
        form_9_implementing_unit = request.form['form_9_implementing_unit']
        form_9_title_trade_promotion = request.form['form_9_title_trade_promotion']
        form_9_type_of_training = request.form['form_9_type_of_training']
        form_9_others = request.form['form_9_others']
        form_9_start_date = request.form['form_9_start_date']
        form_9_end_date = request.form['form_9_end_date']
        form_9_venue = request.form['form_9_venue']
        form_9_rapid_actual_budget = request.form['form_9_rapid_actual_budget']
        form_9_name_of_resource_person = request.form['form_9_name_of_resource_person']
        form_9_name_of_participant_org = request.form['form_9_name_of_participant_org']
        form_9_counterpart_amount = request.form['form_9_counterpart_amount']
        form_9_name_of_participant = request.form['form_9_name_of_participant']
        form_9_organization = request.form['form_9_organization']
        form_9_designation = request.form['form_9_designation']
        form_9_male = request.form['form_9_male']
        form_9_female = request.form['form_9_female']
        form_9_pwd = request.form['form_9_pwd']
        form_9_youth = request.form['form_9_youth']
        form_9_ip = request.form['form_9_ip']
        form_9_sc = request.form['form_9_sc']
        form_9_pre_test1 = request.form['form_9_pre_test1']
        form_9_post_test1 = request.form['form_9_post_test1']
        form_9_activity_output = request.form['form_9_activity_output']
        form_9_pre_test2 = request.form['form_9_pre_test2']
        form_9_post_test2 = request.form['form_9_post_test2']
        form_9_rating = request.form['form_9_rating']
        form_9_comments = request.form['form_9_comments']

        sql = """UPDATE dcf_enablers_activity
               SET form_9_implementing_unit='{}',form_9_title_trade_promotion='{}',form_9_type_of_training='{}',form_9_others='{}',form_9_start_date='{}',form_9_end_date='{}',form_9_venue='{}',form_9_rapid_actual_budget='{}',form_9_name_of_resource_person='{}',form_9_name_of_participant_org='{}',form_9_counterpart_amount='{}',form_9_name_of_participant='{}',form_9_organization='{}',form_9_designation='{}',form_9_male='{}',form_9_female='{}',form_9_pwd='{}',form_9_youth='{}',form_9_ip='{}',form_9_sc='{}',form_9_pre_test1='{}',form_9_post_test1='{}',form_9_activity_output='{}',form_9_pre_test2='{}',form_9_post_test2='{}',form_9_rating='{}',form_9_comments='{}'
               WHERE id={}
            """.format(form_9_implementing_unit,form_9_title_trade_promotion,form_9_type_of_training,form_9_others,form_9_start_date,form_9_end_date,form_9_venue,form_9_rapid_actual_budget,form_9_name_of_resource_person,form_9_name_of_participant_org,form_9_counterpart_amount,form_9_name_of_participant,form_9_organization,form_9_designation,form_9_male,form_9_female,form_9_pwd,form_9_youth,form_9_ip,form_9_sc,form_9_pre_test1,form_9_post_test1,form_9_activity_output,form_9_pre_test2,form_9_post_test2,form_9_rating,form_9_comments, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)