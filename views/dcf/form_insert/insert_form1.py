from flask import flash, session, render_template
import Configurations as c
from modules.Connections import mysql
from modules.Req_Brorn_util import file_from_request

db = mysql(*c.DB_CRED)
db.err_page = 0

def insert_form1(request):
    if request.method == "POST":
        upload_by = session["USER_DATA"][0]['id']
        form_1_rcus = request.form['form_1_rcus']
        # form_1_number_of_dips = request.form['form_1_number_of_dips']
        form_1_anchor_firm = request.form['form_1_anchor_firm']
        form_1_size_of_anchor = request.form.get('form_1_size_of_anchor')
        form_1_commodity = request.form.get('form_1_commodity', None)
        form_1_commodity_others = request.form.get('form_1_commodity_others', None)

        if form_1_commodity == 'PFN' and form_1_commodity_others:
            chosen_commodity = form_1_commodity_others
        else:
            chosen_commodity = form_1_commodity
        form_1_scope_provinces = request.form['form_1_scope_provinces']
        form_1_for_development = request.form['form_1_for_development']
        # form_1_cn_approved = request.form.get('form_1_cn_approved')
        form_1_finalized_approved = request.form.get('form_1_finalized_approved')
        form_1_date_of_parallel_review = request.form['form_1_date_of_parallel_review']
        form_1_date_of_submission = request.form['form_1_date_of_submission']
        form_1_date_of_rtwg = request.form.get('form_1_date_of_rtwg')
        form_1_date_of_npco_cursory = request.form.get('form_1_date_of_npco_cursory')
        form_1_date_of_uploading_to_ifad = request.form.get('form_1_date_of_uploading_to_ifad')
        form_1_date_of_ifad_no_inssuance = request.form.get('form_1_date_of_ifad_no_inssuance')
        form_1_totalmsme = request.form.get('form_1_totalmsme')
        form_1_total_farmerbene = request.form.get('form_1_total_farmerbene')
        form_1_totalfo = request.form.get('form_1_totalfo')
        # form_1_namefo = request.form.get('form_1_namefo')
        form_1_totalhectarage_cov = request.form.get('form_1_totalhectarage_cov')
        form_1_hect_rehab = request.form.get('form_1_hect_rehab')
        form_1_total_cost_rehab = request.form.get('form_1_total_cost_rehab')
        form_1_hect_exp = request.form.get('form_1_hect_exp')
        form_1_cost_exp = request.form.get('form_1_cost_exp')
        form_1_euqipment = request.form.get('form_1_euqipment')
        form_1_facilities = request.form.get('form_1_facilities')
        form_1_warehouse = request.form.get('form_1_warehouse')
        form_1_aa = request.form.get('form_1_aa')
        form_1_ab = request.form.get('form_1_ab')
        form_1_total_matching_grant = request.form.get('form_1_total_matching_grant')
        form_1_organizational = request.form.get('form_1_organizational')
        form_1_technical_trainings = request.form.get('form_1_technical_trainings')
        form_1_post_production = request.form.get('form_1_post_production')
        form_1_others = request.form.get('form_1_others')
        form_1_supply_chain_manager = request.form.get('form_1_supply_chain_manager')
        form_1_y = request.form.get('form_1_y')
        form_1_ac = request.form.get('form_1_ac')
        form_1_ad = request.form.get('form_1_ad')
        form_1_ae = request.form.get('form_1_ae')
        form_1_totalproject_cost = request.form.get('form_1_totalproject_cost')
        form_1_fmi = request.form.get('form_1_fmi')
        form_1_fmi_kms = request.form.get('form_1_fmi_kms')
        # mov = file_from_request(None)
        # file_NAME_mov = mov._save_file_from_request(request,"mov",c.RECORDS+"objects/dcf_mov/",True,True)['file_arr_str']
        form1_data = db.do("INSERT INTO dcf_prep_review_aprv_status  (upload_by,form_1_rcus,form_1_anchor_firm,form_1_size_of_anchor,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_facilities,form_1_warehouse,form_1_aa,form_1_ab,form_1_total_matching_grant,form_1_organizational,form_1_technical_trainings,form_1_post_production,form_1_others,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad,form_1_ae,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by,form_1_rcus,form_1_anchor_firm,form_1_size_of_anchor,chosen_commodity,form_1_scope_provinces,form_1_for_development,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_uploading_to_ifad,form_1_date_of_ifad_no_inssuance,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_facilities,form_1_warehouse,form_1_aa,form_1_ab,form_1_total_matching_grant,form_1_organizational,form_1_technical_trainings,form_1_post_production,form_1_others,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad,form_1_ae,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms))
        #return str(form5_data)
        # skkkrt = {}
        # for key in request.form:
        #     skkkrt[key] = request.form[key]
        # print(skkkrt)
        if(form1_data["response"]=="error"):
            flash(f"An error occured !", "error")
            # print(form1_data)
            # return render_template('includes/forms/form1.html',user_data=session["USER_DATA"][0],data_recovery = skkkrt)
        else:
            flash(f"Record Saved!", "success")

    return(form1_data)