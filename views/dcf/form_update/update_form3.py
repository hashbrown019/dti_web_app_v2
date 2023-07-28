from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform3(request):

    if request.method == 'POST':
        id = request.form['id']
        form_3_types_of_bdsp = request.form['form_3_types_of_bdsp']
        form_3_contact_person = request.form['form_3_contact_person']
        form_3_training_number = request.form['form_3_training_number']
        form_3_sex = request.form.get('form_3_sex')
        form_3_office_addr = request.form['form_3_office_addr']
        form_3_email = request.form['form_3_email']
        form_3_breif_description = request.form['form_3_breif_description']
        phone = request.form['phone']
        form_3_choices = request.form.getlist('form_3_choices[]')
        form_3_preferred_region = request.form.get('form_3_preferred_region')
        form_3_preferred_province = request.form['form_3_preferred_province']
        form_3_name = ', '.join(request.form.getlist('form_3_name[]') )
        form_3_education = ', '.join(request.form.getlist('form_3_education[]') )
        form_3_expertise = ', '.join(request.form.getlist('form_3_expertise[]') )
        form_3_prior_rapid_engagements = request.form.get('form_3_prior_rapid_engagements')
        form_3_date_registered = request.form.get('form_3_date_registered')
        form_3_rapid_implementing_unit = request.form.get('form_3_rapid_implementing_unit')
        form_3_nature_engagements = request.form.get('form_3_nature_engagements')
        form_3_suppliers_evaluation = request.form.get('form_3_suppliers_evaluation')
        form_3_other_engagement_outside_rapid = request.form.get('form_3_other_engagement_outside_rapid')
        form_3_lecture_training_seminar = request.form.get('form_3_lecture_training_seminar')
        form_3_training_materials = request.form.get('form_3_training_materials')
        form_3_organize_pool = request.form.get('form_3_organize_pool')
        form_3_demand_basis = request.form.get('form_3_demand_basis')
        form_3_extension_service_facilitation = request.form.get('form_3_extension_service_facilitation')
        form_3_philgeps_registered = request.form.get('form_3_philgeps_registered')
        form_3_choices_string = ', '.join(form_3_choices)

        sql = """UPDATE dcf_bdsp_reg
               SET form_3_types_of_bdsp='{}',form_3_contact_person='{}',form_3_training_number='{}',form_3_sex='{}',form_3_office_addr='{}',form_3_email='{}',form_3_breif_description='{}',phone='{}',form_3_choices='{}',form_3_preferred_region='{}',form_3_preferred_province='{}',form_3_name='{}',form_3_education='{}',form_3_expertise='{}',form_3_prior_rapid_engagements='{}',form_3_date_registered='{}',form_3_rapid_implementing_unit='{}',form_3_nature_engagements='{}',form_3_suppliers_evaluation='{}',form_3_other_engagement_outside_rapid='{}',form_3_lecture_training_seminar='{}',form_3_training_materials='{}',form_3_organize_pool='{}',form_3_demand_basis='{}',form_3_extension_service_facilitation='{}',form_3_philgeps_registered='{}'
               WHERE id={}
            """.format(form_3_types_of_bdsp,form_3_contact_person,form_3_training_number,form_3_sex,form_3_office_addr,form_3_email,form_3_breif_description,phone,form_3_choices_string,form_3_preferred_region,form_3_preferred_province,form_3_name,form_3_education,form_3_expertise,form_3_prior_rapid_engagements,form_3_date_registered,form_3_rapid_implementing_unit,form_3_nature_engagements,form_3_suppliers_evaluation,form_3_other_engagement_outside_rapid,form_3_lecture_training_seminar,form_3_training_materials,form_3_organize_pool,form_3_demand_basis,form_3_extension_service_facilitation,form_3_philgeps_registered, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)