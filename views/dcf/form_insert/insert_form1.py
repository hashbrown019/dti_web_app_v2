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
        form_1_name_dip = request.form['form_1_name_dip']
        form_1_anchor_firm = request.form['form_1_anchor_firm']
        form_1_size_of_anchor =', '.join(request.form.getlist('form_1_size_of_anchor[]') )
        form_1_msmes =', '.join(request.form.getlist('form_1_msmes[]') )
        form_1_commodity = request.form.get('form_1_commodity', None)
        form_1_commodity_others = request.form.get('form_1_commodity_others', None)
        if form_1_commodity == 'PFN' and form_1_commodity_others:
            chosen_commodity = form_1_commodity_others
        else:
            chosen_commodity = form_1_commodity
        form_1_scope_provinces =', '.join(request.form.getlist('form_1_scope_provinces[]') )
        form_1_for_development = request.form['form_1_for_development']
        # form_1_cn_approved = request.form.get('form_1_cn_approved')
        form_1_finalized_approved = request.form.get('form_1_finalized_approved')
        form_1_date_of_parallel_review = request.form['form_1_date_of_parallel_review']
        form_1_date_of_submission = request.form['form_1_date_of_submission']
        form_1_date_of_rtwg = request.form.get('form_1_date_of_rtwg')
        form_1_date_of_npco_cursory = request.form.get('form_1_date_of_npco_cursory')
        # form_1_date_of_uploading_to_ifad = request.form.get('form_1_date_of_uploading_to_ifad')
        # form_1_date_of_approval_to_ifad = request.form.get('form_1_date_of_approval_to_ifad')
        form_1_date_of_ifad_no_inssuance = request.form.get('form_1_date_of_ifad_no_inssuance')
        total_large_enterprise = request.form.get('total_large_enterprise')
        total_medium_enterprise = request.form.get('total_medium_enterprise')
        total_small_enterprise = request.form.get('total_small_enterprise')
        total_micro_enterprise = request.form.get('total_micro_enterprise')
        form_1_totalmale= request.form.get('form_1_totalmale')
        form_1_maleyouth = request.form.get('form_1_maleyouth')
        form_1_maleip= request.form.get('form_1_maleip')
        form_1_malepwd= request.form.get('form_1_malepwd')
        form_1_totalfemale= request.form.get('form_1_totalfemale')
        form_1_femaleyouth = request.form.get('form_1_femaleyouth')
        form_1_femaleip= request.form.get('form_1_femaleip')
        form_1_femalepwd= request.form.get('form_1_femalepwd')
        form_1_totalyouth = request.form.get('form_1_totalyouth')
        form_1_totalip = request.form.get('form_1_totalip')
        form_1_totalpwd = request.form.get('form_1_totalpwd')
        form_1_totalcooperatives = request.form.get('form_1_totalcooperatives')
        form_1_totalassociations = request.form.get('form_1_totalassociations')
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
        form_1_Facilities_warehouse = request.form.get('form_1_Facilities_warehouse')
        form_1_totalcost_prodinvest = request.form.get('form_1_totalcost_prodinvest')
        form_1_total_rehab = request.form.get('form_1_total_rehab')
        form_1_total_exp = request.form.get('form_1_total_exp')
        form_1_totalcost_prodinvest2 = request.form.get('form_1_totalcost_prodinvest2')
        form_1_partners_counterpart = request.form.get('form_1_partners_counterpart')
        form1_total_mg_cost = request.form.get('form1_total_mg_cost')
        form_1_total_matching_grant = request.form.get('form_1_total_matching_grant')
        form_1_organizational = request.form.get('form_1_organizational')
        form_1_technical_trainings = request.form.get('form_1_technical_trainings')
        form_1_post_production = request.form.get('form_1_post_production')
        form_1_others = request.form.get('form_1_others')
        form_1_total_capbuild = request.form.get('form_1_total_capbuild')
        form_1_supply_chain_manager = request.form.get('form_1_supply_chain_manager')
        form_1_y = request.form.get('form_1_y')
        form_1_ac = request.form.get('form_1_ac')
        form_1_ad = request.form.get('form_1_ad')
        form1_total_fmi = request.form.get('form1_total_fmi')
        form_1_ae = request.form.get('form_1_ae')
        form_1_totalproject_cost = request.form.get('form_1_totalproject_cost')
        form_1_fmi = request.form.get('form_1_fmi')
        form_1_fmi_kms = request.form.get('form_1_fmi_kms')
        fmi_part_counter = request.form.get('fmi_part_counter')
        partner_counterpart_MG = request.form.get('partner_counterpart_MG')
        partner_counterpart_CB = request.form.get('partner_counterpart_CB')
        partner_counterpart_SCM = request.form.get('partner_counterpart_SCM')
        partner_counterpart_FMI = request.form.get('partner_counterpart_FMI')
        partner_counterpart_total = request.form.get('partner_counterpart_total')
        total_dip_cost_MG = request.form.get('total_dip_cost_MG')
        total_dip_cost_CB = request.form.get('total_dip_cost_CB')
        total_dip_cost_SCM = request.form.get('total_dip_cost_SCM')
        total_dip_cost_FMI = request.form.get('total_dip_cost_FMI')
        total_dip_cost_total = request.form.get('total_dip_cost_total')

        # mov = file_from_request(None)
        # file_NAME_mov = mov._save_file_from_request(request,"mov",c.RECORDS+"objects/dcf_mov/",True,True)['file_arr_str']
        form1_data = db.do("INSERT INTO dcf_prep_review_aprv_status  (upload_by,form_1_rcus,form_1_name_dip,form_1_anchor_firm,form_1_size_of_anchor,form_1_msmes,form_1_commodity,form_1_scope_provinces,form_1_for_development,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_ifad_no_inssuance,total_large_enterprise,total_medium_enterprise,total_small_enterprise,total_micro_enterprise,form_1_totalmale,form_1_maleyouth,form_1_maleip,form_1_malepwd,form_1_totalfemale,form_1_femaleyouth,form_1_femaleip,form_1_femalepwd,form_1_totalyouth,form_1_totalip,form_1_totalpwd,form_1_totalcooperatives,form_1_totalassociations,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_Facilities_warehouse,form_1_totalcost_prodinvest,form_1_total_rehab,form_1_total_exp,form_1_totalcost_prodinvest2,form_1_partners_counterpart,form1_total_mg_cost,form_1_total_matching_grant,form_1_organizational,form_1_technical_trainings,form_1_post_production,form_1_others,form_1_total_capbuild,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad,form1_total_fmi,form_1_ae,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms,fmi_part_counter,partner_counterpart_MG,partner_counterpart_CB,partner_counterpart_SCM,partner_counterpart_FMI,partner_counterpart_total,total_dip_cost_MG,total_dip_cost_CB,total_dip_cost_SCM,total_dip_cost_FMI,total_dip_cost_total) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')". 
        format(upload_by,form_1_rcus,form_1_name_dip,form_1_anchor_firm,form_1_size_of_anchor,form_1_msmes,chosen_commodity,form_1_scope_provinces,form_1_for_development,form_1_finalized_approved,form_1_date_of_parallel_review,form_1_date_of_submission,form_1_date_of_rtwg,form_1_date_of_npco_cursory,form_1_date_of_ifad_no_inssuance,total_large_enterprise,total_medium_enterprise,total_small_enterprise,total_micro_enterprise,form_1_totalmale,form_1_maleyouth,form_1_maleip,form_1_malepwd,form_1_totalfemale,form_1_femaleyouth,form_1_femaleip,form_1_femalepwd,form_1_totalyouth,form_1_totalip,form_1_totalpwd,form_1_totalcooperatives,form_1_totalassociations,form_1_totalmsme,form_1_total_farmerbene,form_1_totalfo,form_1_totalhectarage_cov,form_1_hect_rehab,form_1_total_cost_rehab,form_1_hect_exp,form_1_cost_exp,form_1_euqipment,form_1_Facilities_warehouse,form_1_totalcost_prodinvest,form_1_total_rehab,form_1_total_exp,form_1_totalcost_prodinvest2,form_1_partners_counterpart,form1_total_mg_cost,form_1_total_matching_grant,form_1_organizational,form_1_technical_trainings,form_1_post_production,form_1_others,form_1_total_capbuild,form_1_supply_chain_manager,form_1_y,form_1_ac,form_1_ad,form1_total_fmi,form_1_ae,form_1_totalproject_cost,form_1_fmi,form_1_fmi_kms,fmi_part_counter,partner_counterpart_MG,partner_counterpart_CB,partner_counterpart_SCM,partner_counterpart_FMI,partner_counterpart_total,total_dip_cost_MG,total_dip_cost_CB,total_dip_cost_SCM,total_dip_cost_FMI,total_dip_cost_total))
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