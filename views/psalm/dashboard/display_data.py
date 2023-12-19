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
    data_count_entry=db.select("SELECT * FROM form_c")
    datatable=db.select("SELECT * FROM form_c")
    data_jan = db.select("SELECT * FROM form_c WHERE YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)")
    data_feb= db.select("SELECT * FROM form_c WHERE YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)")
    data_march= db.select("SELECT * FROM form_c WHERE YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)")
    data_april = db.select("SELECT * FROM form_c WHERE YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)")
    data_count_reg_business = db.select("SELECT reg_businessname FROM form_c")
    data_count_position_firm = db.select("SELECT position_firm FROM form_c where position_firm LIKE '%owner%'")
    data_count_cacao = db.select("SELECT * FROM form_c where industry_cluster = 'cacao'")
    data_count_coffee = db.select("SELECT * FROM form_c where industry_cluster = 'coffee'")
    data_count_coconut = db.select("SELECT * FROM form_c where industry_cluster = 'coconut'")
    data_count_pfn = db.select("SELECT industry_cluster FROM `form_c` WHERE industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee'  AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' ")
    intpfn= len(data_count_pfn)
    totalpfn = intpfn
    print(data_count_entry)
    thismonth=len(data_april)
    lastmonth=len(data_march)
    subperc= thismonth - lastmonth
    percentage= (subperc / lastmonth)
    all = data_count_cacao + data_count_coffee + data_count_coconut + data_count_pfn
    count_entry=len(data_count_entry)
    tabledata=data_count_entry
    count_reg_business=len(data_count_reg_business) 
    count_position_firm=len(data_count_position_firm)
    count_cacao=len(data_count_cacao)
    count_coffee=len(data_count_coffee)
    count_pfn=len(data_count_pfn)
    count_coconut=len(data_count_coconut)
    datatable=datatable
    data_jan=len(data_jan)
    data_march=len(data_march)
    data_feb=len(data_feb)
    data_april=len(data_april)
    percentages = round(percentage,2)
    totalpfn =totalpfn
    return{
        'USER_INFO':  USER_INFO,
        'tabledata':  tabledata,
        'data_count_entry':  data_count_entry,
        'datatable':  datatable,
        'data_jan':  data_jan,
        'data_march':  data_march,
        'data_april':  data_april,
        'data_feb':  data_feb,
        'data_count_reg_business':  data_count_reg_business,
        'data_count_position_firm':  data_count_position_firm,
        'data_count_cacao':  data_count_cacao,
        'data_count_coffee':  data_count_coffee,
        'data_count_coconut':  data_count_coconut,
        'data_count_pfn':  data_count_pfn,
        'intpfn':  intpfn,
        'totalpfn':  totalpfn,
        'thismonth':  thismonth,
        'lastmonth':  lastmonth,
        'subperc':  subperc,
        'percentage':  percentage,
        'percentages':  percentages,
        'all':  all,
        'count_entry':  count_entry,
        'count_reg_business':  count_reg_business,
        'count_position_firm':  count_position_firm,
        'count_cacao':  count_cacao,
        'count_coffee':  count_coffee,
        'count_pfn':  count_pfn,
        'count_coconut':  count_coconut
    }


def display__():
    if(is_on_session()):
        pass
    else:
        return redirect("/login?force_url=1")
        
    USER_INFO = session["USER_DATA"]
    data_count_entry=db.select("SELECT * FROM form_c {} ".format(position_data_filter()))
    datatable=db.select("SELECT * FROM form_c {};".format(position_data_filter()))
    data_jan = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 10 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 11 MONTH)".format(position_data_filter()))
    data_feb= db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 10 MONTH)".format(position_data_filter()))
    data_march = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    data_april = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    data_may = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    data_june= db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    data_july = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    data_august = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    data_sept = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    data_oct =db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    data_nov = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    data_dec = db.select("SELECT * FROM form_c {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    data_count_reg_business = db.select("SELECT reg_businessname FROM form_c {} ".format(position_data_filter()))
    data_count_position_firm = db.select("SELECT position_firm FROM form_c {} AND position_firm LIKE '%owner%'".format(position_data_filter()))
    data_count_cacao = db.select("SELECT * FROM form_c {} AND industry_cluster = 'cacao'".format(position_data_filter()))
    data_count_coffee = db.select("SELECT * FROM form_c {} AND industry_cluster = 'coffee'".format(position_data_filter()))
    data_count_coconut = db.select("SELECT * FROM form_c {} AND industry_cluster = 'coconut'".format(position_data_filter()))
    data_count_pfn = db.select("SELECT industry_cluster FROM `form_c` {} AND industry_cluster !='cacao' AND industry_cluster !='coconut' AND industry_cluster !='coffee'  AND industry_cluster != '' AND industry_cluster!= ' ' AND industry_cluster NOT LIKE '%cacao%' AND industry_cluster NOT LIKE '%coconut%' AND industry_cluster NOT LIKE '%coffee%' ".format(position_data_filter()))
    intpfn= len(data_count_pfn)
    totalpfn = intpfn
    thismonth=len(data_dec)
    lastmonth=len(data_nov)
    subperc= thismonth - lastmonth
    try: percentage= (subperc / lastmonth)
    except Exception as e: percentage = 0
    # return data_count_coffee
    all = data_count_cacao + data_count_coffee + data_count_coconut + data_count_pfn
    count_entry=len(data_count_entry)
    tabledata=data_count_entry
    count_reg_business=len(data_count_reg_business) 
    count_position_firm=len(data_count_position_firm)
    count_cacao=len(data_count_cacao)
    count_coffee=len(data_count_coffee)
    count_pfn=len(data_count_pfn)
    count_coconut=len(data_count_coconut)
    datatable=datatable
    data_jan=len(data_jan)
    data_feb=len(data_feb)
    data_march=len(data_march)
    data_april=len(data_april)
    data_may=len(data_may)
    data_june=len(data_june)
    data_july=len(data_july)
    data_august=len(data_august)
    data_sept=len(data_sept)
    data_oct=len(data_oct)
    data_nov=len(data_nov)

    percentages = round(percentage,2)
    totalpfn =totalpfn
    return{
        'USER_INFO':  USER_INFO,
        'tabledata':  tabledata,
        'data_count_entry':  data_count_entry,
        'datatable':  datatable,
        'data_jan':  data_jan,
        'data_feb':  data_feb,
        'data_march':  data_march,
        'data_april':  data_april,
        'data_may':  data_may,
        'data_june':  data_june,
        'data_july':  data_july,
        'data_august':  data_august,
        'data_sept':  data_sept,
        'data_oct':  data_oct,
        'data_nov':  data_nov,
        'data_dec':  data_dec,
        'data_count_reg_business':  data_count_reg_business,
        'data_count_position_firm':  data_count_position_firm,
        'data_count_cacao':  data_count_cacao,
        'data_count_coffee':  data_count_coffee,
        'data_count_coconut':  data_count_coconut,
        'data_count_pfn':  data_count_pfn,
        'intpfn':  intpfn,
        'totalpfn':  totalpfn,
        'thismonth':  thismonth,
        'lastmonth':  lastmonth,
        'subperc':  subperc,
        'percentage':  percentage,
        'percentages':  percentages,
        'all':  all,
        'count_entry':  count_entry,
        'count_reg_business':  count_reg_business,
        'count_position_firm':  count_position_firm,
        'count_cacao':  count_cacao,
        'count_coffee':  count_coffee,
        'count_pfn':  count_pfn,
        'count_coconut':  count_coconut
    }

def position_data_filter():
    _filter = "WHERE 1 "
    JOB = session["USER_DATA"][0]["job"].lower()

    if(JOB in "admin" or JOB in "super admin"):
        session["USER_DATA"][0]["office"] = "NPCO"
        _filter = "WHERE 1 "
    else:
        session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
        _filter = "WHERE  upload_by in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])

    return _filter
