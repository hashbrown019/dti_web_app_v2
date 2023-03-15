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
    select_countform1=db.select("SELECT * FROM dcf_prep_review_aprv_status")
    select_countform2=db.select("SELECT * FROM dcf_implementing_unit")
    select_countform3=db.select("SELECT * FROM dcf_bdsp_reg")
    select_countform4=db.select("SELECT * FROM dcf_capacity_building")
    select_countform5=db.select("SELECT * FROM dcf_matching_grant")
    select_countform6=db.select("SELECT * FROM dcf_product_development")
    select_countform7=db.select("SELECT * FROM dcf_trade_promotion")
    select_countform9=db.select("SELECT * FROM dcf_enablers_activity")
    dcf_form5=len(select_countform5)
    dcf_form4=len(select_countform4)
    dcf_form3=len(select_countform3)
    dcf_form2=len(select_countform2)
    dcf_form1=len(select_countform1)
    dcf_form6=len(select_countform6)
    dcf_form7=len(select_countform7)
    dcf_form9=len(select_countform9)
    return{
        'USER_INFO':  USER_INFO,
        'dcf_form1': dcf_form1,
        'dcf_form2': dcf_form2,
        'dcf_form3': dcf_form3,
        'dcf_form4': dcf_form4,
        'dcf_form5': dcf_form5,
        'dcf_form6': dcf_form6,
        'dcf_form7': dcf_form7,
        'dcf_form9': dcf_form9

    }


def display__():
    if(is_on_session()):
        pass
    else:
        return redirect("/login?force_url=1")
        
    USER_INFO = session["USER_DATA"]
    select_countform1=db.select("SELECT * FROM dcf_prep_review_aprv_status {} ".format(position_data_filter()))
    select_countform2=db.select("SELECT * FROM dcf_implementing_unit {} ".format(position_data_filter()))
    select_countform3=db.select("SELECT * FROM dcf_bdsp_reg {} ".format(position_data_filter()))
    select_countform4=db.select("SELECT * FROM dcf_capacity_building {} ".format(position_data_filter()))
    select_countform5=db.select("SELECT * FROM dcf_matching_grant {} ".format(position_data_filter()))
    select_countform6=db.select("SELECT * FROM dcf_product_development {} ".format(position_data_filter()))
    select_countform7=db.select("SELECT * FROM dcf_trade_promotion {} ".format(position_data_filter()))
    select_countform9=db.select("SELECT * FROM dcf_enablers_activity {} ".format(position_data_filter()))
    dcf_form5=len(select_countform5)
    dcf_form4=len(select_countform4)
    dcf_form3=len(select_countform3)
    dcf_form2=len(select_countform2)
    dcf_form1=len(select_countform1)
    dcf_form6=len(select_countform6)
    dcf_form7=len(select_countform7)
    dcf_form9=len(select_countform9)
    return{
        'USER_INFO':  USER_INFO,
        'dcf_form1': dcf_form1,
        'dcf_form2': dcf_form2,
        'dcf_form3': dcf_form3,
        'dcf_form4': dcf_form4,
        'dcf_form5': dcf_form5,
        'dcf_form6': dcf_form6,
        'dcf_form7': dcf_form7,
        'dcf_form9': dcf_form9
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
