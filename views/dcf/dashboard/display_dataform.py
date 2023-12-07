from flask import flash,render_template,redirect,session
import Configurations as c
from modules.Connections import mysql
from flask_session import Session
import Configurations as c
from werkzeug.utils import secure_filename


db = mysql(*c.DB_CRED)
db.err_page = 0
def is_on_session(): return ('USER_DATA' in session)

def display():
    if(is_on_session()):
        pass
    else:
        return redirect("/login?force_url=1")
        
    USER_INFO = session["USER_DATA"]
    form1_datatable=db.select("SELECT * FROM dcf_prep_review_aprv_status")
    form2_datatable=db.select("SELECT * FROM dcf_implementing_unit")
    form3_datatable=db.select("SELECT * FROM dcf_bdsp_reg")
    form4_datatable=db.select("SELECT * FROM dcf_capacity_building")
    form5_datatable=db.select("SELECT * FROM dcf_matching_grant")
    form6_datatable=db.select("SELECT * FROM dcf_product_development")
    form7_datatable=db.select("SELECT * FROM dcf_trade_promotion")
    form8_datatable=db.select("SELECT * FROM form8")
    form9_datatable=db.select("SELECT * FROM dcf_enablers_activity")
    form10_datatable=db.select("SELECT * FROM dcf_negosyo_center")
    form11_datatable=db.select("SELECT * FROM dcf_access_financing")


    return{
        'form1_datatable':  form1_datatable,
        'form2_datatable':  form2_datatable,
        'form3_datatable':  form3_datatable,
        'form4_datatable':  form4_datatable,
        'form5_datatable':  form5_datatable,
        'form6_datatable':  form6_datatable,
        'form7_datatable':  form7_datatable,
        'form8_datatable':  form8_datatable,
        'form9_datatable':  form9_datatable,
        'form10_datatable':  form10_datatable,
        'form11_datatable':  form11_datatable
    }


def displayform():
    if(is_on_session()):
        pass
    else:
        return redirect("/login?force_url=1")
        
    USER_INFO = session["USER_DATA"]
    form1_datatable=db.select("SELECT * FROM dcf_prep_review_aprv_status {} ORDER BY `id` DESC;".format(position_data_filter()))
    form2_datatable=db.select("SELECT * FROM dcf_implementing_unit {} ORDER BY `id` DESC;".format(position_data_filter()))
    form3_datatable=db.select("SELECT * FROM dcf_bdsp_reg {} ORDER BY `id` DESC;".format(position_data_filter()))
    form4_datatable=db.select("SELECT * FROM dcf_capacity_building {} ORDER BY `id` DESC;".format(position_data_filter()))
    form5_datatable=db.select("SELECT * FROM dcf_matching_grant {} ORDER BY `id` DESC;".format(position_data_filter()))
    form6_datatable=db.select("SELECT * FROM dcf_product_development {} ORDER BY `id` DESC;".format(position_data_filter()))
    form7_datatable=db.select("SELECT * FROM dcf_trade_promotion {} ORDER BY `id` DESC;".format(position_data_filter()))
    form8_datatable=db.select("SELECT * FROM form8 {} ORDER BY `id` DESC;".format(position_data_filter()))
    form9_datatable=db.select("SELECT * FROM dcf_enablers_activity {} ORDER BY `id` DESC;".format(position_data_filter()))
    form10_datatable=db.select("SELECT * FROM dcf_negosyo_center {} ORDER BY `id` DESC;".format(position_data_filter()))
    form11_datatable=db.select("SELECT * FROM dcf_access_financing {} ORDER BY `id` DESC;".format(position_data_filter()))

    dcf_form1male=db.select("SELECT SUM(form_1_totalmale) AS total_male FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1maleyouth=db.select("SELECT SUM(form_1_maleyouth) AS total_maleyouth FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1maleip=db.select("SELECT SUM(form_1_maleip) AS total_maleip FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1malepwd=db.select("SELECT SUM(form_1_malepwd) AS total_malepwd FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))


    dcf_form1sextotal=db.select("SELECT SUM(form_1_total_farmerbene) AS total_sex FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form2sextotal=db.select("SELECT  SUM(form_2_male + form_2_female)AS total_sex2 FROM dcf_implementing_unit {}; ".format(position_data_filter()))


    dcf_form1female=db.select("SELECT SUM(form_1_totalfemale) AS total_female FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1femaleyouth=db.select("SELECT SUM(form_1_femaleyouth) AS total_femaleyouth FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1femaleip=db.select("SELECT SUM(form_1_femaleip) AS total_femaleip FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1femalepwd=db.select("SELECT SUM(form_1_femalepwd) AS total_femalepwd FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))


    dcf_form2FOmale=db.select("SELECT SUM(form_2_male) AS total_male2 FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    dcf_form2FOfemale=db.select("SELECT SUM(form_2_female) AS total_female2 FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    selectdcf_form3male=db.select("SELECT form_3_sex AS total_male3 FROM dcf_bdsp_reg {} AND form_3_sex = 'male';".format(position_data_filter()))
    selectdcf_form3female=db.select("SELECT form_3_sex AS total_female3 FROM dcf_bdsp_reg {} AND form_3_sex = 'female';".format(position_data_filter()))
    dcf_form3male=len(selectdcf_form3male)
    dcf_form3female=len(selectdcf_form3female)
    dcf_form4male=db.select("SELECT SUM(cbb_total_number_per_gender_male) AS total_male4 FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4female=db.select("SELECT SUM(cbb_total_number_per_gender_female) AS total_female4 FROM dcf_capacity_building {};".format(position_data_filter()))

    dcf_form1msme=db.select("SELECT SUM(total_large_enterprise) as total_large_entep FROM dcf_prep_review_aprv_status {};".format(position_data_filter()))
    dcf_form1msme2=db.select("SELECT SUM(total_medium_enterprise) as total_medium_entep FROM dcf_prep_review_aprv_status {};".format(position_data_filter()))
    dcf_form1msme3=db.select("SELECT SUM(total_small_enterprise ) as total_small_entep FROM dcf_prep_review_aprv_status {};".format(position_data_filter()))
    dcf_form1msme4=db.select("SELECT SUM(total_micro_enterprise ) as total_micro_entep FROM dcf_prep_review_aprv_status {};".format(position_data_filter()))
    

    selectapprovedform1=db.select("SELECT form_1_date_of_npco_cursory,form_1_date_of_ifad_no_inssuance,form_1_rcus FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance != '' AND form_1_date_of_npco_cursory != '' OR ' ' ".format(position_data_filter()))
    # print(selectapprovedform1)
    rcu8approvedform1 = len(selectapprovedform1)



    # selectpipelineform1=db.select("SELECT form_1_for_development,form_1_finalized_approved,form_1_rcus FROM dcf_prep_review_aprv_status {} AND form_1_finalized_approved != '' AND form_1_for_development != '' OR ' ' ".format(position_data_filter()))
    # print(selectpipelineform1)
    # pipelineform1 = len(selectpipelineform1)

    # selectongoingform1=db.select("SELECT form_1_for_development,form_1_rcus FROM dcf_prep_review_aprv_status {} AND form_1_for_development != '' OR ' ' ".format(position_data_filter()))
    # print(selectongoingform1)
    # ongoingform1 = len(selectongoingform1)

    # dips_list=db.select('''
    #     SELECT 
    #         form_1_for_development, #PIPELINE # ONGOING
    #         form_1_finalized_approved, #PIPELINE
    #         form_1_date_of_ifad_no_inssuance, #APPROVE
    #         form_1_date_of_npco_cursory,  #APPROVE
    #         form_1_rcus,
    #         form_1_commodity
    #     FROMdcf_prep_review_aprv_status {} ;'''.format(position_data_filter()))
##################################FORM2#########################################
    dips_list2 = form2_datatable
    over_all_commodity_count2 = {}
    for index in range(len(dips_list2)):
        DIP2 = dips_list2[index]
        _comm_rule2 = ["cacao","coconut","coffee","pfn"]
        _com2 = DIP2['form_2_commodity']
        if(_com2.lower() not in _comm_rule2):
            _com2 = "Others"
        if(_com2 not in over_all_commodity_count2):
            over_all_commodity_count2[_com2 ] = 0
        over_all_commodity_count2[_com2 ] += 1

######################FORM1########################################
    dips_list = form1_datatable
    
    dip_status_group_per_region={}
    over_all = {"over_all_total":0,"approve":0,"ongoing":0,"pipeline":0,"not_started":0,}
    commodities_per_status_per_region= {}
    over_all_commodity_count = {}

    for index in range(len(dips_list)):
        DIP = dips_list[index]
        if(DIP['form_1_rcus'] not in dip_status_group_per_region):
            dip_status_group_per_region[DIP['form_1_rcus']] = {'max':0, "total":0,"approve":0, "pipeline":0, "ongoing":0, "not_started":0 }
            commodities_per_status_per_region[DIP['form_1_rcus']] = {"total":{},"approve":{}, "pipeline":{}, "ongoing":{}, "not_started":{} }
            # dip_status_group_per_region[DIP['form_1_rcus']] = {"total":0,"approve":[], "pipeline":[], "ongoing":[], "not_started":[] }
        else:pass

        # COMMODITY COUNT PER REGION total
        if(DIP['form_1_commodity'] not in commodities_per_status_per_region[DIP['form_1_rcus']]["total"]):
            commodities_per_status_per_region[DIP['form_1_rcus']]["total"][DIP['form_1_commodity']] = 0

        # FOR OVER ALL COMMODITY COUNT
        _comm_rule = ["cacao","coconut","coffee","pfn"]
        _com = DIP['form_1_commodity']
        if(_com.lower() not in _comm_rule):
            _com = "Others"
        if(_com not in over_all_commodity_count):
            over_all_commodity_count[_com ] = 0
        over_all_commodity_count[_com ] += 1

        if(DIP["form_1_date_of_npco_cursory"] != "" and DIP["form_1_date_of_ifad_no_inssuance"] != ""):
            dip_status_group_per_region[DIP['form_1_rcus']]["total"] += 1
            over_all["over_all_total"] +=1
            dip_status_group_per_region[DIP['form_1_rcus']]["approve"]+= 1
            over_all["approve"] += 1
            
            if(DIP['form_1_commodity'] not in commodities_per_status_per_region[DIP['form_1_rcus']]["approve"]):
                commodities_per_status_per_region[DIP['form_1_rcus']]["approve"][DIP['form_1_commodity']] = 0
            commodities_per_status_per_region[DIP['form_1_rcus']]["approve"][DIP['form_1_commodity']] += 1
            commodities_per_status_per_region[DIP['form_1_rcus']]["total"][DIP['form_1_commodity']] += 1
            # dip_status_group_per_region[DIP['form_1_rcus']]["approve"].append(DIP)

        elif(DIP["form_1_for_development"] != "" and DIP["form_1_finalized_approved"] != ""):
            dip_status_group_per_region[DIP['form_1_rcus']]["total"] += 1
            over_all["over_all_total"] +=1
            dip_status_group_per_region[DIP['form_1_rcus']]["pipeline"]+= 1
            over_all["pipeline"] += 1
            
            if(DIP['form_1_commodity'] not in commodities_per_status_per_region[DIP['form_1_rcus']]["pipeline"]):
                commodities_per_status_per_region[DIP['form_1_rcus']]["pipeline"][DIP['form_1_commodity']] = 0
            commodities_per_status_per_region[DIP['form_1_rcus']]["pipeline"][DIP['form_1_commodity']] += 1
            commodities_per_status_per_region[DIP['form_1_rcus']]["total"][DIP['form_1_commodity']] += 1
            # dip_status_group_per_region[DIP['form_1_rcus']]["pipeline"].append(DIP)

        elif(DIP["form_1_for_development"] != ""):
            dip_status_group_per_region[DIP['form_1_rcus']]["total"]+= 1
            over_all["over_all_total"] +=1
            dip_status_group_per_region[DIP['form_1_rcus']]["ongoing"]+= 1
            over_all["ongoing"] += 1
            
            if(DIP['form_1_commodity'] not in commodities_per_status_per_region[DIP['form_1_rcus']]["ongoing"]):
                commodities_per_status_per_region[DIP['form_1_rcus']]["ongoing"][DIP['form_1_commodity']] = 0
            commodities_per_status_per_region[DIP['form_1_rcus']]["ongoing"][DIP['form_1_commodity']] += 1
            commodities_per_status_per_region[DIP['form_1_rcus']]["total"][DIP['form_1_commodity']] += 1
            # dip_status_group_per_region[DIP['form_1_rcus']]["ongoing"].append(DIP)

        else:
            dip_status_group_per_region[DIP['form_1_rcus']]["total"] += 1
            over_all["over_all_total"] +=1
            dip_status_group_per_region[DIP['form_1_rcus']]["not_started"]+= 1
            over_all["not_started"] += 1
            
            if(DIP['form_1_commodity'] not in commodities_per_status_per_region[DIP['form_1_rcus']]["not_started"]):
                commodities_per_status_per_region[DIP['form_1_rcus']]["not_started"][DIP['form_1_commodity']] = 0
            commodities_per_status_per_region[DIP['form_1_rcus']]["not_started"][DIP['form_1_commodity']] += 1
            commodities_per_status_per_region[DIP['form_1_rcus']]["total"][DIP['form_1_commodity']] += 1
            # dip_status_group_per_region[DIP['form_1_rcus']]["not_started"].append(DIP)
        # dip_status_group_per_region[DIP['form_1_rcus']].append(DIP)
    alltotal = 0

    for xxx in dip_status_group_per_region:
        alltotal += dip_status_group_per_region[xxx]['total']
    # print(alltotal)
    # dip_status_group_per_region["_over_all"] = over_all
    total_untagged = 0
    dip_sex_group_per_region = {}
    for index in range(len(dips_list)):
        DIP = dips_list[index]
        if(DIP['form_1_rcus'] not in dip_sex_group_per_region):
            dip_sex_group_per_region[DIP['form_1_rcus']] = {'total_bene':0, 'male':{ "youth":0,"ip":0,"pwd":0,"total":0}, "female":{ "youth":0,"ip":0,"pwd":0,"total":0},"all_total":{'untagged':0, "total_youth":0,"total_ip":0,"total_pwd":0,"total_sex":0}}
            # dip_sex_group_per_region[DIP['form_1_rcus']] = {"total":0,"approve":[], "pipeline":[], "ongoing":[], "not_started":[] }
        else:pass
        dip_sex_group_per_region[DIP['form_1_rcus']]['male']['youth'] += DIP['form_1_maleyouth']
        dip_sex_group_per_region[DIP['form_1_rcus']]['male']['ip'] += DIP['form_1_maleip']
        dip_sex_group_per_region[DIP['form_1_rcus']]['male']['pwd'] += DIP['form_1_malepwd']
        dip_sex_group_per_region[DIP['form_1_rcus']]['male']['total'] += DIP['form_1_totalmale']

        dip_sex_group_per_region[DIP['form_1_rcus']]['female']['youth'] += DIP['form_1_femaleyouth']
        dip_sex_group_per_region[DIP['form_1_rcus']]['female']['ip'] += DIP['form_1_femaleip']
        dip_sex_group_per_region[DIP['form_1_rcus']]['female']['pwd'] += DIP['form_1_femalepwd']
        dip_sex_group_per_region[DIP['form_1_rcus']]['female']['total'] += DIP['form_1_totalfemale']

        dip_sex_group_per_region[DIP['form_1_rcus']]['all_total']['total_youth'] += DIP['form_1_maleyouth'] + DIP['form_1_femaleyouth']
        dip_sex_group_per_region[DIP['form_1_rcus']]['all_total']['total_ip'] += DIP['form_1_maleip'] + DIP['form_1_femaleip']
        dip_sex_group_per_region[DIP['form_1_rcus']]['all_total']['total_pwd'] += DIP['form_1_malepwd'] + DIP['form_1_femalepwd']
        dip_sex_group_per_region[DIP['form_1_rcus']]['all_total']['total_sex'] += DIP['form_1_totalmale'] + DIP['form_1_totalfemale']

        try:
            dip_sex_group_per_region[DIP['form_1_rcus']]['total_bene'] += float(DIP['form_1_total_farmerbene'])
            dip_sex_group_per_region[DIP['form_1_rcus']]['all_total']['untagged'] += float(DIP['form_1_total_farmerbene'])- (DIP['form_1_totalmale'] + DIP['form_1_totalfemale'])
            total_untagged += float(DIP['form_1_total_farmerbene'])- (DIP['form_1_totalmale'] + DIP['form_1_totalfemale'])
        except Exception as e:
            # raise e
            pass
        # if(DIP['form_1_total_farmerbene'].isnumeric()):
        #     dip_sex_group_per_region[DIP['form_1_rcus']]['total_bene'] += int(DIP['form_1_total_farmerbene'])

    return{
        'form1_datatable':  form1_datatable,
        'form2_datatable':  form2_datatable,
        'form3_datatable':  form3_datatable,
        'form4_datatable':  form4_datatable,
        'form5_datatable':  form5_datatable,
        'form6_datatable':  form6_datatable,
        'form7_datatable':  form7_datatable,
        'form8_datatable':  form8_datatable,
        'form9_datatable':  form9_datatable,
        'form10_datatable':  form10_datatable,
        'form11_datatable':  form11_datatable,
        'dcf_form1male':  dcf_form1male,
        'dcf_form1maleyouth': dcf_form1maleyouth,
        'dcf_form1maleip':dcf_form1maleip,
        'dcf_form1malepwd':dcf_form1malepwd,
        'dcf_form1sextotal':dcf_form1sextotal,
        'dcf_form2sextotal':dcf_form2sextotal,
        'dcf_form1female':  dcf_form1female,
        'dcf_form1femaleyouth': dcf_form1femaleyouth,
        'dcf_form1femaleip':dcf_form1femaleip,
        'dcf_form1femalepwd':dcf_form1femalepwd,
        'dcf_form2FOmale':  dcf_form2FOmale,
        'dcf_form2FOfemale':  dcf_form2FOfemale,
        'dcf_form3male':  dcf_form3male,
        'dcf_form3female':  dcf_form3female,
        'dcf_form4male':  dcf_form4male,
        'dcf_form4female':  dcf_form4female,
        'dips_list':  dip_status_group_per_region,
        'over_all_dips_list':  over_all,
        'total_dip_nat':alltotal,
        'dip_sex_group_per_region' : dip_sex_group_per_region,
        "commodities_per_status_per_region" : commodities_per_status_per_region,
        'dcf_form1msme':dcf_form1msme,
        'dcf_form1msme2':dcf_form1msme2,
        'dcf_form1msme3':dcf_form1msme3,
        'dcf_form1msme4':dcf_form1msme4,
        'total_untagged' : total_untagged,
        'over_all_commodity_count':over_all_commodity_count,
        'over_all_commodity_count2':over_all_commodity_count2,


    }

def position_data_filter():
    _filter = "WHERE 1 "
    JOB = session["USER_DATA"][0]["job"].lower()

    if(JOB in "admin" or JOB in "super admin"):
        session["USER_DATA"][0]["office"] = "NPCO"
        _filter = "WHERE 1 "
    else:
        session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
        _filter = "WHERE `upload_by` in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])

    return _filter
