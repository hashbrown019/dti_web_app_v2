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
    form1_datatable=db.select("SELECT * FROM dcf_prep_review_aprv_status {};".format(position_data_filter()))
    form2_datatable=db.select("SELECT * FROM dcf_implementing_unit {};".format(position_data_filter()))
    form3_datatable=db.select("SELECT * FROM dcf_bdsp_reg {};".format(position_data_filter()))
    form4_datatable=db.select("SELECT * FROM dcf_capacity_building {};".format(position_data_filter()))
    form5_datatable=db.select("SELECT * FROM dcf_matching_grant {};".format(position_data_filter()))
    form6_datatable=db.select("SELECT * FROM dcf_product_development {};".format(position_data_filter()))
    form7_datatable=db.select("SELECT * FROM dcf_trade_promotion {};".format(position_data_filter()))
    form9_datatable=db.select("SELECT * FROM dcf_enablers_activity {};".format(position_data_filter()))
    form10_datatable=db.select("SELECT * FROM dcf_negosyo_center {};".format(position_data_filter()))
    form11_datatable=db.select("SELECT * FROM dcf_access_financing {};".format(position_data_filter()))
    return{
        'form1_datatable':  form1_datatable,
        'form2_datatable':  form2_datatable,
        'form3_datatable':  form3_datatable,
        'form4_datatable':  form4_datatable,
        'form5_datatable':  form5_datatable,
        'form6_datatable':  form6_datatable,
        'form7_datatable':  form7_datatable,
        'form9_datatable':  form9_datatable,
        'form10_datatable':  form10_datatable,
        'form11_datatable':  form11_datatable

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