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


    return{
        'form1_datatable':  form1_datatable,
        'form2_datatable':  form2_datatable
    }


def displayform():
    if(is_on_session()):
        pass
    else:
        return redirect("/login?force_url=1")
        
    USER_INFO = session["USER_DATA"]
    form1_datatable=db.select("SELECT * FROM dcf_prep_review_aprv_status {};".format(position_data_filter()))
    form2_datatable=db.select("SELECT * FROM dcf_implementing_unit {};".format(position_data_filter()))
    return{
        'form1_datatable':  form1_datatable,
        'form2_datatable':  form2_datatable

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
