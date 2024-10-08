from flask import flash, session
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form6(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
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
        form_6_beneficiary_participant = ', '.join(request.form.getlist('form_6_beneficiary_participant[]'))
        form_6_commodity = ', '.join(request.form.getlist('form_6_commodity[]'))
        form_6_type_of_beneficiary = ', '.join(request.form.getlist('form_6_type_of_beneficiary[]'))
        # form_6_male = request.form['form_6_male']
        # form_6_female = request.form['form_6_female']
        form_6_sex = ', '.join(request.form.getlist('form_6_sex[]'))
        form_6_sector = ', '.join(request.form.getlist('form_6_sector[]'))
        # form_6_total_1 = request.form['form_6_total_1']
        # form_6_pwd = request.form['form_6_pwd']
        # form_6_youth = request.form['form_6_youth']
        # form_6_ip = request.form['form_6_ip']
        # form_6_sc = request.form['form_6_sc']
        # form_6_total_2 = request.form['form_6_total_2']
        form_6_product_developed =  ', '.join(request.form.getlist('form_6_product_developed[]'))
        form_6_date_launched_to_market = ', '.join(request.form.getlist('form_6_date_launched_to_market[]'))
        form_6_improved_product = ', '.join(request.form.getlist('form_6_improved_product[]'))
        print(request.form.getlist('form_6_type_of_product_improvement[]'))
        form_6_type_of_product_improvement = ', '.join(request.form.getlist('form_6_type_of_product_improvement[]'))
        form_6_name_of_product_developed = request.form['form_6_name_of_product_developed']
        form_6_ = request.form['form_6_']
        form_6_commodity1 = request.form.get('form_6_commodity1', None)
        form6_otherss1 = request.form.get('form6_otherss1', None)
        if form_6_commodity1 == 'other' and form6_otherss1:
            chosen_form6other1 = form6_otherss1
        else:
            chosen_form6other1 = form_6_commodity1
        form_6_commodity2 = request.form.get('form_6_commodity2', None)
        form6_otherss2 = request.form.get('form6_otherss2', None)
        if form_6_commodity2 == 'other' and form6_otherss2:
            chosen_form6other2 = form6_otherss2
        else:
            chosen_form6other2 = form_6_commodity2
        form_6_date_issuance = request.form['form_6_date_issuance']
        form_6_expiration_date = request.form['form_6_expiration_date']
        form_6_product_certified = request.form['form_6_product_certified']
        form_6_rating = request.form['form_6_rating']
        form_6_comment_ares_of_improvement = request.form['form_6_comment_ares_of_improvement']
        
        form6_data = db.do("INSERT INTO dcf_product_development (upload_by, form_6_implementing_unit,form_6_type_of_assisstance,form_6_type_of_activity,form_6_dip_alignment,form_6_activity_duration_start,form_6_activity_duration_end,form_6_venue,form_6_resource_person,form_6_rapid_actual_budget,form_6_name_of_partner_organization_1,form_6_name_of_partner_organization_2,form_6_beneficiary_participant,form_6_commodity,form_6_type_of_beneficiary,form_6_sex,form_6_sector,form_6_product_developed,form_6_date_launched_to_market,form_6_improved_product,form_6_type_of_product_improvement,form_6_name_of_product_developed,form_6_,form_6_commodity1,form_6_commodity2,form_6_date_issuance,form_6_expiration_date,form_6_product_certified,form_6_rating,form_6_comment_ares_of_improvement) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by, form_6_implementing_unit,form_6_type_of_assisstance,form_6_type_of_activity,form_6_dip_alignment,form_6_activity_duration_start,form_6_activity_duration_end,form_6_venue,form_6_resource_person,form_6_rapid_actual_budget,form_6_name_of_partner_organization_1,form_6_name_of_partner_organization_2,form_6_beneficiary_participant,form_6_commodity,form_6_type_of_beneficiary,form_6_sex,form_6_sector,form_6_product_developed,form_6_date_launched_to_market,form_6_improved_product,form_6_type_of_product_improvement,form_6_name_of_product_developed,form_6_,chosen_form6other1,chosen_form6other2,form_6_date_issuance,form_6_expiration_date,form_6_product_certified,form_6_rating,form_6_comment_ares_of_improvement))
        #return str(form5_data)
     
        if(form6_data["response"]=="error"):
            flash(f"An error occured !", "error")
            print(form6_data)
        else:
            flash(f"Record Saved!", "success")

    return(form6_data)