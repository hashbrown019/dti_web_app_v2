from flask import flash,render_template,redirect,session
import Configurations as c
from modules.Connections import mysql
from flask_session import Session
import Configurations as c
from werkzeug.utils import secure_filename


db = mysql(*c.DB_CRED)
db.err_page = 0
def is_on_session(): return ('USER_DATA' in session)

def data_filter(request):
    if request.method == 'POST':
        filter1 = request.form.get('filter1')
        filter2 = request.form.get('filter2')
        filter3 = request.form.get('filter3')
        filter4 = request.form.get('filter4')
    # filtering industry cluster - form enterprise
    datatable=db.select("SELECT * FROM form_c")
    coffee_singlesolesql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='coffee' AND form_interprise='Single/Sole'")
    cacao_singlesolesql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='cacao' AND form_interprise='Single/Sole'")
    coconut_singlesolesql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='coconut' AND form_interprise='Single/Sole'")
    pfn_singlesolesql=db.select("SELECT industry_cluster, form_interprise FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND form_interprise='Single/Sole'")

    coffee_partnershipsql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='coffee' AND form_interprise='partnership'")
    cacao_partnershipsql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='cacao' AND form_interprise='partnership'")
    coconut_partnershipsql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='coconut' AND form_interprise='partnership'")
    pfn_partnershipsql=db.select("SELECT industry_cluster, form_interprise FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND form_interprise='partnership'")

    coffee_corporationsql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='coffee' AND form_interprise='corporation'")
    cacao_corporationsql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='cacao' AND form_interprise='corporation'")
    coconut_corporationsql=db.select("SELECT `industry_cluster`,`form_interprise` from form_c where industry_cluster='coconut' AND form_interprise='corporation'")
    pfn_corporationsql=db.select("SELECT industry_cluster, form_interprise FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND form_interprise='corporation'")

    coffee_otherql=db.select("SELECT `industry_cluster`,`interprise_other` from form_c where industry_cluster='coffee' AND interprise_other != '' ")
    cacao_othersql=db.select("SELECT `industry_cluster`,`interprise_other` from form_c where industry_cluster='cacao' AND interprise_other != '' ")
    coconut_othersql=db.select("SELECT `industry_cluster`,`interprise_other` from form_c where industry_cluster='coconut' AND interprise_other != '' ")
    pfn_othersql=db.select("SELECT `pfn_specify`,`interprise_other` from form_c where pfn_specify !='' AND interprise_other != '' ")
    #------------------------------------

    # filtering gender - form enterprise
    male_singlesolesql=db.select("SELECT * from form_c where sex='male' AND form_interprise='Single/Sole'")
    female_singlesolesql=db.select("SELECT * from form_c where sex='female'  AND form_interprise='Single/Sole'")

    male_partnershipsql=db.select("SELECT `sex`,`form_interprise` from form_c where sex='male' AND form_interprise='Partnership'")
    female_partnershipsql=db.select("SELECT `sex`,`form_interprise` from form_c where sex='female'  AND form_interprise='Partnership'")

    male_corporationsql=db.select("SELECT `sex`,`form_interprise` from form_c where sex='male' AND form_interprise='corporation'")
    female_corporationsql=db.select("SELECT `sex`,`form_interprise` from form_c where sex='female'  AND form_interprise='corporation'")

    male_othersql=db.select("SELECT `sex`,`interprise_other` from form_c where sex='male' AND interprise_other != ''")
    female_othersql=db.select("SELECT `sex`,`interprise_other` from form_c where sex='female' AND interprise_other != ''")
    #------------------------------------

    # filtering form enterprise - business address
    adn_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%agusan del norte%' AND form_interprise='Single/Sole'")
    ads_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%agusan del sur%' AND form_interprise='Single/Sole'")
    sds_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%surigao del sur%' AND form_interprise='Single/Sole'")
    magui_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%maguindanao%' AND form_interprise='Single/Sole'")
    ns_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%northern samar%' AND form_interprise='Single/Sole'")
    leyte_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE 'leyte%' AND form_interprise='Single/Sole'")
    sleyte_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%southern leyte%' AND form_interprise='Single/Sole'")
    mo_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%misamis oriental%' AND form_interprise='Single/Sole'")
    bukd_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%bukidnon%' AND form_interprise='Single/Sole'")
    ldn_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%lanao del norte%' AND form_interprise='Single/Sole'")
    nc_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%north cotabato%' AND form_interprise='Single/Sole'")
    sk_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%sultan kudarat%' AND form_interprise='Single/Sole'")
    srng_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%sarangani%' AND form_interprise='Single/Sole'")
    zdn_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga del norte%' AND form_interprise='Single/Sole'")
    zs_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga sibugay%' AND form_interprise='Single/Sole'")
    zds_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga del sur%' AND form_interprise='Single/Sole'")
    ddo_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao de oro%' AND form_interprise='Single/Sole'")
    do_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao oriental%' AND form_interprise='Single/Sole'")
    ddn_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao del norte%' AND form_interprise='Single/Sole'")
    dds_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao del sur%' AND form_interprise='Single/Sole'")
    doc_singlesql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao occidental%' AND form_interprise='Single/Sole'")

    adn_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%agusan del norte%' AND form_interprise='partnership'")
    ads_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%agusan del sur%' AND form_interprise='partnership'")
    sds_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%surigao del sur%' AND form_interprise='partnership'")
    magui_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%maguindanao%' AND form_interprise='partnership'")
    ns_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%northern samar%' AND form_interprise='partnership'")
    leyte_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE 'leyte%' AND form_interprise='partnership'")
    sleyte_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%southern leyte%' AND form_interprise='partnership'")
    mo_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%misamis oriental%' AND form_interprise='partnership'")
    bukd_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%bukidnon%' AND form_interprise='partnership'")
    ldn_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%lanao del norte%' AND form_interprise='partnership'")
    nc_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%north cotabato%' AND form_interprise='partnership'")
    sk_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%sultan kudarat%' AND form_interprise='partnership'")
    srng_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%sarangani%' AND form_interprise='partnership'")
    zdn_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga del norte%' AND form_interprise='partnership'")
    zs_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga sibugay%' AND form_interprise='partnership'")
    zds_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga del sur%' AND form_interprise='partnership'")
    ddo_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao de oro%' AND form_interprise='partnership'")
    do_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao oriental%' AND form_interprise='partnership'")
    ddn_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao del norte%' AND form_interprise='partnership'")
    dds_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao del sur%' AND form_interprise='partnership'")
    doc_partsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao occidental%' AND form_interprise='partnership'")

    adn_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%agusan del norte%' AND form_interprise='corporation'")
    ads_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%agusan del sur%' AND form_interprise='corporation'")
    sds_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%surigao del sur%' AND form_interprise='corporation'")
    magui_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%maguindanao%' AND form_interprise='corporation'")
    ns_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%northern samar%' AND form_interprise='corporation'")
    leyte_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE 'leyte%' AND form_interprise='corporation'")
    sleyte_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%southern leyte%' AND form_interprise='corporation'")
    mo_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%misamis oriental%' AND form_interprise='corporation'")
    bukd_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%bukidnon%' AND form_interprise='corporation'")
    ldn_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%lanao del norte%' AND form_interprise='corporation'")
    nc_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%north cotabato%' AND form_interprise='corporation'")
    sk_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%sultan kudarat%' AND form_interprise='corporation'")
    srng_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%sarangani%' AND form_interprise='corporation'")
    zdn_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga del norte%' AND form_interprise='corporation'")
    zs_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga sibugay%' AND form_interprise='corporation'")
    zds_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%zamboanga del sur%' AND form_interprise='corporation'")
    ddo_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao de oro%' AND form_interprise='corporation'")
    do_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao oriental%' AND form_interprise='corporation'")
    ddn_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao del norte%' AND form_interprise='corporation'")
    dds_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao del sur%' AND form_interprise='corporation'")
    doc_corpsql=db.select("SELECT `business_addr`,`form_interprise` from form_c where business_addr LIKE '%davao occidental%' AND form_interprise='corporation'")

    adn_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%agusan del norte%' AND interprise_other != '' ")
    ads_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%agusan del sur%' AND interprise_other != '' ")
    sds_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%surigao del sur%' AND interprise_other != '' ")
    magui_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%maguindanao%' AND interprise_other != '' ")
    ns_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%northern samar%' AND interprise_other != '' ")
    leyte_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE 'leyte%' AND interprise_other != '' ")
    sleyte_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%southern leyte%' AND interprise_other != '' ")
    mo_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%misamis oriental%' AND interprise_other != '' ")
    bukd_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%bukidnon%' AND interprise_other != '' ")
    ldn_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%lanao del norte%' AND interprise_other != '' ")
    nc_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%north cotabato%' AND interprise_other != '' ")
    sk_othersqll=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%sultan kudarat%' AND interprise_other != '' ")
    srng_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%sarangani%' AND interprise_other != '' ")
    zdn_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%zamboanga del norte%' AND interprise_other != '' ")
    zs_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%zamboanga sibugay%' AND interprise_other != '' ")
    zds_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%zamboanga del sur%' AND interprise_other != '' ")
    ddo_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%davao de oro%' AND interprise_other != '' ")
    do_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%davao oriental%' AND interprise_other != '' ")
    ddn_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%davao del norte%' AND interprise_other != '' ")
    dds_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%davao del sur%' AND interprise_other != '' ")
    doc_othersql=db.select("SELECT `business_addr`,`interprise_other` from form_c where business_addr LIKE '%davao occidental%' AND interprise_other != '' ")
    #------------------------------------

     # filtering industry cluster - gender
    coffee_malesql=db.select("SELECT `industry_cluster`,`sex` from form_c where industry_cluster='coffee' AND sex='male'")
    cacao_malesql=db.select("SELECT `industry_cluster`,`sex` from form_c where industry_cluster='cacao' AND sex='male'")
    coconut_malesql=db.select("SELECT `industry_cluster`,`sex` from form_c where industry_cluster='coconut' AND sex='male'")
    pfn_malesql=db.select("SELECT industry_cluster, sex FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND sex='male'")

    coffee_femalesql=db.select("SELECT `industry_cluster`,`sex` from form_c where industry_cluster='coffee' AND sex='female'")
    cacao_femalesql=db.select("SELECT `industry_cluster`,`sex` from form_c where industry_cluster='cacao' AND sex='female'")
    coconut_femalesql=db.select("SELECT `industry_cluster`,`sex` from form_c where industry_cluster='coconut' AND sex='female'")
    pfn_femalesql=db.select("SELECT industry_cluster, sex FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND sex='female'")
    #----------------------------------------

    # filtering gender - business address
    adn_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%agusan del norte%' AND sex='male'")
    ads_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%agusan del sur%' AND sex='male'")
    sds_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%surigao del sur%' AND sex='male'")
    magui_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%maguindanao%' AND sex='male'")
    ns_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%northern samar%' AND sex='male'")
    leyte_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE 'leyte%' AND sex='male'")
    sleyte_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%southern leyte%' AND sex='male'")
    mo_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%misamis oriental%' AND sex='male'")
    bukd_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%bukidnon%' AND sex='male'")
    ldn_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%lanao del norte%' AND sex='male'")
    nc_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%north cotabato%' AND sex='male'")
    sk_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%sultan kudarat%' AND sex='male'")
    srng_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%sarangani%' AND sex='male'")
    zdn_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%zamboanga del norte%' AND sex='male'")
    zs_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%zamboanga sibugay%' AND sex='male'")
    zds_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%zamboanga del sur%' AND sex='male'")
    ddo_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao de oro%' AND sex='male'")
    do_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao oriental%' AND sex='male'")
    ddn_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao del norte%' AND sex='male'")
    dds_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao del sur%' AND sex='male'")
    doc_malesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao occidental%' AND sex='male'")

    adn_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%agusan del norte%' AND sex='female'")
    ads_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%agusan del sur%' AND sex='female'")
    sds_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%surigao del sur%' AND sex='female'")
    magui_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%maguindanao%' AND sex='female'")
    ns_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%northern samar%' AND sex='female'")
    leyte_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE 'leyte%' AND sex='female'")
    sleyte_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%southern leyte%' AND sex='female'")
    mo_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%misamis oriental%' AND sex='female'")
    bukd_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%bukidnon%' AND sex='female'")
    ldn_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%lanao del norte%' AND sex='female'")
    nc_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%north cotabato%' AND sex='female'")
    sk_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%sultan kudarat%' AND sex='female'")
    srng_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%sarangani%' AND sex='female'")
    zdn_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%zamboanga del norte%' AND sex='female'")
    zs_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%zamboanga sibugay%' AND sex='female'")
    zds_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%zamboanga del sur%' AND sex='female'")
    ddo_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao de oro%' AND sex='female'")
    do_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao oriental%' AND sex='female'")
    ddn_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao del norte%' AND sex='female'")
    dds_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao del sur%' AND sex='female'")
    doc_femalesql=db.select("SELECT `business_addr`,`sex` from form_c where business_addr LIKE '%davao occidental%' AND sex='female'")
    #----------------------------------------

     # filtering industry cluster - business address
    adn_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%agusan del norte%' AND industry_cluster='coffee'")
    ads_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%agusan del sur%' AND industry_cluster='coffee'")
    sds_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%surigao del sur%' AND industry_cluster='coffee'")
    magui_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%maguindanao%' AND industry_cluster='coffee'")
    ns_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%northern samar%' AND industry_cluster='coffee'")
    leyte_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE 'leyte%' AND industry_cluster='coffee'")
    sleyte_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%southern leyte%' AND industry_cluster='coffee'")
    mo_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%misamis oriental%' AND industry_cluster='coffee'")
    bukd_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%bukidnon%' AND industry_cluster='coffee'")
    ldn_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%lanao del norte%' AND industry_cluster='coffee'")
    nc_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%north cotabato%' AND industry_cluster='coffee'")
    sk_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%sultan kudarat%' AND industry_cluster='coffee'")
    srng_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%sarangani%' AND industry_cluster='coffee'")
    zdn_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga del norte%' AND industry_cluster='coffee'")
    zs_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga sibugay%' AND industry_cluster='coffee'")
    zds_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga del sur%' AND industry_cluster='coffee'")
    ddo_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao de oro%' AND industry_cluster='coffee'")
    do_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao oriental%' AND industry_cluster='coffee'")
    ddn_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao del norte%' AND industry_cluster='coffee'")
    dds_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao del sur%' AND industry_cluster='coffee'")
    doc_coffeesql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao occidental%' AND industry_cluster='coffee'")

    adn_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%agusan del norte%' AND industry_cluster='cacao'")
    ads_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%agusan del sur%' AND industry_cluster='cacao'")
    sds_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%surigao del sur%' AND industry_cluster='cacao'")
    magui_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%maguindanao%' AND industry_cluster='cacao'")
    ns_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%northern samar%' AND industry_cluster='cacao'")
    leyte_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE 'leyte%' AND industry_cluster='cacao'")
    sleyte_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%southern leyte%' AND industry_cluster='cacao'")
    mo_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%misamis oriental%' AND industry_cluster='cacao'")
    bukd_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%bukidnon%' AND industry_cluster='cacao'")
    ldn_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%lanao del norte%' AND industry_cluster='cacao'")
    nc_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%north cotabato%' AND industry_cluster='cacao'")
    sk_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%sultan kudarat%' AND industry_cluster='cacao'")
    srng_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%sarangani%' AND industry_cluster='cacao'")
    zdn_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga del norte%' AND industry_cluster='cacao'")
    zs_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga sibugay%' AND industry_cluster='cacao'")
    zds_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga del sur%' AND industry_cluster='cacao'")
    ddo_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao de oro%' AND industry_cluster='cacao'")
    do_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao oriental%' AND industry_cluster='cacao'")
    ddn_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao del norte%' AND industry_cluster='cacao'")
    dds_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao del sur%' AND industry_cluster='cacao'")
    doc_cacaosql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao occidental%' AND industry_cluster='cacao'")

    adn_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%agusan del norte%' AND industry_cluster='coconut'")
    ads_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%agusan del sur%' AND industry_cluster='coconut'")
    sds_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%surigao del sur%' AND industry_cluster='coconut'")
    magui_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%maguindanao%' AND industry_cluster='coconut'")
    ns_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%northern samar%' AND industry_cluster='coconut'")
    leyte_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE 'leyte%' AND industry_cluster='coconut'")
    sleyte_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%southern leyte%' AND industry_cluster='coconut'")
    mo_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%misamis oriental%' AND industry_cluster='coconut'")
    bukd_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%bukidnon%' AND industry_cluster='coconut'")
    ldn_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%lanao del norte%' AND industry_cluster='coconut'")
    nc_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%north cotabato%' AND industry_cluster='coconut'")
    sk_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%sultan kudarat%' AND industry_cluster='coconut'")
    srng_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%sarangani%' AND industry_cluster='coconut'")
    zdn_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga del norte%' AND industry_cluster='coconut'")
    zs_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga sibugay%' AND industry_cluster='coconut'")
    zds_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%zamboanga del sur%' AND industry_cluster='coconut'")
    ddo_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao de oro%' AND industry_cluster='coconut'")
    do_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao oriental%' AND industry_cluster='coconut'")
    ddn_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao del norte%' AND industry_cluster='coconut'")
    dds_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao del sur%' AND industry_cluster='coconut'")
    doc_coconutsql=db.select("SELECT `business_addr`,`industry_cluster` from form_c where business_addr LIKE '%davao occidental%' AND industry_cluster='coconut'")

    adn_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%agusan del norte%'")
    ads_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%agusan del sur%'")
    sds_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%surigao del sur%'")
    magui_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%maguindanao%'")
    ns_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%northern samar%'")
    leyte_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%leyte%'")
    sleyte_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%southern leyte%'")
    mo_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%misamis oriental%'")
    bukd_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%bukidnon%'")
    ldn_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%lanao del norte%'")
    nc_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%north cotabato%'")
    sk_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%sultan kudarat%'")
    srng_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%sarangani%'")
    zdn_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%zamboanga del norte%'")
    zs_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%zamboanga sibugay%'")
    zds_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%zamboanga del sur%'")
    ddo_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%davao de oro%'")
    do_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%davao oriental%'")
    ddn_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%davao del norte%'")
    dds_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%davao del sur%'")
    doc_pfnsql=db.select("SELECT industry_cluster, business_addr FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee' AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' AND business_addr LIKE '%davao occidental%'")
    #----------------------------------------


    count_male_singlesole=len(male_singlesolesql)
    count_female_singlesole=len(female_singlesolesql)
    count_malepartnership=len(male_partnershipsql)
    count_femalepartnership=len(female_partnershipsql)
    count_male_corporation=len(male_corporationsql)
    count_female_corporation=len(female_corporationsql)
    totalsinglesole=len(male_singlesolesql + female_singlesolesql)
    totalpartnership=len(male_partnershipsql + female_partnershipsql)
    totalcorporation=len(male_corporationsql + female_corporationsql)
    count_male_other=len(male_othersql)
    count_female_other=len(female_othersql)
    totalother=len(male_othersql + female_othersql)
    filter1=filter1
    filter2=filter2
    filter3=filter3
    filter4=filter4
    count_coffee_single=len(coffee_singlesolesql)
    count_cacao_single=len(cacao_singlesolesql)
    count_coconut_single=len(coconut_singlesolesql)
    count_pfn_single=len(pfn_singlesolesql)
    total_industrysingle=len(coffee_singlesolesql+cacao_singlesolesql+coconut_singlesolesql+pfn_singlesolesql)
    count_coffeepart=len(coffee_partnershipsql)
    count_cacaopart=len(cacao_partnershipsql)
    count_coconutpart=len(coconut_partnershipsql)
    count_pfnpart=len(pfn_partnershipsql)
    total_industrypart=len(coffee_partnershipsql+cacao_partnershipsql+coconut_partnershipsql+pfn_partnershipsql)
    count_coffeecorp=len(coffee_corporationsql)
    count_cacaocorp=len(cacao_corporationsql)
    count_coconutcorp=len(coconut_corporationsql)
    count_pfncorp=len(pfn_corporationsql)
    total_industrycorp=len(coffee_corporationsql+cacao_corporationsql+coconut_corporationsql+pfn_corporationsql)
    count_coffeeoth=len(coffee_otherql)
    count_cacaooth=len(cacao_othersql)
    count_coconutoth=len(coconut_othersql)
    count_pfnoth=len(pfn_othersql)
    total_industryoth=len(coffee_otherql+cacao_othersql+coconut_othersql+pfn_othersql)
    adn_singlesql=len(adn_singlesql)
    ads_singlesql=len(ads_singlesql)
    sds_singlesql=len(sds_singlesql)
    magui_singlesql=len(magui_singlesql)
    ns_singlesql=len(ns_singlesql)
    leyte_singlesql=len(leyte_singlesql)
    sleyte_singlesql=len(sleyte_singlesql)
    mo_singlesql=len(mo_singlesql)
    bukd_singlesql=len(bukd_singlesql)
    ldn_singlesql=len(ldn_singlesql)
    nc_singlesql=len(nc_singlesql)
    sk_singlesql=len(sk_singlesql)
    srng_singlesql=len(srng_singlesql)
    zdn_singlesql=len(zdn_singlesql)
    zs_singlesql=len(zs_singlesql)
    zds_singlesql=len(zds_singlesql)
    ddo_singlesql=len(ddo_singlesql)
    do_singlesql=len(do_singlesql)
    ddn_singlesql=len(ddn_singlesql)
    dds_singlesql=len(dds_singlesql)
    doc_singlesql=len(doc_singlesql)
    total_addrsingle=(adn_singlesql+ads_singlesql+sds_singlesql+magui_singlesql+ns_singlesql+leyte_singlesql
    +sleyte_singlesql+mo_singlesql+bukd_singlesql+ldn_singlesql+nc_singlesql+sk_singlesql+srng_singlesql+zdn_singlesql+zs_singlesql+zds_singlesql+ddo_singlesql+do_singlesql+ddn_singlesql+
    dds_singlesql+doc_singlesql)
    adn_partsql=len(adn_partsql)
    ads_partsql=len(ads_partsql)
    sds_partsql=len(sds_partsql)
    magui_partsql=len(magui_partsql)
    ns_partsql=len(ns_partsql)
    leyte_partsql=len(leyte_partsql)
    sleyte_partsql=len(sleyte_partsql)
    mo_partsql=len(mo_partsql)
    bukd_partsql=len(bukd_partsql)
    ldn_partsql=len(ldn_partsql)
    nc_partsql=len(nc_partsql)
    sk_partsql=len(sk_partsql)
    srng_partsql=len(srng_partsql)
    zdn_partsql=len(zdn_partsql)
    zs_partsql=len(zs_partsql)
    zds_partsql=len(zds_partsql)
    ddo_partsql=len(ddo_partsql)
    do_partsql=len(do_partsql)
    ddn_partsql=len(ddn_partsql)
    dds_partsql=len(dds_partsql)
    doc_partsql=len(doc_partsql)
    total_addrpart=(adn_partsql+ads_partsql+sds_partsql+magui_partsql+ns_partsql+
    leyte_partsql+sleyte_partsql+mo_partsql+bukd_partsql+ldn_partsql+nc_partsql+sk_partsql+srng_partsql+zdn_partsql+zs_partsql+zds_partsql+ddo_partsql+do_partsql+ddn_partsql+dds_partsql+doc_partsql)
    adn_corpsql1=len(adn_corpsql)
    ads_corpsq2=len(ads_corpsql)
    sds_corpsql3=len(sds_corpsql)
    magui_corpsq4=len(magui_corpsql)
    ns_corpsql5=len(ns_corpsql)
    leyte_corsql6=len(leyte_corpsql)
    sleyte_corpsql7=len(sleyte_corpsql)
    mo_corpsql8=len(mo_corpsql)
    bukd_corpsql9=len(bukd_corpsql)
    ldn_corpsql10=len(ldn_corpsql)
    nc_corpsql11=len(nc_corpsql)
    sk_corpsql12=len(sk_corpsql)
    srng_corpsql13=len(srng_corpsql)
    zdn_corpsql14=len(zdn_corpsql)
    zs_corpsql15=len(zs_corpsql)
    zds_corpsql16=len(zds_corpsql)
    ddo_corpsql17=len(ddo_corpsql)
    do_corpsql18=len(do_corpsql)
    ddn_corpsql19=len(ddn_corpsql)
    dds_corpsql20=len(dds_corpsql)
    doc_corpsql21=len(doc_corpsql)
    total_addrcorp=(adn_corpsql1+ads_corpsq2+sds_corpsql3+magui_corpsq4+ns_corpsql5+leyte_corsql6+sleyte_corpsql7+mo_corpsql8+bukd_corpsql9+ldn_corpsql10+nc_corpsql11+sk_corpsql12+srng_corpsql13+zdn_corpsql14+zs_corpsql15+zds_corpsql16+ddo_corpsql17+do_corpsql18+ddn_corpsql19+dds_corpsql20+doc_corpsql21)
    coffee_malesql=len(coffee_malesql)
    cacao_malesql=len(cacao_malesql)
    coconut_malesql=len(coconut_malesql)
    pfn_malesql=len(pfn_malesql)
    coffee_femalesql=len(coffee_femalesql)
    cacao_femalesql=len(cacao_femalesql)
    coconut_femalesql=len(coconut_femalesql)
    pfn_femalesql=len(pfn_femalesql)
    total_coffeegender=(coffee_malesql+coffee_femalesql)
    total_cacaogender=(cacao_malesql+cacao_femalesql)
    total_coconutgender=(coconut_malesql+coconut_femalesql)
    total_pfngender=(pfn_malesql+pfn_femalesql)
    adn_malesql=len(adn_malesql)
    ads_malesql=len(ads_malesql)
    sds_malesql=len(sds_malesql)
    magui_malesql=len(magui_malesql)
    ns_malesql=len(ns_malesql)
    leyte_malesql=len(leyte_malesql)
    sleyte_malesql=len(sleyte_malesql)
    mo_malesql=len(mo_malesql)
    bukd_malesql=len(bukd_malesql)
    ldn_malesql=len(ldn_malesql)
    nc_malesql=len(nc_malesql)
    sk_malesql=len(sk_malesql)
    srng_malesql=len(srng_malesql)
    zdn_malesql=len(zdn_malesql)
    zs_malesql=len(zs_malesql)
    zds_malesql=len(zds_malesql)
    ddo_malesql=len(ddo_malesql)
    do_malesql=len(do_malesql)
    ddn_malesql=len(ddn_malesql)
    dds_malesql=len(dds_malesql)
    doc_malesql=len(doc_malesql)
    adn_femalesql1=len(adn_femalesql)
    ads_femalesql2=len(ads_femalesql)
    sds_femalesql3=len(sds_femalesql)
    magui_femalesql4=len(magui_femalesql)
    ns_femalesql5=len(ns_femalesql)
    leyte_femalesql6=len(leyte_femalesql)
    sleyte_femalesql7=len(sleyte_femalesql)
    mo_femalesql8=len(mo_femalesql)
    bukd_femalesql9=len(bukd_femalesql)
    ldn_femalesql10=len(ldn_femalesql)
    nc_femalesql11=len(nc_femalesql)
    sk_femalesql12=len(sk_femalesql)
    srng_femalesql13=len(srng_femalesql)
    zdn_femalesql14=len(zdn_femalesql)
    zs_femalesql15=len(zs_femalesql)
    zds_femalesql16=len(zds_femalesql)
    ddo_femalesql17=len(ddo_femalesql)
    do_femaleql18=len(do_femalesql)
    ddn_femalesql19=len(ddn_femalesql)
    dds_femalesql20=len(dds_femalesql)
    doc_femalesql21=len(doc_femalesql)
    total_maleaddr=(adn_malesql+ads_malesql+sds_malesql+magui_malesql+ns_malesql+leyte_malesql+sleyte_malesql+mo_malesql+bukd_malesql+ldn_malesql+nc_malesql+sk_malesql+srng_malesql+
    zdn_malesql+zs_malesql+zds_malesql+ddo_malesql+do_malesql+ddn_malesql+dds_malesql+doc_malesql)
    total_femaleaddr=(adn_femalesql1+ads_femalesql2+sds_femalesql3+magui_femalesql4+ns_femalesql5+leyte_femalesql6+sleyte_femalesql7+mo_femalesql8+bukd_femalesql9+ldn_femalesql10+nc_femalesql11+sk_femalesql12+srng_femalesql13+zdn_femalesql14+zs_femalesql15+zds_femalesql16+ddo_femalesql17+do_femaleql18+ddn_femalesql19+dds_femalesql20+doc_femalesql21)
    adn_coffeesql=len(adn_coffeesql)
    ads_coffeesql=len(ads_coffeesql)
    sds_coffeesql=len(sds_coffeesql)
    magui_coffeesql=len(magui_coffeesql)
    ns_coffeesql=len(ns_coffeesql)
    leyte_coffeesql=len(leyte_coffeesql)
    sleyte_coffeesql=len(sleyte_coffeesql)
    mo_coffeesql=len(mo_coffeesql)
    bukd_coffeesql=len(bukd_coffeesql)
    ldn_coffeesql=len(ldn_coffeesql)
    nc_coffeesql=len(nc_coffeesql)
    sk_coffeesql=len(sk_coffeesql)
    srng_coffeesql=len(srng_coffeesql)
    zdn_coffeesql=len(zdn_coffeesql)
    zs_coffeesql=len(zs_coffeesql)
    zds_coffeesql=len(zds_coffeesql)
    ddo_coffeesql=len(ddo_coffeesql)
    do_coffeesql=len(do_coffeesql)
    ddn_coffeesql=len(ddn_coffeesql)
    dds_coffeesql=len(dds_coffeesql)
    doc_coffeesql=len(doc_coffeesql)
    adn_cacaosql=len(adn_cacaosql)
    ads_cacaosql=len(ads_cacaosql)
    sds_cacaosql=len(sds_cacaosql)
    magui_cacaosql=len(magui_cacaosql)
    ns_cacaosql=len(ns_cacaosql)
    leyte_cacaosql=len(leyte_cacaosql)
    sleyte_cacaosql=len(sleyte_cacaosql)
    mo_cacaosql=len(mo_cacaosql)
    bukd_cacaosql=len(bukd_cacaosql)
    ldn_cacaosql=len(ldn_cacaosql)
    nc_cacaosql=len(nc_cacaosql)
    sk_cacaosql=len(sk_cacaosql)
    srng_cacaosql=len(srng_cacaosql)
    zdn_cacaosql=len(zdn_cacaosql)
    zs_cacaosql=len(zs_cacaosql)
    zds_cacaosql=len(zds_cacaosql)
    ddo_cacaosql=len(ddo_cacaosql)
    do_cacaosql=len(do_cacaosql)
    ddn_cacaosql=len(ddn_cacaosql)
    dds_cacaosql=len(dds_cacaosql)
    doc_cacaosql=len(doc_cacaosql)
    adn_coconutsql=len(adn_coconutsql)
    ads_coconutsql=len(ads_coconutsql)
    sds_coconutsql=len(sds_coconutsql)
    magui_coconutsql=len(magui_coconutsql)
    ns_coconutsql=len(ns_coconutsql)
    leyte_coconutsql=len(leyte_coconutsql)
    sleyte_coconutsql=len(sleyte_coconutsql)
    mo_coconutsql=len(mo_coconutsql)
    bukd_coconutsql=len(bukd_coconutsql)
    ldn_coconutsql=len(ldn_coconutsql)
    nc_coconutsql=len(nc_coconutsql)
    sk_coconutsql=len(sk_coconutsql)
    srng_coconutsql=len(srng_coconutsql)
    zdn_coconutsql=len(zdn_coconutsql)
    zs_coconutsql=len(zs_coconutsql)
    zds_coconutsql=len(zds_coconutsql)
    ddo_coconutsql=len(ddo_coconutsql)
    do_coconutsql=len(do_coconutsql)
    ddn_coconutsql=len(ddn_coconutsql)
    dds_coconutsql=len(dds_coconutsql)
    doc_coconutsql=len(doc_coconutsql)
    adn_pfnsql=len(adn_pfnsql)
    ads_pfnsql=len(ads_pfnsql)
    sds_pfnsql=len(sds_pfnsql)
    magui_pfnsql=len(magui_pfnsql)
    ns_pfnsql=len(ns_pfnsql)
    leyte_pfnsql=len(leyte_pfnsql)
    sleyte_pfnsql=len(sleyte_pfnsql)
    mo_pfnsql=len(mo_pfnsql)
    bukd_pfnsql=len(bukd_pfnsql)
    ldn_pfnsql=len(ldn_pfnsql)
    nc_pfnsql=len(nc_pfnsql)
    sk_pfnsql=len(sk_pfnsql)
    srng_pfnsql=len(srng_pfnsql)
    zdn_pfnsql=len(zdn_pfnsql)
    zs_pfnsql=len(zs_pfnsql)
    zds_pfnsql=len(zds_pfnsql)
    ddo_pfnsql=len(ddo_pfnsql)
    do_pfnsql=len(do_pfnsql)
    ddn_pfnsql=len(ddn_pfnsql)
    dds_pfnsql=len(dds_pfnsql)
    doc_pfnsql=len(doc_pfnsql)
    total_coffeeaddr=(adn_coffeesql+ads_coffeesql+sds_coffeesql+
    magui_coffeesql+ns_coffeesql+leyte_coffeesql+sleyte_coffeesql+mo_coffeesql+bukd_coffeesql+
    ldn_coffeesql+nc_coffeesql+sk_coffeesql+srng_coffeesql+zdn_coffeesql+zs_coffeesql+zds_coffeesql+
    ddo_coffeesql+do_coffeesql+ddn_coffeesql+dds_coffeesql+doc_coffeesql)
    total_cacaoaddr=(adn_cacaosql+ads_cacaosql+sds_cacaosql+
    magui_cacaosql+ns_cacaosql+leyte_cacaosql+sleyte_cacaosql+mo_cacaosql+bukd_cacaosql+
    ldn_cacaosql+nc_cacaosql+sk_cacaosql+srng_cacaosql+zdn_cacaosql+zs_cacaosql+zds_cacaosql+
    ddo_cacaosql+do_cacaosql+ddn_cacaosql+dds_cacaosql+doc_cacaosql)
    total_coconutaddr=(adn_coconutsql+ads_coconutsql+sds_coconutsql+
    magui_coconutsql+ns_coconutsql+leyte_coconutsql+sleyte_coconutsql+mo_coconutsql+bukd_coconutsql+
    ldn_coconutsql+nc_coconutsql+sk_coconutsql+srng_coconutsql+zdn_coconutsql+zs_coconutsql+zds_coconutsql+
    ddo_coconutsql+do_coconutsql+ddn_coconutsql+dds_coconutsql+doc_coconutsql)
    total_pfnaddr=(adn_pfnsql+ads_pfnsql+sds_pfnsql+
    magui_pfnsql+ns_pfnsql+leyte_pfnsql+sleyte_pfnsql+mo_pfnsql+bukd_pfnsql+
    ldn_pfnsql+nc_pfnsql+sk_pfnsql+srng_pfnsql+zdn_pfnsql+zs_pfnsql+zds_pfnsql+
    ddo_pfnsql+do_pfnsql+ddn_pfnsql+dds_pfnsql+doc_pfnsql)
    datatable=datatable
    maless=male_singlesolesql
    femaless=female_singlesolesql


    return{
        'count_male_singlesole': count_male_singlesole,
'count_female_singlesole': count_female_singlesole,
'count_malepartnership': count_malepartnership,
'count_femalepartnership': count_femalepartnership,
'count_male_corporation': count_male_corporation,
'count_female_corporation': count_female_corporation,
'totalsinglesole': totalsinglesole,
'totalpartnership': totalpartnership,
'totalcorporation': totalcorporation,
'count_male_other': count_male_other,
'count_female_other': count_female_other,
'totalother': totalother,
'filter1': filter1,
'filter2': filter2,
'filter3': filter3,
'filter4': filter4,
'count_coffee_single': count_coffee_single,
'count_cacao_single': count_cacao_single,
'count_coconut_single': count_coconut_single,
'count_pfn_single': count_pfn_single,
'total_industrysingle': total_industrysingle,
'count_coffeepart': count_coffeepart,
'count_cacaopart': count_cacaopart,
'count_coconutpart': count_coconutpart,
'count_pfnpart': count_pfnpart,
'total_industrypart': total_industrypart,
'count_coffeecorp': count_coffeecorp,
'count_cacaocorp': count_cacaocorp,
'count_coconutcorp': count_coconutcorp,
'count_pfncorp': count_pfncorp,
'total_industrycorp': total_industrycorp,
'count_coffeeoth': count_coffeeoth,
'count_cacaooth': count_cacaooth,
'count_coconutoth': count_coconutoth,
'count_pfnoth': count_pfnoth,
'total_industryoth': total_industryoth,
'adn_singlesql': adn_singlesql,
'ads_singlesql': ads_singlesql,
'sds_singlesql': sds_singlesql,
'magui_singlesql': magui_singlesql,
'ns_singlesql': ns_singlesql,
'leyte_singlesql': leyte_singlesql,
'sleyte_singlesql': sleyte_singlesql,
'mo_singlesql': mo_singlesql,
'bukd_singlesql': bukd_singlesql,
'ldn_singlesql': ldn_singlesql,
'nc_singlesql': nc_singlesql,
'sk_singlesql': sk_singlesql,
'srng_singlesql': srng_singlesql,
'zdn_singlesql': zdn_singlesql,
'zs_singlesql': zs_singlesql,
'zds_singlesql': zds_singlesql,
'ddo_singlesql': ddo_singlesql,
'do_singlesql': do_singlesql,
'ddn_singlesql': ddn_singlesql,
'dds_singlesql': dds_singlesql,
'doc_singlesql': doc_singlesql,
'total_addrsingle': total_addrsingle,
'adn_partsql': adn_partsql,
'ads_partsql': ads_partsql,
'sds_partsql': sds_partsql,
'magui_partsql': magui_partsql,
'ns_partsql': ns_partsql,
'leyte_partsql': leyte_partsql,
'sleyte_partsql': sleyte_partsql,
'mo_partsql': mo_partsql,
'bukd_partsql': bukd_partsql,
'ldn_partsql': ldn_partsql,
'nc_partsql': nc_partsql,
'sk_partsql': sk_partsql,
'srng_partsql': srng_partsql,
'zdn_partsql': zdn_partsql,
'zs_partsql': zs_partsql,
'zds_partsql': zds_partsql,
'ddo_partsql': ddo_partsql,
'do_partsql': do_partsql,
'ddn_partsql': ddn_partsql,
'dds_partsql': dds_partsql,
'doc_partsql': doc_partsql,
'total_addrpart': total_addrpart,
'adn_corpsql': adn_corpsql,
'ads_corpsql': ads_corpsql,
'sds_corpsql': sds_corpsql,
'magui_corpsql': magui_corpsql,
'ns_corpsql': ns_corpsql,
'leyte_corsql': leyte_corsql6,
'sleyte_corpsql': sleyte_corpsql,
'mo_corpsql': mo_corpsql,
'bukd_corpsql': bukd_corpsql,
'ldn_corpsql': ldn_corpsql,
'nc_corpsql': nc_corpsql,
'sk_corpsql': sk_corpsql,
'srng_corpsql': srng_corpsql,
'zdn_corpsql': zdn_corpsql,
'zs_corpsql': zs_corpsql,
'zds_corpsql': zds_corpsql,
'ddo_corpsql': ddo_corpsql,
'do_corpsql': do_corpsql,
'ddn_corpsql': ddn_corpsql,
'dds_corpsql': dds_corpsql,
'doc_corpsql': doc_corpsql,
'total_addrcorp': total_addrcorp,
'coffee_malesql': coffee_malesql,
'cacao_malesql': cacao_malesql,
'coconut_malesql': coconut_malesql,
'pfn_malesql': pfn_malesql,
'coffee_femalesql': coffee_femalesql,
'cacao_femalesql': cacao_femalesql,
'coconut_femalesql': coconut_femalesql,
'pfn_femalesql': pfn_femalesql,
'total_coffeegender': total_coffeegender,
'total_cacaogender': total_cacaogender,
'total_coconutgender': total_coconutgender,
'total_pfngender': total_pfngender,
'adn_malesql': adn_malesql,
'ads_malesql': ads_malesql,
'sds_malesql': sds_malesql,
'magui_malesql': magui_malesql,
'ns_malesql': ns_malesql,
'leyte_malesql': leyte_malesql,
'sleyte_malesql': sleyte_malesql,
'mo_malesql': mo_malesql,
'bukd_malesql': bukd_malesql,
'ldn_malesql': ldn_malesql,
'nc_malesql': nc_malesql,
'sk_malesql': sk_malesql,
'srng_malesql': srng_malesql,
'zdn_malesql': zdn_malesql,
'zs_malesql': zs_malesql,
'zds_malesql': zds_malesql,
'ddo_malesql': ddo_malesql,
'do_malesql': do_malesql,
'ddn_malesql': ddn_malesql,
'dds_malesql': dds_malesql,
'doc_malesql': doc_malesql,
'adn_femalesql1' : adn_femalesql1,
'ads_femalesql2' : ads_femalesql2,
'sds_femalesql3' : sds_femalesql3,
'magui_females' : magui_femalesql4,
'ns_femalesql5' : ns_femalesql5,
'leyte_femalesql6' : leyte_femalesql6,
'sleyte_femalesql7' : sleyte_femalesql7,
'mo_femalesql8' : mo_femalesql8,
'bukd_femalesql' : bukd_femalesql9,
'ldn_femalesql10' : ldn_femalesql10,
'nc_femalesql11' : nc_femalesql11,
'sk_femalesql12' : sk_femalesql12,
'srng_femalesql' : srng_femalesql13,
'zdn_femalesql14' : zdn_femalesql14,
'zs_femalesql15' : zs_femalesql15,
'zds_femalesql16' : zds_femalesql16,
'ddo_femalesql17' : ddo_femalesql17,
'do_femaleql18' : do_femaleql18,
'ddn_femalesql19' : ddn_femalesql19,
'dds_femalesql20' : dds_femalesql20,
'doc_femalesql21' : doc_femalesql21,
'total_maleaddr' : total_maleaddr,
'total_femaleaddr': total_femaleaddr,
'adn_coffeesql': adn_coffeesql,
'ads_coffeesql': ads_coffeesql,
'sds_coffeesql': sds_coffeesql,
'magui_coffeesql': magui_coffeesql,
'ns_coffeesql': ns_coffeesql,
'leyte_coffeesql': leyte_coffeesql,
'sleyte_coffeesql': sleyte_coffeesql,
'mo_coffeesql': mo_coffeesql,
'bukd_coffeesql': bukd_coffeesql,
'ldn_coffeesql': ldn_coffeesql,
'nc_coffeesql': nc_coffeesql,
'sk_coffeesql': sk_coffeesql,
'srng_coffeesql': srng_coffeesql,
'zdn_coffeesql': zdn_coffeesql,
'zs_coffeesql': zs_coffeesql,
'zds_coffeesql': zds_coffeesql,
'ddo_coffeesql': ddo_coffeesql,
'do_coffeesql': do_coffeesql,
'ddn_coffeesql': ddn_coffeesql,
'dds_coffeesql': dds_coffeesql,
'doc_coffeesql': doc_coffeesql,
'adn_cacaosql': adn_cacaosql,
'ads_cacaosql': ads_cacaosql,
'sds_cacaosql': sds_cacaosql,
'magui_cacaosql': magui_cacaosql,
'ns_cacaosql': ns_cacaosql,
'leyte_cacaosql': leyte_cacaosql,
'sleyte_cacaosql': sleyte_cacaosql,
'mo_cacaosql': mo_cacaosql,
'bukd_cacaosql': bukd_cacaosql,
'ldn_cacaosql': ldn_cacaosql,
'nc_cacaosql': nc_cacaosql,
'sk_cacaosql': sk_cacaosql,
'srng_cacaosql': srng_cacaosql,
'zdn_cacaosql': zdn_cacaosql,
'zs_cacaosql': zs_cacaosql,
'zds_cacaosql': zds_cacaosql,
'ddo_cacaosql': ddo_cacaosql,
'do_cacaosql': do_cacaosql,
'ddn_cacaosql': ddn_cacaosql,
'dds_cacaosql': dds_cacaosql,
'doc_cacaosql': doc_cacaosql,
'adn_coconutsql': adn_coconutsql,
'ads_coconutsql': ads_coconutsql,
'sds_coconutsql': sds_coconutsql,
'magui_coconutsql': magui_coconutsql,
'ns_coconutsql': ns_coconutsql,
'leyte_coconutsql': leyte_coconutsql,
'sleyte_coconutsql': sleyte_coconutsql,
'mo_coconutsql': mo_coconutsql,
'bukd_coconutsql': bukd_coconutsql,
'ldn_coconutsql': ldn_coconutsql,
'nc_coconutsql': nc_coconutsql,
'sk_coconutsql': sk_coconutsql,
'srng_coconutsql': srng_coconutsql,
'zdn_coconutsql': zdn_coconutsql,
'zs_coconutsql': zs_coconutsql,
'zds_coconutsql': zds_coconutsql,
'ddo_coconutsql': ddo_coconutsql,
'do_coconutsql': do_coconutsql,
'ddn_coconutsql': ddn_coconutsql,
'dds_coconutsql': dds_coconutsql,
'doc_coconutsql': doc_coconutsql,
'adn_pfnsql': adn_pfnsql,
'ads_pfnsql': ads_pfnsql,
'sds_pfnsql': sds_pfnsql,
'magui_pfnsql': magui_pfnsql,
'ns_pfnsql': ns_pfnsql,
'leyte_pfnsql': leyte_pfnsql,
'sleyte_pfnsql': sleyte_pfnsql,
'mo_pfnsql': mo_pfnsql,
'bukd_pfnsql': bukd_pfnsql,
'ldn_pfnsql': ldn_pfnsql,
'nc_pfnsql': nc_pfnsql,
'sk_pfnsql': sk_pfnsql,
'srng_pfnsql': srng_pfnsql,
'zdn_pfnsql': zdn_pfnsql,
'zs_pfnsql': zs_pfnsql,
'zds_pfnsql': zds_pfnsql,
'ddo_pfnsql': ddo_pfnsql,
'do_pfnsql': do_pfnsql,
'ddn_pfnsql': ddn_pfnsql,
'dds_pfnsql': dds_pfnsql,
'doc_pfnsql': doc_pfnsql,
'total_coffeeaddr': total_coffeeaddr,
'total_coconutaddr': total_coconutaddr,
'total_cacaoaddr':total_cacaoaddr,
'total_pfnaddr': total_pfnaddr,
'datatable': datatable,
'maless': maless,
'femaless': femaless,
    }
