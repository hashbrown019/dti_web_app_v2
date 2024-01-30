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

    form1_data_jul= db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form1_data_aug = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form1_data_sep = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form1_data_oct = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form1_data_nov =db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form1_data_dec = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form1_data_jan = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form1_thismonth=len(form1_data_jan)
    form1_lastmonth=len(form1_data_dec)
    form1_subperc= form1_thismonth - form1_lastmonth
    try: form1_percentage= (form1_subperc / form1_lastmonth)
    except Exception as e: form1_percentage = 0

    form1_percentages = round(form1_percentage,2)

    form1_data_jul=len(form1_data_jul)
    form1_data_aug=len(form1_data_aug)
    form1_data_sep=len(form1_data_sep)
    form1_data_oct=len(form1_data_oct)
    form1_data_nov=len(form1_data_nov)
    form1_data_dec=len(form1_data_dec)
    form1_data_jan=len(form1_data_jan)


    form2_data_jul= db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form2_data_aug = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form2_data_sep = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form2_data_oct = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form2_data_nov =db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form2_data_dec = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form2_data_jan = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form2_thismonth=len(form2_data_jan)
    form2_lastmonth=len(form2_data_dec)
    form2_subperc= form2_thismonth - form2_lastmonth
    try: form2_percentage= (form2_subperc / form2_lastmonth)
    except Exception as e: form2_percentage = 0

    form2_percentages = round(form2_percentage,2)

    form2_data_jul=len(form2_data_jul)
    form2_data_aug=len(form2_data_aug)
    form2_data_sep=len(form2_data_sep)
    form2_data_oct=len(form2_data_oct)
    form2_data_nov=len(form2_data_nov)
    form2_data_dec=len(form2_data_dec)
    form2_data_jan=len(form2_data_jan)


    form3_data_jul= db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form3_data_aug = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form3_data_sep = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form3_data_oct = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form3_data_nov =db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form3_data_dec = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form3_data_jan = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form3_thismonth=len(form3_data_jan)
    form3_lastmonth=len(form3_data_dec)
    form3_subperc= form3_thismonth - form3_lastmonth
    try: form3_percentage= (form3_subperc / form3_lastmonth)
    except Exception as e: form3_percentage = 0

    form3_percentages = round(form3_percentage,2)

    form3_data_jul=len(form3_data_jul)
    form3_data_aug=len(form3_data_aug)
    form3_data_sep=len(form3_data_sep)
    form3_data_oct=len(form3_data_oct)
    form3_data_nov=len(form3_data_nov)
    form3_data_dec=len(form3_data_dec)
    form3_data_jan=len(form3_data_jan)


    form4_data_jul= db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form4_data_aug = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form4_data_sep = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form4_data_oct = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form4_data_nov =db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form4_data_dec = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form4_data_jan = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form4_thismonth=len(form4_data_jan)
    form4_lastmonth=len(form4_data_dec)
    form4_subperc= form4_thismonth - form4_lastmonth
    try: form4_percentage= (form4_subperc / form4_lastmonth)
    except Exception as e: form4_percentage = 0

    form4_percentages = round(form4_percentage,2)

    form4_data_jul=len(form4_data_jul)
    form4_data_aug=len(form4_data_aug)
    form4_data_sep=len(form4_data_sep)
    form4_data_oct=len(form4_data_oct)
    form4_data_nov=len(form4_data_nov)
    form4_data_dec=len(form4_data_dec)
    form4_data_jan=len(form4_data_jan)


    form5_data_jul= db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form5_data_aug = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form5_data_sep = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form5_data_oct = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form5_data_nov =db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form5_data_dec = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form5_data_jan = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form5_thismonth=len(form5_data_jan)
    form5_lastmonth=len(form5_data_dec)
    form5_subperc= form5_thismonth - form5_lastmonth
    try: form5_percentage= (form5_subperc / form5_lastmonth)
    except Exception as e: form5_percentage = 0

    form5_percentages = round(form5_percentage,2)

    form5_data_jul=len(form5_data_jul)
    form5_data_aug=len(form5_data_aug)
    form5_data_sep=len(form5_data_sep)
    form5_data_oct=len(form5_data_oct)
    form5_data_nov=len(form5_data_nov)
    form5_data_dec=len(form5_data_dec)
    form5_data_jan=len(form5_data_jan)

    form6_data_jul= db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form6_data_aug = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form6_data_sep = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form6_data_oct = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form6_data_nov =db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form6_data_dec = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form6_data_jan = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form6_thismonth=len(form6_data_jan)
    form6_lastmonth=len(form6_data_dec)
    form6_subperc= form6_thismonth - form6_lastmonth
    try: form6_percentage= (form6_subperc / form6_lastmonth)
    except Exception as e: form6_percentage = 0

    form6_percentages = round(form6_percentage,2)

    form6_data_jul=len(form6_data_jul)
    form6_data_aug=len(form6_data_aug)
    form6_data_sep=len(form6_data_sep)
    form6_data_oct=len(form6_data_oct)
    form6_data_nov=len(form6_data_nov)
    form6_data_dec=len(form6_data_dec)
    form6_data_jan=len(form6_data_jan)


    form7_data_jul= db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form7_data_aug = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form7_data_sep = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form7_data_oct = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form7_data_nov =db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form7_data_dec = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form7_data_jan = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form7_thismonth=len(form7_data_jan)
    form7_lastmonth=len(form7_data_dec)
    form7_subperc= form7_thismonth - form7_lastmonth
    try: form7_percentage= (form7_subperc / form7_lastmonth)
    except Exception as e: form7_percentage = 0

    form7_percentages = round(form7_percentage,2)

    form7_data_jul=len(form7_data_jul)
    form7_data_aug=len(form7_data_aug)
    form7_data_sep=len(form7_data_sep)
    form7_data_oct=len(form7_data_oct)
    form7_data_nov=len(form7_data_nov)
    form7_data_dec=len(form7_data_dec)
    form7_data_jan=len(form7_data_jan)


    form9_data_jul= db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form9_data_aug = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form9_data_sep = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form9_data_oct = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form9_data_nov =db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form9_data_dec = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form9_data_jan = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form9_thismonth=len(form9_data_jan)
    form9_lastmonth=len(form9_data_dec)
    form9_subperc= form9_thismonth - form9_lastmonth
    try: form9_percentage= (form9_subperc / form9_lastmonth)
    except Exception as e: form9_percentage = 0

    form9_percentages = round(form9_percentage,2)

    form9_data_jul=len(form9_data_jul)
    form9_data_aug=len(form9_data_aug)
    form9_data_sep=len(form9_data_sep)
    form9_data_oct=len(form9_data_oct)
    form9_data_nov=len(form9_data_nov)
    form9_data_dec=len(form9_data_dec)
    form9_data_jan=len(form9_data_jan)


    form10_data_jul= db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form10_data_aug = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form10_data_sep = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form10_data_oct = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form10_data_nov =db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form10_data_dec = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form10_data_jan = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form10_thismonth=len(form10_data_jan)
    form10_lastmonth=len(form10_data_dec)
    form10_subperc= form10_thismonth - form10_lastmonth
    try: form10_percentage= (form10_subperc / form10_lastmonth)
    except Exception as e: form10_percentage = 0

    form10_percentages = round(form10_percentage,2)

    form10_data_jul=len(form10_data_jul)
    form10_data_aug=len(form10_data_aug)
    form10_data_sep=len(form10_data_sep)
    form10_data_oct=len(form10_data_oct)
    form10_data_nov=len(form10_data_nov)
    form10_data_dec=len(form10_data_dec)
    form10_data_jan=len(form10_data_jan)


    form11_data_jul= db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form11_data_aug = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form11_data_sep = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form11_data_oct = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form11_data_nov =db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form11_data_dec = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form11_data_jan = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))

    form11_thismonth=len(form11_data_jan)
    form11_lastmonth=len(form11_data_dec)
    form11_subperc= form11_thismonth - form11_lastmonth
    try: form11_percentage= (form11_subperc / form11_lastmonth)
    except Exception as e: form11_percentage = 0

    form11_percentages = round(form11_percentage,2)

    form11_data_jul=len(form11_data_jul)
    form11_data_aug=len(form11_data_aug)
    form11_data_sep=len(form11_data_sep)
    form11_data_oct=len(form11_data_oct)
    form11_data_nov=len(form11_data_nov)
    form11_data_dec=len(form11_data_dec)
    form11_data_jan=len(form11_data_jan)





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


    form2status_nonrenewal=db.select("SELECT form_2_remarks_status AS totalnonrenewal FROM dcf_implementing_unit {} AND form_2_remarks_status = 'Non-renewal';".format(position_data_filter()))
    dcf_form2nonrenewal=len(form2status_nonrenewal)
    form2status_cancelled=db.select("SELECT form_2_remarks_status AS totalcancelled FROM dcf_implementing_unit {} AND form_2_remarks_status = 'Cancelled';".format(position_data_filter()))
    dcf_form2cancelled=len(form2status_cancelled)
    form2status_og=db.select("SELECT form_2_remarks_status AS totalog FROM dcf_implementing_unit {} AND form_2_remarks_status = 'On-going';".format(position_data_filter()))
    dcf_form2og=len(form2status_og)
    totalstatus = dcf_form2cancelled+dcf_form2nonrenewal+dcf_form2og



    dcf_form1male=db.select("SELECT SUM(form_1_totalmale) AS total_male FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1maleyouth=db.select("SELECT SUM(form_1_maleyouth) AS total_maleyouth FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1maleip=db.select("SELECT SUM(form_1_maleip) AS total_maleip FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1malepwd=db.select("SELECT SUM(form_1_malepwd) AS total_malepwd FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))


    dcf_form1sextotal=db.select("SELECT SUM(form_1_total_farmerbene) AS total_sex FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form2sextotal=db.select("SELECT  SUM(form_2_male + form_2_female)AS total_sex2 FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    dcf_form3sextotal=db.select("SELECT COUNT(CASE WHEN form_3_sex = 'male' OR form_3_sex = 'female' THEN 1 END) AS total_sex3 FROM dcf_bdsp_reg {}; ".format(position_data_filter()))
    dcf_form4sextotal=db.select("SELECT  SUM(cbb_total_number_per_gender_male + cbb_total_number_per_gender_female)AS total_sex4 FROM dcf_capacity_building {}; ".format(position_data_filter()))



    dcf_form1female=db.select("SELECT SUM(form_1_totalfemale) AS total_female FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1femaleyouth=db.select("SELECT SUM(form_1_femaleyouth) AS total_femaleyouth FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1femaleip=db.select("SELECT SUM(form_1_femaleip) AS total_femaleip FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))
    dcf_form1femalepwd=db.select("SELECT SUM(form_1_femalepwd) AS total_femalepwd FROM dcf_prep_review_aprv_status {}; ".format(position_data_filter()))


    dcf_form2FOmale=db.select("SELECT SUM(form_2_male) AS total_male2 FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    dcf_form2FOfemale=db.select("SELECT SUM(form_2_female) AS total_female2 FROM dcf_implementing_unit {}; ".format(position_data_filter()))

    dcf_form2FOpwd=db.select("SELECT SUM(form_2_pwde) AS total_pwd FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    dcf_form2FOyouth=db.select("SELECT SUM( form_2_youth) AS total_youth FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    dcf_form2FOip=db.select("SELECT SUM(form_2_ip) AS total_ip FROM dcf_implementing_unit {}; ".format(position_data_filter()))
    dcf_form2FOsc=db.select("SELECT SUM(form_2_sc) AS total_sc FROM dcf_implementing_unit {}; ".format(position_data_filter()))

    form3_agri =db.select("SELECT COUNT(id) AS total_agri FROM dcf_bdsp_reg  {} AND form_3_choices LIKE '%Agri-technical%'; ".format(position_data_filter()))
    form3_entrep =db.select("SELECT COUNT(id) AS total_entrep FROM dcf_bdsp_reg  {} AND form_3_choices LIKE '%Entrepreneurial%'; ".format(position_data_filter()))
    form3_extserv =db.select("SELECT COUNT(id) AS total_extserv FROM dcf_bdsp_reg  {} AND form_3_choices LIKE '%Extension Service%'; ".format(position_data_filter()))
    form3_org =db.select("SELECT COUNT(id) AS total_org FROM dcf_bdsp_reg  {} AND form_3_choices LIKE '%Organizational%'; ".format(position_data_filter()))

    form3red=db.select("SELECT COUNT(form_3_philgeps_registered) AS totalred FROM dcf_bdsp_reg {} AND form_3_philgeps_registered = 'RED';".format(position_data_filter()))
    form3plat=db.select("SELECT COUNT(form_3_philgeps_registered) AS totalplat FROM dcf_bdsp_reg {} AND form_3_philgeps_registered = 'PLATINUM';".format(position_data_filter()))
    form3unreg=db.select("SELECT COUNT(form_3_philgeps_registered) AS totalunreg FROM dcf_bdsp_reg {} AND form_3_philgeps_registered = 'UNREGISTERED';".format(position_data_filter()))

    form3orgfirm=db.select("SELECT COUNT(form_3_types_of_bdsp) AS totalorgfirm FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm';".format(position_data_filter()))
    form3indiv=db.select("SELECT COUNT(form_3_types_of_bdsp) AS totalindiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual';".format(position_data_filter()))

    form2status_cancelled=db.select("SELECT form_2_remarks_status AS totalcancelled FROM dcf_implementing_unit {} AND form_2_remarks_status = 'Cancelled';".format(position_data_filter()))
    dcf_form2cancelled=len(form2status_cancelled)
    form2status_og=db.select("SELECT form_2_remarks_status AS totalog FROM dcf_implementing_unit {} AND form_2_remarks_status = 'On-going';".format(position_data_filter()))
    dcf_form2og=len(form2status_og)

    form4beforedip=db.select("SELECT COUNT(cbb_dip_approved_alignment) AS totalbeforedip FROM dcf_capacity_building {} AND cbb_dip_approved_alignment = 'Conducted after DIP approval';".format(position_data_filter()))
    form4afterdip=db.select("SELECT COUNT(cbb_dip_approved_alignment) AS totalafterdip FROM dcf_capacity_building {} AND cbb_dip_approved_alignment = 'Conducted before DIP approval';".format(position_data_filter()))


    dcf_form5male=db.select("SELECT SUM(mgit_total_number_fo_gender_male) AS totalmale5 FROM dcf_matching_grant {}; ".format(position_data_filter()))
    dcf_form5female=db.select("SELECT SUM(mgit_total_number_fo_gender_female) AS totalfemale5 FROM dcf_matching_grant {}; ".format(position_data_filter()))

    dcf_form5pwd=db.select("SELECT SUM(mgit_total_number_fo_sectoral_pwd) AS totalpwd5 FROM dcf_matching_grant {}; ".format(position_data_filter()))
    dcf_form5youth=db.select("SELECT SUM(mgit_total_number_fo_sectoral_youth) AS totalyouth5 FROM dcf_matching_grant {}; ".format(position_data_filter()))
    dcf_form5ip=db.select("SELECT SUM(mgit_total_number_fo_sectoral_IP) AS totalip5 FROM dcf_matching_grant {}; ".format(position_data_filter()))
    dcf_form5sc=db.select("SELECT SUM(mgit_total_number_fo_sectoral_SC) AS totalsc5 FROM dcf_matching_grant {}; ".format(position_data_filter()))


    selectdcf_form3male=db.select("SELECT form_3_sex AS total_male3 FROM dcf_bdsp_reg {} AND form_3_sex = 'male';".format(position_data_filter()))
    selectdcf_form3female=db.select("SELECT form_3_sex AS total_female3 FROM dcf_bdsp_reg {} AND form_3_sex = 'female';".format(position_data_filter()))
    dcf_form3male=len(selectdcf_form3male)
    dcf_form3female=len(selectdcf_form3female)

    dcf_form4female=db.select("SELECT SUM(cbb_female_total) AS total_female4 FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4male=db.select("SELECT SUM(cbb_male_total) AS total_male4 FROM dcf_capacity_building {};".format(position_data_filter()))

    dcf_form4maleip=db.select("SELECT SUM(cbb_male_ip) AS total_male4ip FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4maleyouth=db.select("SELECT SUM(cbb_male_youth) AS total_male4youth FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4malepwd=db.select("SELECT SUM(cbb_male_pwd) AS total_male4pwd FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4malesc=db.select("SELECT SUM(cbb_male_sc) AS total_male4sc FROM dcf_capacity_building {};".format(position_data_filter()))

    dcf_form4femaleip=db.select("SELECT SUM(cbb_female_ip) AS total_female4ip FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4femaleyouth=db.select("SELECT SUM(cbb_female_youth) AS total_female4youth FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4femalepwd=db.select("SELECT SUM(cbb_female_pwd) AS total_female4pwd FROM dcf_capacity_building {};".format(position_data_filter()))
    dcf_form4femalesc=db.select("SELECT SUM(cbb_female_sc) AS total_female4sc FROM dcf_capacity_building {};".format(position_data_filter()))


    dcf_form7msme=db.select("SELECT COUNT(form_7_beneficiary) AS totalmsme7 FROM dcf_trade_promotion {} AND form_7_beneficiary = 'MSME';".format(position_data_filter()))
    dcf_form7fo=db.select("SELECT COUNT(form_7_beneficiary) AS totalfo7 FROM dcf_trade_promotion {} AND form_7_beneficiary = 'FO';".format(position_data_filter()))
    dcf_form7farmer=db.select("SELECT COUNT(form_7_beneficiary) AS totalfarmer7 FROM dcf_trade_promotion {} AND form_7_beneficiary = 'Farmer';".format(position_data_filter()))

    dcf_form7male=db.select("SELECT COUNT(form_7_sex) AS totalmale7 FROM dcf_trade_promotion {} AND form_7_sex = 'Male';".format(position_data_filter()))
    dcf_form7female=db.select("SELECT COUNT(form_7_sex) AS totalfemale7 FROM dcf_trade_promotion {} AND form_7_sex = 'Female';".format(position_data_filter()))

    dcf_form7pwd=db.select("SELECT COUNT(form_7_sector) AS totalpwd7 FROM dcf_trade_promotion {} AND form_7_sector = 'PWD';".format(position_data_filter()))
    dcf_form7youth=db.select("SELECT COUNT(form_7_sector) AS totalyouth7 FROM dcf_trade_promotion {} AND form_7_sector = 'Youth';".format(position_data_filter()))
    dcf_form7ip=db.select("SELECT COUNT(form_7_sector) AS totalip7 FROM dcf_trade_promotion {} AND form_7_sector = 'IP';".format(position_data_filter()))
    dcf_form7sc=db.select("SELECT COUNT(form_7_sector) AS totalsc7 FROM dcf_trade_promotion {} AND form_7_sector = 'SC';".format(position_data_filter()))
    dcf_form7abled=db.select("SELECT COUNT(form_7_sector) AS totalabled7 FROM dcf_trade_promotion {} AND form_7_sector = 'Abled';".format(position_data_filter()))

    dcf_form7cashsales=db.select("SELECT SUM(form_7_cash_sales) AS total_cash7 FROM dcf_trade_promotion {};".format(position_data_filter()))
    dcf_form7bookedsales=db.select("SELECT SUM(form_7_booked_sales) AS total_booked7 FROM dcf_trade_promotion {};".format(position_data_filter()))
    dcf_form7undernego=db.select("SELECT SUM(form_7_under_negotiations) AS total_undernego FROM dcf_trade_promotion {};".format(position_data_filter()))
    dcf_form7total=db.select("SELECT SUM(form_7_total_autosum) AS total_ovrlltotal FROM dcf_trade_promotion {};".format(position_data_filter()))









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





###################FORM7####################################################

    dips_list7 = form7_datatable
    over_all_commodity_count7 = {}
    for index in range(len(dips_list7)):
        DIP7 = dips_list7[index]
        _comm_rule7 = ["cacao","coconut","coffee","pfn"]
        _com7 = DIP7['form_7_commodity']
        if(_com7.lower() not in _comm_rule7):
            _com7 = "Others"
        if(_com7 not in over_all_commodity_count7):
            over_all_commodity_count7[_com7 ] = 0
        over_all_commodity_count7[_com7 ] += 1






###################FORM5####################################################

    dips_list5 = form5_datatable
    over_all_commodity_count5 = {}
    for index in range(len(dips_list5)):
        DIP5 = dips_list5[index]
        _comm_rule5 = ["cacao","coconut","coffee","pfn"]
        _com5 = DIP5['mgit_commodity']
        if(_com5.lower() not in _comm_rule5):
            _com5 = "Others"
        if(_com5 not in over_all_commodity_count5):
            over_all_commodity_count5[_com5 ] = 0
        over_all_commodity_count5[_com5 ] += 1





###########################FORM4##################################################
    dips_list4 = form4_datatable
    over_all_commodity_count4 = {}
    for index in range(len(dips_list4)):
        DIP4 = dips_list4[index]
        _comm_rule4 = ["cacao","coconut","coffee","pfn"]
        _com4 = DIP4['cbb_commodity']
        if(_com4.lower() not in _comm_rule4):
            _com4 = "Others"
        if(_com4 not in over_all_commodity_count4):
            over_all_commodity_count4[_com4 ] = 0
        over_all_commodity_count4[_com4 ] += 1





##################################FORM3#########################################


    dips_list3 = form3_datatable
    typebdsp = {}
    for index in range(len(dips_list3)):
        DIP3 = dips_list3[index]
        _comm_rule3 = ["individual","organization/firm"]
        _com3 = DIP3['form_3_types_of_bdsp']
        if(_com3.lower() not in _comm_rule3):
            _com3 = "Untagged"
        if(_com3 not in typebdsp):
            typebdsp[_com3 ] = 0
        typebdsp[_com3 ] += 1

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
        'dcf_form3sextotal':dcf_form3sextotal,
        'dcf_form4sextotal':dcf_form4sextotal,
        'dcf_form1female':  dcf_form1female,
        'dcf_form1femaleyouth': dcf_form1femaleyouth,
        'dcf_form1femaleip':dcf_form1femaleip,
        'dcf_form1femalepwd':dcf_form1femalepwd,
        'dcf_form2FOmale':  dcf_form2FOmale,
        'dcf_form2FOpwd':  dcf_form2FOpwd,
        'dcf_form2FOyouth':  dcf_form2FOyouth,
        'dcf_form2FOip':  dcf_form2FOip,
        'dcf_form2FOsc':  dcf_form2FOsc,
        'dcf_form2FOfemale':  dcf_form2FOfemale,
        'dcf_form3male':  dcf_form3male,
        'dcf_form3female':  dcf_form3female,
        'dcf_form4male':  dcf_form4male,
        'dcf_form4female':  dcf_form4female,
        'dips_list':  dip_status_group_per_region,
        'dcf_form2nonrenewal': dcf_form2nonrenewal,
        'dcf_form2cancelled': dcf_form2cancelled,
        'dcf_form2og': dcf_form2og,
        'totalstatus': totalstatus,
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
        'over_all_commodity_count4':over_all_commodity_count4,
        'over_all_commodity_count5':over_all_commodity_count5,
        'over_all_commodity_count7':over_all_commodity_count7,
        'typebdsp':typebdsp,
        'form1_data_jul':form1_data_jul,
        'form1_data_aug':form1_data_aug,
        'form1_data_sep':form1_data_sep,
        'form1_data_oct':form1_data_oct,
        'form1_data_nov':form1_data_nov,
        'form1_data_dec':form1_data_dec,
        'form1_data_jan':form1_data_jan,
        'form1_percentages':form1_percentages,
        'form1_thismonth':form1_thismonth,
        'form1_lastmonth':form1_lastmonth,
        'form1_subperc':form1_subperc,
        'form2_data_jul':form2_data_jul,
        'form2_data_aug':form2_data_aug,
        'form2_data_sep':form2_data_sep,
        'form2_data_oct':form2_data_oct,
        'form2_data_nov':form2_data_nov,
        'form2_data_dec':form2_data_dec,
        'form2_data_jan':form2_data_jan,
        'form2_percentages':form2_percentages,
        'form2_thismonth':form2_thismonth,
        'form2_lastmonth':form2_lastmonth,
        'form2_subperc':form2_subperc,
        'form3_data_jul':form3_data_jul,
        'form3_data_aug':form3_data_aug,
        'form3_data_sep':form3_data_sep,
        'form3_data_oct':form3_data_oct,
        'form3_data_nov':form3_data_nov,
        'form3_data_dec':form3_data_dec,
        'form3_data_jan':form3_data_jan,
        'form3_percentages':form3_percentages,
        'form3_thismonth':form3_thismonth,
        'form3_lastmonth':form3_lastmonth,
        'form3_subperc':form3_subperc,
        'form4_data_jul':form4_data_jul,
        'form4_data_aug':form4_data_aug,
        'form4_data_sep':form4_data_sep,
        'form4_data_oct':form4_data_oct,
        'form4_data_nov':form4_data_nov,
        'form4_data_dec':form4_data_dec,
        'form4_data_jan':form4_data_jan,
        'form4_percentages':form4_percentages,
        'form4_thismonth':form4_thismonth,
        'form4_lastmonth':form4_lastmonth,
        'form4_subperc':form4_subperc,
        'form5_data_jul':form5_data_jul,
        'form5_data_aug':form5_data_aug,
        'form5_data_sep':form5_data_sep,
        'form5_data_oct':form5_data_oct,
        'form5_data_nov':form5_data_nov,
        'form5_data_dec':form5_data_dec,
        'form5_data_jan':form5_data_jan,
        'form5_percentages':form5_percentages,
        'form5_thismonth':form5_thismonth,
        'form5_lastmonth':form5_lastmonth,
        'form5_subperc':form5_subperc,
        'form6_data_jul':form6_data_jul,
        'form6_data_aug':form6_data_aug,
        'form6_data_sep':form6_data_sep,
        'form6_data_oct':form6_data_oct,
        'form6_data_nov':form6_data_nov,
        'form6_data_dec':form6_data_dec,
        'form6_data_jan':form6_data_jan,
        'form6_percentages':form6_percentages,
        'form6_thismonth':form6_thismonth,
        'form6_lastmonth':form6_lastmonth,
        'form6_subperc':form6_subperc,
        'form7_data_jul':form7_data_jul,
        'form7_data_aug':form7_data_aug,
        'form7_data_sep':form7_data_sep,
        'form7_data_oct':form7_data_oct,
        'form7_data_nov':form7_data_nov,
        'form7_data_dec':form7_data_dec,
        'form7_data_jan':form7_data_jan,
        'form7_percentages':form7_percentages,
        'form7_thismonth':form7_thismonth,
        'form7_lastmonth':form7_lastmonth,
        'form7_subperc':form7_subperc,
        'form9_data_jul':form9_data_jul,
        'form9_data_aug':form9_data_aug,
        'form9_data_sep':form9_data_sep,
        'form9_data_oct':form9_data_oct,
        'form9_data_nov':form9_data_nov,
        'form9_data_dec':form9_data_dec,
        'form9_data_jan':form9_data_jan,
        'form9_percentages':form9_percentages,
        'form9_thismonth':form9_thismonth,
        'form9_lastmonth':form9_lastmonth,
        'form9_subperc':form9_subperc,
        'form10_data_jul':form10_data_jul,
        'form10_data_aug':form10_data_aug,
        'form10_data_sep':form10_data_sep,
        'form10_data_oct':form10_data_oct,
        'form10_data_nov':form10_data_nov,
        'form10_data_dec':form10_data_dec,
        'form10_data_jan':form10_data_jan,
        'form10_percentages':form10_percentages,
        'form10_thismonth':form10_thismonth,
        'form10_lastmonth':form10_lastmonth,
        'form10_subperc':form10_subperc,
        'form11_data_jul':form11_data_jul,
        'form11_data_aug':form11_data_aug,
        'form11_data_sep':form11_data_sep,
        'form11_data_oct':form11_data_oct,
        'form11_data_nov':form11_data_nov,
        'form11_data_dec':form11_data_dec,
        'form11_data_jan':form11_data_jan,
        'form11_percentages':form11_percentages,
        'form11_thismonth':form11_thismonth,
        'form11_lastmonth':form11_lastmonth,
        'form3_agri':form3_agri,
        'form3_entrep':form3_entrep,
        'form3_extserv':form3_extserv,
        'form3_org':form3_org,
        'form3red':form3red,
        'form3plat':form3plat,
        'form3unreg':form3unreg,
        'form3orgfirm':form3orgfirm,
        'form3indiv':form3indiv,
        'form4beforedip':form4beforedip,
        'form4afterdip':form4afterdip,
        'dcf_form5male':dcf_form5male,
        'dcf_form5female':dcf_form5female,
        'dcf_form5pwd':dcf_form5pwd,
        'dcf_form5youth':dcf_form5youth,
        'dcf_form5ip':dcf_form5ip,
        'dcf_form5sc':dcf_form5sc,
        'dcf_form4maleip':dcf_form4maleip,
        'dcf_form4maleyouth':dcf_form4maleyouth,
        'dcf_form4malepwd':dcf_form4malepwd,
        'dcf_form4malesc':dcf_form4malesc,
        'dcf_form4femaleip':dcf_form4femaleip,
        'dcf_form4femaleyouth':dcf_form4femaleyouth,
        'dcf_form4femalepwd':dcf_form4femalepwd,
        'dcf_form4femalesc':dcf_form4femalesc,
        'dcf_form7msme':dcf_form7msme,
        'dcf_form7fo':dcf_form7fo,
        'dcf_form7farmer':dcf_form7farmer,
        'dcf_form7female':dcf_form7female,
        'dcf_form7male':dcf_form7male,
        'dcf_form7pwd':dcf_form7pwd,
        'dcf_form7youth':dcf_form7youth,
        'dcf_form7ip':dcf_form7ip,
        'dcf_form7sc':dcf_form7sc,
        'dcf_form7abled':dcf_form7abled,
        'dcf_form7cashsales':dcf_form7cashsales,
        'dcf_form7bookedsales':dcf_form7bookedsales,
        'dcf_form7undernego':dcf_form7undernego,
        'dcf_form7total':dcf_form7total

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
