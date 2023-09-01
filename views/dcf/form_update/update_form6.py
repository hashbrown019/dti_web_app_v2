from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform6(request):

    if request.method == 'POST':
        id = request.form['id']
        form_6_implementing_unit = request.form['form_6_implementing_unit']
        form_6_type_of_assisstance = request.form['form_6_type_of_assisstance']
        form_6_type_of_activity = request.form['form_6_type_of_activity']
        form_6_dip_alignment = request.form['form_6_dip_alignment']
        form_6_activity_duration_start = request.form['form_6_activity_duration_start']
        form_6_activity_duration_end = request.form['form_6_activity_duration_end']
        form_6_venue = request.form['form_6_venue']
        form_6_resource_person = request.form['form_6_resource_person']
        form_6_rapid_actual_budget = request.form['form_6_rapid_actual_budget']
        form_6_name_of_partner_organization_1 = ', '.join(request.form.getlist('form_6_name_of_partner_organization_1[]'))
        form_6_name_of_partner_organization_2 = ', '.join(request.form.getlist('form_6_name_of_partner_organization_2[]'))
        form_6_beneficiary_participant = request.form['form_6_beneficiary_participant']
        form_6_commodity = request.form.get('form_6_commodity', None)
        form_6_commodity_others = request.form.get('form_6_commodity_others', None)

        if form_6_commodity == 'PFN' and form_6_commodity_others:
            chosen_commodity = form_6_commodity_others
        else:
            chosen_commodity = form_6_commodity
        form_6_type_of_beneficiary = request.form['form_6_type_of_beneficiary']
        # form_6_male = request.form['form_6_male']
        # form_6_female = request.form['form_6_female']
        form_6_sex = request.form['form_6_sex']
        form_6_sector = request.form['form_6_sector']
        # form_6_total_1 = request.form['form_6_total_1']
        # form_6_pwd = request.form['form_6_pwd']
        # form_6_youth = request.form['form_6_youth']
        # form_6_ip = request.form['form_6_ip']
        # form_6_sc = request.form['form_6_sc']
        # form_6_total_2 = request.form['form_6_total_2']
        form_6_product_developed =  ', '.join(request.form.getlist('form_6_product_developed[]'))
        form_6_date_launched_to_market = ', '.join(request.form.getlist('form_6_date_launched_to_market[]'))
        form_6_improved_product = ', '.join(request.form.getlist('form_6_improved_product[]'))
        form_6_type_of_product_improvement = ', '.join(request.form.getlist('form_6_type_of_product_improvement[]'))
        form_6_name_of_product_developed = request.form['form_6_name_of_product_developed']
        form_6_ = request.form['form_6_']
        form_6_commodity1 = request.form['form_6_commodity1']
        form_6_commodity2 = request.form['form_6_commodity2']
        form_6_date_issuance = request.form['form_6_date_issuance']
        form_6_expiration_date = request.form['form_6_expiration_date']
        form_6_product_certified = request.form['form_6_product_certified']
        form_6_rating = request.form['form_6_rating']
        form_6_comment_ares_of_improvement = request.form['form_6_comment_ares_of_improvement']

        sql = """UPDATE dcf_product_development
               SET form_6_implementing_unit='{}',form_6_type_of_assisstance='{}',form_6_type_of_activity='{}',form_6_dip_alignment='{}',form_6_activity_duration_start='{}',form_6_activity_duration_end='{}',form_6_venue='{}',form_6_resource_person='{}',form_6_rapid_actual_budget='{}',form_6_name_of_partner_organization_1='{}',form_6_name_of_partner_organization_2='{}',form_6_beneficiary_participant='{}',form_6_commodity='{}',form_6_type_of_beneficiary='{}',form_6_sex='{}',form_6_sector='{}',form_6_product_developed='{}',form_6_date_launched_to_market='{}',form_6_improved_product='{}',form_6_type_of_product_improvement='{}',form_6_name_of_product_developed='{}',form_6_='{}',form_6_commodity1='{}',form_6_commodity2='{}',form_6_date_issuance='{}',form_6_expiration_date='{}',form_6_product_certified='{}',form_6_rating='{}',form_6_comment_ares_of_improvement='{}',date_created=CURRENT_TIMESTAMP
               WHERE id={}
            """.format(form_6_implementing_unit,form_6_type_of_assisstance,form_6_type_of_activity,form_6_dip_alignment,form_6_activity_duration_start,form_6_activity_duration_end,form_6_venue,form_6_resource_person,form_6_rapid_actual_budget,form_6_name_of_partner_organization_1,form_6_name_of_partner_organization_2,form_6_beneficiary_participant,chosen_commodity,form_6_type_of_beneficiary,form_6_sex,form_6_sector,form_6_product_developed,form_6_date_launched_to_market,form_6_improved_product,form_6_type_of_product_improvement,form_6_name_of_product_developed,form_6_,form_6_commodity1,form_6_commodity2,form_6_date_issuance,form_6_expiration_date,form_6_product_certified,form_6_rating,form_6_comment_ares_of_improvement, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)