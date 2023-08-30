from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form2(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        form_2_rcus	 = request.form['form_2_rcus']
        form_2_pcu = request.form['form_2_pcu']
        form_2_commodity = request.form.get('form_2_commodity', None)
        form_2_commodity_others = request.form.get('form_2_commodity_others', None)

        if form_2_commodity == 'Others' and form_2_commodity_others:
            chosen_commodity = form_2_commodity_others
        else:
            chosen_commodity = form_2_commodity
        form_2_dip_alignment = request.form.get('form_2_dip_alignment')
        form_2_yes = request.form['form_2_yes']
        form_2_name_owner_manager = request.form['form_2_name_owner_manager']
        form_2_sex_owner_manager = request.form['form_2_sex_owner_manager']
        form_2_sector_owner_manager = request.form.get('form_2_sector_owner_manager')
        form_2_business_owner_manager = request.form.get('form_2_business_owner_manager')
        form_2_partner_fo_engaged = request.form['form_2_partner_fo_engaged']
        form_2_chairperson_manager = request.form['form_2_chairperson_manager']
        form_2_sex_chairperson_manager = request.form.get('form_2_sex_chairperson_manager')
        form_2_sector_chairperson_manager = request.form.get('form_2_sector_chairperson_manager')
        form_2_office_address_province = request.form.get('form_2_office_address_province')
        form_2_total_number_fo = request.form.get('form_2_total_number_fo')
        form_2_male = request.form.get('form_2_male')
        form_2_female = request.form.get('form_2_female')
        form_2_pwde = request.form.get('form_2_pwde')
        form_2_youth = request.form.get('form_2_youth')
        form_2_ip = request.form.get('form_2_ip')
        form_2_sc = request.form.get('form_2_sc')
        form_2_address_of_fo_members = request.form.get('form_2_address_of_fo_members')
        form_2_hectares_covered = request.form.get('form_2_hectares_covered')
        form_2_cpa_date_signing = request.form.get('form_2_cpa_date_signing')
        form_2_cpa_date_expiration = request.form.get('form_2_cpa_date_expiration')
        form_2_days_remaining = request.form.get('form_2_days_remaining')
        form_2_date_renewed = request.form.get('form_2_date_renewed')
        form_2_notable_cpa_incentives = request.form.get('form_2_notable_cpa_incentives')
        form_2_remarks_status = request.form.get('form_2_remarks_status')
        form_2_activity_agreements = request.form.get('form_2_activity_agreements')
        form_2_date_conducted = request.form.get('form_2_date_conducted')

        
        form2_data = db.do("INSERT INTO dcf_implementing_unit  (upload_by,form_2_rcus	,form_2_pcu,form_2_commodity,form_2_dip_alignment,form_2_yes,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_remarks_status,form_2_activity_agreements,form_2_date_conducted) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by,form_2_rcus,form_2_pcu,chosen_commodity,form_2_dip_alignment,form_2_yes,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_address_of_fo_members,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,form_2_remarks_status,form_2_activity_agreements,form_2_date_conducted))
        #return str(form2_data)
     
        if(form2_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form2_data)
        else:
            flash(f"Record Saved!", "success")

    return(form2_data)