from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form5(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        mgit_implementing_unit = request.form['mgit_implementing_unit']
        mgit_name_of_dip = request.form['mgit_name_of_dip']
        mgit_msme_recipient = request.form.get('mgit_msme_recipient')
        mgit_total_member_recipient = request.form['mgit_total_member_recipient']
        mgit_commodity = request.form.get('mgit_commodity', None)
        mgit_commodity_others = request.form.get('mgit_commodity_others', None)

        if mgit_commodity == 'PFN' and mgit_commodity_others:
            chosen_commodity = mgit_commodity_others
        else:
            chosen_commodity = mgit_commodity
        mgit_total_number_fo_gender_male = request.form['mgit_total_number_fo_gender_male']
        mgit_total_number_fo_gender_female = request.form.get('mgit_total_number_fo_gender_female')
        mgit_total_number_fo_sectoral_pwd = request.form.get('mgit_total_number_fo_sectoral_pwd')
        mgit_total_number_fo_sectoral_youth = request.form['mgit_total_number_fo_sectoral_youth']
        mgit_total_number_fo_sectoral_IP = request.form['mgit_total_number_fo_sectoral_IP']
        mgit_total_number_fo_sectoral_SC = request.form.get('mgit_total_number_fo_sectoral_SC')
        mgit_type_of_investment = request.form.get('mgit_type_of_investment')
        mgit_total_mgas_based_approved_DIP = request.form.get('mgit_total_mgas_based_approved_DIP')
        mgit_total_mgas_signed = request.form.get('mgit_total_mgas_signed')
        mgit_total_mgas_not_yet_signed = request.form.get('mgit_total_mgas_not_yet_signed')
        mgit_total_matching_grant_based_on_approved_business = request.form.get('mgit_total_matching_grant_based_on_approved_business')
        mgit_pmga_first_availment = request.form.get('mgit_pmga_first_availment')
        mgit_mgar_period_date = request.form.get('mgit_mgar_period_date')
        mgit_remaining_matching_grant_balance = request.form.get('mgit_remaining_matching_grant_balance')
        mgit_inclusive_timeline_implementation_start = request.form.get('mgit_inclusive_timeline_implementation_start')
        mgit_inclusive_timeline_implementation_end = request.form.get('mgit_inclusive_timeline_implementation_end')
        mgit_time_elapse = request.form.get('mgit_time_elapse')
        mgit_total_budget_approved_in_the_DIP = request.form.get('mgit_total_budget_approved_in_the_DIP')
        mgit_actual_cost_of_procurement = request.form.get('mgit_actual_cost_of_procurement')
        mgit_summary_of_actual_tools_procured = request.form.get('mgit_summary_of_actual_tools_procured')
        mgit_inclusive_timeline_implementation_start1 = request.form.get('mgit_inclusive_timeline_implementation_start1')
        mgit_inclusive_timeline_implementation_end1 = request.form.get('mgit_inclusive_timeline_implementation_end1')
        mgit_time_elapse1 = request.form.get('mgit_time_elapse1')
        mgit_date_of_distribution = request.form.get('mgit_date_of_distribution')
        mgit_remarks_on_the_deliverd_tools = request.form.get('mgit_remarks_on_the_deliverd_tools')
        
        form5_data = db.do("INSERT INTO dcf_matching_grant (upload_by, mgit_implementing_unit,mgit_name_of_dip,mgit_msme_recipient,mgit_total_member_recipient,mgit_commodity,mgit_total_number_fo_gender_male,mgit_total_number_fo_gender_female,mgit_total_number_fo_sectoral_pwd,mgit_total_number_fo_sectoral_youth,mgit_total_number_fo_sectoral_IP,mgit_total_number_fo_sectoral_SC,mgit_type_of_investment,mgit_total_mgas_based_approved_DIP,mgit_total_mgas_signed,mgit_total_mgas_not_yet_signed,mgit_total_matching_grant_based_on_approved_business,mgit_pmga_first_availment,mgit_mgar_period_date,mgit_remaining_matching_grant_balance,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_budget_approved_in_the_DIP,mgit_actual_cost_of_procurement,mgit_summary_of_actual_tools_procured,mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_date_of_distribution,mgit_remarks_on_the_deliverd_tools) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by, mgit_implementing_unit,mgit_name_of_dip,mgit_msme_recipient,mgit_total_member_recipient,chosen_commodity,mgit_total_number_fo_gender_male,mgit_total_number_fo_gender_female,mgit_total_number_fo_sectoral_pwd,mgit_total_number_fo_sectoral_youth,mgit_total_number_fo_sectoral_IP,mgit_total_number_fo_sectoral_SC,mgit_type_of_investment,mgit_total_mgas_based_approved_DIP,mgit_total_mgas_signed,mgit_total_mgas_not_yet_signed,mgit_total_matching_grant_based_on_approved_business,mgit_pmga_first_availment,mgit_mgar_period_date,mgit_remaining_matching_grant_balance,mgit_inclusive_timeline_implementation_start,mgit_inclusive_timeline_implementation_end,mgit_time_elapse,mgit_total_budget_approved_in_the_DIP,mgit_actual_cost_of_procurement,mgit_summary_of_actual_tools_procured,mgit_inclusive_timeline_implementation_start1,mgit_inclusive_timeline_implementation_end1,mgit_time_elapse1,mgit_date_of_distribution,mgit_remarks_on_the_deliverd_tools))
        #return str(form5_data)
     
        if(form5_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form5_data)
        else:
            flash(f"Record Saved!", "success")

    return(form5_data)