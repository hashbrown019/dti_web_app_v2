from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform2(request):

    if request.method == 'POST':
        id = request.form['id']
        form_2_rcus	 = request.form['form_2_rcus']
        form_2_pcu = request.form['form_2_pcu']
        form_2_commodity = request.form.get('form_2_commodity', None)
        form_2_commodity_others = request.form.get('form_2_commodity_others', None)

        if form_2_commodity == 'PFN' and form_2_commodity_others:
            chosen_commodity = form_2_commodity_others
        else:
            chosen_commodity = form_2_commodity
        form_2_dip_alignment = request.form.get('form_2_dip_alignment', None)
        form_2_dip_alignment_yes = request.form.get('form_2_dip_alignment_yes', None)

        if form_2_dip_alignment == 'Yes' and form_2_dip_alignment_yes:
            chosen_dip = form_2_dip_alignment_yes
        else:
            chosen_dip = form_2_dip_alignment
        form_2_name_owner_manager = request.form['form_2_name_owner_manager']
        form_2_sex_owner_manager = request.form['form_2_sex_owner_manager']
        form_2_sector_owner_manager = request.form.get('form_2_sector_owner_manager')
        form_2_businessname = request.form.get('form_2_businessname')
        form_2_business_owner_manager = request.form.get('form_2_business_owner_manager')
        form_2_partner_fo_engaged = request.form['form_2_partner_fo_engaged']
        form_2_chairperson_manager = request.form['form_2_chairperson_manager']
        form_2_sex_chairperson_manager = request.form.get('form_2_sex_chairperson_manager')
        form_2_sector_chairperson_manager = request.form.get('form_2_sector_chairperson_manager')
        form_2_office_address_province = request.form.get('form_2_office_address_province')
        form_2_total_number_fo = request.form.get('form_2_total_number_fo')
        # form_2_cpa_incentives = request.form.get('form_2_cpa_incentives')
        form_2_male = request.form.get('form_2_male')
        form_2_female = request.form.get('form_2_female')
        form_2_pwde = request.form.get('form_2_pwde')
        form_2_youth = request.form.get('form_2_youth')
        form_2_ip = request.form.get('form_2_ip')
        form_2_sc = request.form.get('form_2_sc')
        # form_2_address_of_fo_members = request.form.get('form_2_address_of_fo_members')
        form_2_hectares_covered = request.form.get('form_2_hectares_covered')
        form_2_cpa_date_signing = request.form.get('form_2_cpa_date_signing')
        form_2_cpa_date_expiration = request.form.get('form_2_cpa_date_expiration')
        form_2_days_remaining = request.form.get('form_2_days_remaining')
        form_2_date_renewed = request.form.get('form_2_date_renewed')
        form_2_notable_cpa_incentives = request.form.get('form_2_notable_cpa_incentives')
        form_2_remarks_status = request.form.get('form_2_remarks_status', None)
        form_2_remarks_status_why = request.form.get('form_2_remarks_status_why', None)
        
        if (form_2_remarks_status == 'Cancelled' or form_2_remarks_status == 'Non-renewal') and form_2_remarks_status_why:
            remarks_status_why = f"{form_2_remarks_status}, {form_2_remarks_status_why}"
        else:
            remarks_status_why = form_2_remarks_status
        form_2_activity_agreements =', '.join(request.form.getlist('form_2_activity_agreements[]') )
        form_2_date_conducted =', '.join(request.form.getlist('form_2_date_conducted[]') )

        sql = """UPDATE dcf_implementing_unit
               SET form_2_rcus	='{}',form_2_pcu='{}',form_2_commodity='{}',form_2_dip_alignment='{}',form_2_name_owner_manager='{}',form_2_sex_owner_manager='{}',form_2_sector_owner_manager='{}',form_2_businessname='{}',form_2_business_owner_manager='{}',form_2_partner_fo_engaged='{}',form_2_chairperson_manager='{}',form_2_sex_chairperson_manager='{}',form_2_sector_chairperson_manager='{}',form_2_office_address_province='{}',form_2_total_number_fo='{}',form_2_male='{}',form_2_female='{}',form_2_pwde='{}',form_2_youth='{}',form_2_ip='{}',form_2_sc='{}',form_2_hectares_covered='{}',form_2_cpa_date_signing='{}',form_2_cpa_date_expiration='{}',form_2_days_remaining='{}',form_2_date_renewed='{}',form_2_notable_cpa_incentives='{}',form_2_remarks_status='{}',form_2_activity_agreements='{}',form_2_date_conducted='{}',date_modified=CURRENT_TIMESTAMP
               WHERE id={}
            """.format(form_2_rcus	,form_2_pcu,chosen_commodity,chosen_dip,form_2_name_owner_manager,form_2_sex_owner_manager,form_2_sector_owner_manager,form_2_businessname,form_2_business_owner_manager,form_2_partner_fo_engaged,form_2_chairperson_manager,form_2_sex_chairperson_manager,form_2_sector_chairperson_manager,form_2_office_address_province,form_2_total_number_fo,form_2_male,form_2_female,form_2_pwde,form_2_youth,form_2_ip,form_2_sc,form_2_hectares_covered,form_2_cpa_date_signing,form_2_cpa_date_expiration,form_2_days_remaining,form_2_date_renewed,form_2_notable_cpa_incentives,remarks_status_why,form_2_activity_agreements,form_2_date_conducted, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)