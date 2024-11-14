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
        'form11_datatable':  form11_datatable,
    }


def displayform():
    if(is_on_session()):
        pass
    else:
        return redirect("/login?force_url=1")
        
    USER_INFO = session["USER_DATA"]

    form1_data_sep = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form1_data_oct = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form1_data_nov =db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form1_data_dec = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form1_data_jan = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form1_data_feb = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form1_data_mar = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form1_data_apr = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form1_data_may = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form1_data_june = db.select("SELECT * FROM dcf_prep_review_aprv_status {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form1_thismonth=len(form1_data_june)
    form1_lastmonth=len(form1_data_may)
    form1_subperc= form1_thismonth - form1_lastmonth
    try: form1_percentage= (form1_subperc / form1_lastmonth)
    except Exception as e: form1_percentage = 0

    form1_percentages = round(form1_percentage,2)

    form1_data_sep=len(form1_data_sep)
    form1_data_oct=len(form1_data_oct)
    form1_data_nov=len(form1_data_nov)
    form1_data_dec=len(form1_data_dec)
    form1_data_jan=len(form1_data_jan)
    form1_data_feb=len(form1_data_feb)
    form1_data_mar=len(form1_data_mar)
    form1_data_apr=len(form1_data_apr)
    form1_data_may=len(form1_data_may)
    form1_data_june=len(form1_data_june)






    form2_data_sep = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form2_data_oct = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form2_data_nov =db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE -  INTERVAL 7 MONTH)".format(position_data_filter()))
    form2_data_dec = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form2_data_jan = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form2_data_feb = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form2_data_mar = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form2_data_apr = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form2_data_may = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form2_data_june = db.select("SELECT * FROM dcf_implementing_unit {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form2_thismonth=len(form2_data_june)
    form2_lastmonth=len(form2_data_may)
    form2_subperc= form2_thismonth - form2_lastmonth
    try: form2_percentage= (form2_subperc / form2_lastmonth)
    except Exception as e: form2_percentage = 0

    form2_percentages = round(form2_percentage,2)

    form2_data_sep=len(form2_data_sep)
    form2_data_oct=len(form2_data_oct)
    form2_data_nov=len(form2_data_nov)
    form2_data_dec=len(form2_data_dec)
    form2_data_jan=len(form2_data_jan)
    form2_data_feb=len(form2_data_feb)
    form2_data_mar=len(form2_data_mar)
    form2_data_apr=len(form2_data_apr)
    form2_data_may=len(form2_data_may)
    form2_data_june=len(form2_data_june)







    form3_data_sep = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form3_data_oct = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form3_data_nov = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE -  INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE -INTERVAL 7 MONTH)".format(position_data_filter()))
    form3_data_dec = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form3_data_jan = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form3_data_feb = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form3_data_mar = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form3_data_apr = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form3_data_may = db.select("SELECT * FROM dcf_bdsp_reg {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form3_data_june = db.select("SELECT * FROM dcf_bdsp_reg {}AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form3_thismonth=len(form3_data_june)
    form3_lastmonth=len(form3_data_may)
    form3_subperc= form3_thismonth - form3_lastmonth
    try: form3_percentage= (form3_subperc / form3_lastmonth)
    except Exception as e: form3_percentage = 0

    form3_percentages = round(form3_percentage,2)

    form3_data_sep=len(form3_data_sep)
    form3_data_oct=len(form3_data_oct)
    form3_data_nov=len(form3_data_nov)
    form3_data_dec=len(form3_data_dec)
    form3_data_jan=len(form3_data_jan)
    form3_data_feb=len(form3_data_feb)
    form3_data_mar=len(form3_data_mar)
    form3_data_apr=len(form3_data_apr)
    form3_data_may=len(form3_data_may)
    form3_data_june=len(form3_data_june)







    form4_data_sep = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form4_data_oct = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form4_data_nov = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE -  INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE -INTERVAL 7 MONTH)".format(position_data_filter()))
    form4_data_dec = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form4_data_jan = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form4_data_feb = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form4_data_mar = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form4_data_apr = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form4_data_may = db.select("SELECT * FROM dcf_capacity_building {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form4_data_june = db.select("SELECT * FROM dcf_capacity_building {}AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))




    form4_thismonth=len(form4_data_june)
    form4_lastmonth=len(form4_data_may)
    form4_subperc= form4_thismonth - form4_lastmonth
    try: form4_percentage= (form4_subperc / form4_lastmonth)
    except Exception as e: form4_percentage = 0

    form4_percentages = round(form4_percentage,2)

    form4_data_sep=len(form4_data_sep)
    form4_data_oct=len(form4_data_oct)
    form4_data_nov=len(form4_data_nov)
    form4_data_dec=len(form4_data_dec)
    form4_data_jan=len(form4_data_jan)
    form4_data_feb=len(form4_data_feb)
    form4_data_mar=len(form4_data_mar)
    form4_data_apr=len(form4_data_apr)
    form4_data_may=len(form4_data_may)
    form4_data_june=len(form4_data_june)







    form5_data_sep = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form5_data_oct = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form5_data_nov =db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form5_data_dec = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form5_data_jan = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form5_data_feb = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form5_data_mar = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form5_data_apr = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form5_data_may = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form5_data_june = db.select("SELECT * FROM dcf_matching_grant {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form5_thismonth=len(form5_data_june)
    form5_lastmonth=len(form5_data_may)
    form5_subperc= form5_thismonth - form5_lastmonth
    try: form5_percentage= (form5_subperc / form5_lastmonth)
    except Exception as e: form5_percentage = 0

    form5_percentages = round(form5_percentage,2)

    form5_data_sep=len(form5_data_sep)
    form5_data_oct=len(form5_data_oct)
    form5_data_nov=len(form5_data_nov)
    form5_data_dec=len(form5_data_dec)
    form5_data_jan=len(form5_data_jan)
    form5_data_feb=len(form5_data_feb)
    form5_data_mar=len(form5_data_mar)
    form5_data_apr=len(form5_data_apr)
    form5_data_may=len(form5_data_may)
    form5_data_june=len(form5_data_june)





    form6_data_sep = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form6_data_oct = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form6_data_nov =db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form6_data_dec = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form6_data_jan = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form6_data_feb = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form6_data_mar = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form6_data_apr = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form6_data_may = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form6_data_june = db.select("SELECT * FROM dcf_product_development {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form6_thismonth=len(form6_data_june)
    form6_lastmonth=len(form6_data_may)
    form6_subperc= form6_thismonth - form6_lastmonth
    try: form6_percentage= (form6_subperc / form6_lastmonth)
    except Exception as e: form6_percentage = 0

    form6_percentages = round(form6_percentage,2)

    form6_data_sep=len(form6_data_sep)
    form6_data_oct=len(form6_data_oct)
    form6_data_nov=len(form6_data_nov)
    form6_data_dec=len(form6_data_dec)
    form6_data_jan=len(form6_data_jan)
    form6_data_feb=len(form6_data_feb)
    form6_data_mar=len(form6_data_mar)
    form6_data_apr=len(form6_data_apr)
    form6_data_may=len(form6_data_may)
    form6_data_june=len(form6_data_june)







    form7_data_sep = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form7_data_oct = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form7_data_nov =db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form7_data_dec = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form7_data_jan = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form7_data_feb = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form7_data_mar = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form7_data_apr = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form7_data_may = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form7_data_june = db.select("SELECT * FROM dcf_trade_promotion {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form7_thismonth=len(form7_data_june)
    form7_lastmonth=len(form7_data_may)
    form7_subperc= form7_thismonth - form7_lastmonth
    try: form7_percentage= (form7_subperc / form7_lastmonth)
    except Exception as e: form7_percentage = 0

    form7_percentages = round(form7_percentage,2)

    form7_data_sep=len(form7_data_sep)
    form7_data_oct=len(form7_data_oct)
    form7_data_nov=len(form7_data_nov)
    form7_data_dec=len(form7_data_dec)
    form7_data_jan=len(form7_data_jan)
    form7_data_feb=len(form7_data_feb)
    form7_data_mar=len(form7_data_mar)
    form7_data_apr=len(form7_data_apr)
    form7_data_may=len(form7_data_may)
    form7_data_june=len(form7_data_june)







    form9_data_sep = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form9_data_oct = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form9_data_nov =db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form9_data_dec = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form9_data_jan = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form9_data_feb = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form9_data_mar = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form9_data_apr = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form9_data_may = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form9_data_june = db.select("SELECT * FROM dcf_enablers_activity {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))



    form9_thismonth=len(form9_data_june)
    form9_lastmonth=len(form9_data_may)
    form9_subperc= form9_thismonth - form9_lastmonth
    try: form9_percentage= (form9_subperc / form9_lastmonth)
    except Exception as e: form9_percentage = 0

    form9_percentages = round(form9_percentage,2)

    form9_data_sep=len(form9_data_sep)
    form9_data_oct=len(form9_data_oct)
    form9_data_nov=len(form9_data_nov)
    form9_data_dec=len(form9_data_dec)
    form9_data_jan=len(form9_data_jan)
    form9_data_feb=len(form9_data_feb)
    form9_data_mar=len(form9_data_mar)
    form9_data_apr=len(form9_data_apr)
    form9_data_may=len(form9_data_may)
    form9_data_june=len(form9_data_june)







    form10_data_sep = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form10_data_oct = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form10_data_nov =db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form10_data_dec = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form10_data_jan = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form10_data_feb = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form10_data_mar = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form10_data_apr = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form10_data_may =  db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form10_data_june = db.select("SELECT * FROM dcf_negosyo_center {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))




    form10_thismonth=len(form10_data_june)
    form10_lastmonth=len(form10_data_may)
    form10_subperc= form10_thismonth - form10_lastmonth
    try: form10_percentage= (form10_subperc / form10_lastmonth)
    except Exception as e: form10_percentage = 0

    form10_percentages = round(form10_percentage,2)

    form10_data_sep=len(form10_data_sep)
    form10_data_oct=len(form10_data_oct)
    form10_data_nov=len(form10_data_nov)
    form10_data_dec=len(form10_data_dec)
    form10_data_jan=len(form10_data_jan)
    form10_data_feb=len(form10_data_feb)
    form10_data_mar=len(form10_data_mar)
    form10_data_apr=len(form10_data_apr)
    form10_data_may=len(form10_data_may)
    form10_data_june=len(form10_data_june)







    form11_data_sep = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 9 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 9 MONTH)".format(position_data_filter()))
    form11_data_oct = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 8 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 8 MONTH)".format(position_data_filter()))
    form11_data_nov =db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 7 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 7 MONTH)".format(position_data_filter()))
    form11_data_dec = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 6 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 6 MONTH)".format(position_data_filter()))
    form11_data_jan = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 5 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 5 MONTH)".format(position_data_filter()))
    form11_data_feb = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 4 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 4 MONTH)".format(position_data_filter()))
    form11_data_mar = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 3 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 3 MONTH)".format(position_data_filter()))
    form11_data_apr = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 2 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 2 MONTH)".format(position_data_filter()))
    form11_data_may = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE - INTERVAL 1 MONTH) AND MONTH(date_created) = MONTH(CURRENT_DATE - INTERVAL 1 MONTH)".format(position_data_filter()))
    form11_data_june = db.select("SELECT * FROM dcf_access_financing {} AND YEAR(date_created) = YEAR(CURRENT_DATE) AND MONTH(date_created) = MONTH(CURRENT_DATE)".format(position_data_filter()))




    form11_thismonth=len(form11_data_june)
    form11_lastmonth=len(form11_data_may)
    form11_subperc= form11_thismonth - form11_lastmonth
    try: form11_percentage= (form11_subperc / form11_lastmonth)
    except Exception as e: form11_percentage = 0

    form11_percentages = round(form11_percentage,2)

    form11_data_sep=len(form11_data_sep)
    form11_data_oct=len(form11_data_oct)
    form11_data_nov=len(form11_data_nov)
    form11_data_dec=len(form11_data_dec)
    form11_data_jan=len(form11_data_jan)
    form11_data_feb=len(form11_data_feb)
    form11_data_mar=len(form11_data_mar)
    form11_data_apr=len(form11_data_apr)
    form11_data_may=len(form11_data_may)
    form11_data_june=len(form11_data_june)







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
    form1_datatabledip =db.select("SELECT id,form_1_rcus,form_1_name_dip FROM dcf_prep_review_aprv_status".format(position_data_filter()))


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

    dcf_form1sextotalappr=db.select("SELECT SUM(form_1_total_farmerbene) AS total_sexappr FROM dcf_prep_review_aprv_status {} AND `form_1_date_of_ifad_no_inssuance` !='' ; ".format(position_data_filter()))



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

    dcf_form9capb=db.select("SELECT COUNT(form_9_type_of_training) AS totalcapbuild9 FROM dcf_enablers_activity {} AND form_9_type_of_training = 'Capbuild';".format(position_data_filter()))
    dcf_form9meetings=db.select("SELECT COUNT(form_9_type_of_training) AS totalmeetings9 FROM dcf_enablers_activity {} AND form_9_type_of_training = 'Meetings';".format(position_data_filter()))
    dcf_form9policy=db.select("SELECT COUNT(form_9_type_of_training) AS totalpolicy9 FROM dcf_enablers_activity {} AND form_9_type_of_training = 'Policy issuances';".format(position_data_filter()))
    dcf_form9budg=db.select("SELECT SUM(form_9_rapid_actual_budget) as totalact9 FROM dcf_enablers_activity {};".format(position_data_filter()))

    dcf_form10female=db.select("SELECT SUM(form_10_sex_female) AS total_female10 FROM dcf_negosyo_center {};".format(position_data_filter()))
    dcf_form10male=db.select("SELECT SUM(form_10_sex_male) AS total_male10 FROM dcf_negosyo_center {};".format(position_data_filter()))



    dcf_form11ip=db.select("SELECT SUM(form_11_ip) AS total_ip11 FROM dcf_access_financing {};".format(position_data_filter()))
    dcf_form11youth=db.select("SELECT SUM(form_11_youth) AS total_youth11 FROM dcf_access_financing {};".format(position_data_filter()))
    dcf_form11pwd=db.select("SELECT SUM(form_11_pwd) AS total_pwd11 FROM dcf_access_financing {};".format(position_data_filter()))
    dcf_form11sc=db.select("SELECT SUM(form_11_sc) AS total_sc11 FROM dcf_access_financing {};".format(position_data_filter()))

    dcf_form11female=db.select("SELECT SUM(form_11_female) AS total_female11 FROM dcf_access_financing {};".format(position_data_filter()))
    dcf_form11male=db.select("SELECT SUM(form_11_male) AS total_male11 FROM dcf_access_financing {};".format(position_data_filter()))

    dcf_form6actualbudget=db.select("SELECT SUM(form_6_rapid_actual_budget) AS total_actbug6 FROM dcf_product_development {};".format(position_data_filter()))



    



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

######################FORM11#################################################

    dips_list11 = form11_datatable
    over_all_commodity_count11 = {}
    for index in range(len(dips_list11)):
        DIP11 = dips_list11[index]
        _comm_rule11 = ["cacao","coconut","coffee","pfn"]
        _com11 = DIP11['form_11_industry_cluster']
        if(_com11.lower() not in _comm_rule11):
            _com11 = "Others"
        if(_com11 not in over_all_commodity_count11):
            over_all_commodity_count11[_com11 ] = 0
        over_all_commodity_count11[_com11 ] += 1



####################FORM10##################################################

    dips_list10 = form10_datatable
    over_all_commodity_count10 = {}
    for index in range(len(dips_list10)):
        DIP11 = dips_list10[index]
        _comm_rule10 = ["cacao","coconut","coffee","pfn"]
        _com10 = DIP11['form_10_commodity']
        if(_com10.lower() not in _comm_rule10):
            _com10 = "Others"
        if(_com10 not in over_all_commodity_count10):
            over_all_commodity_count10[_com10 ] = 0
        over_all_commodity_count10[_com10 ] += 1





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
    dips_listdcf1 = form1_datatabledip
    
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

        if(DIP["form_1_date_of_ifad_no_inssuance"] != ""):
            dip_status_group_per_region[DIP['form_1_rcus']]["total"] += 1
            over_all["over_all_total"] +=1
            dip_status_group_per_region[DIP['form_1_rcus']]["approve"]+= 1
            over_all["approve"] += 1
            
            if(DIP['form_1_commodity'] not in commodities_per_status_per_region[DIP['form_1_rcus']]["approve"]):
                commodities_per_status_per_region[DIP['form_1_rcus']]["approve"][DIP['form_1_commodity']] = 0
            commodities_per_status_per_region[DIP['form_1_rcus']]["approve"][DIP['form_1_commodity']] += 1
            commodities_per_status_per_region[DIP['form_1_rcus']]["total"][DIP['form_1_commodity']] += 1
            # dip_status_group_per_region[DIP['form_1_rcus']]["approve"].append(DIP)

        elif( DIP["form_1_finalized_approved"] != "" or DIP["form_1_date_of_parallel_review"] != "" or DIP["form_1_date_of_submission"] != "" or DIP["form_1_date_of_rtwg"] != "" or DIP["form_1_date_of_npco_cursory"] != ""):
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




  
#######################################################################################################################
###NEW DATA FROM INTERNS###############################################################################################
#######################################################################################################################

    dcf7_TFP=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfp7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Provincial';".format(position_data_filter()))
    dcf7_TFR=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfr7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Regional';".format(position_data_filter()))
    dcf7_TFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfn7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - National';".format(position_data_filter()))
    dcf7_TFI=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfi7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - International';".format(position_data_filter()))
    dcf7_TSMPR=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tsmpr7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Mission Province and Region';".format(position_data_filter()))
    dcf7_TSMN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tsmn7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Mission National';".format(position_data_filter()))
    dcf7_TSMI=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tsmi7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Mission International';".format(position_data_filter()))
    dcf7_BMPR=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS bmpr7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching Povince and Region';".format(position_data_filter()))
    dcf7_BMN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS bmn7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching National';".format(position_data_filter()))
    dcf7_BMI=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS bmi7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching International';".format(position_data_filter()))

    dcf10_FO=db.select("SELECT COUNT(form_10_type_of_beneficiary) AS FO10 FROM dcf_negosyo_center  {} AND form_10_type_of_beneficiary LIKE '%FO%' OR `form_10_type_of_beneficiary` LIKE '%farmer Organization%';".format(position_data_filter()))
    dcf10_MSME=db.select("SELECT COUNT(form_10_type_of_beneficiary) AS msme10 FROM dcf_negosyo_center  {} AND form_10_type_of_beneficiary LIKE '%MSME%';".format(position_data_filter()))
    dcf_form10_male=db.select("SELECT SUM(form_10_sex_male) as totalmale10 FROM dcf_negosyo_center {} AND form_10_type_of_beneficiary NOT LIKE '%FO%' AND `form_10_type_of_beneficiary` NOT LIKE '%farmer Organization%' AND `form_10_type_of_beneficiary` NOT LIKE '%MSME%';".format(position_data_filter()))
    dcf_form10_female=db.select("SELECT SUM(form_10_sex_female) as totalfemale10 FROM dcf_negosyo_center {} AND form_10_type_of_beneficiary NOT LIKE '%FO%' AND `form_10_type_of_beneficiary` NOT LIKE '%farmer Organization%' AND `form_10_type_of_beneficiary` NOT LIKE '%MSME%';".format(position_data_filter()))

    dcf4_TOT=db.select("SELECT COUNT(cbb_types_of_training) AS tot4 FROM dcf_capacity_building {} AND cbb_types_of_training LIKE '%MSME-%' OR cbb_types_of_training LIKE '%FO-%' OR cbb_types_of_training LIKE '%Individual Farmer-%';".format(position_data_filter()))

    dcf10_NOT=db.select("SELECT COUNT(form_10_type_of_beneficiary) AS NOT10 FROM dcf_negosyo_center {} AND form_10_type_of_beneficiary NOT LIKE '%FO%' AND `form_10_type_of_beneficiary` NOT LIKE '%farmer Organization%' AND `form_10_type_of_beneficiary` NOT LIKE '%MSME%';".format(position_data_filter()))

    dcf7_TA=db.select("SELECT SUM(form_7_total_autosum) AS ta7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion LIKE '%trade fair%';".format(position_data_filter()))
    

    dcf7_TFPCOFFEE=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfpcoffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Provincial' AND `form_7_commodity`='coffee';".format(position_data_filter()))
    dcf7_TFPCACAO=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfpcacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Provincial' AND `form_7_commodity`='cacao';".format(position_data_filter()))
    dcf7_TFPCOCONUT=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfpcoconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Provincial' AND `form_7_commodity`='coconut';".format(position_data_filter()))
    dcf7_TFPPFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfppfn7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Provincial' AND `form_7_commodity`='pfn';".format(position_data_filter()))

################################################################

    dcf7_TFRCOFFEE=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfrcoffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Regional' AND `form_7_commodity`='coffee';".format(position_data_filter()))
    dcf7_TFRCACAO=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfrcacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Regional' AND `form_7_commodity`='cacao';".format(position_data_filter()))
    dcf7_TFRCOCONUT=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfrcoconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Regional' AND `form_7_commodity`='coconut';".format(position_data_filter()))
    dcf7_TFRPFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) AS tfrpfn7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - Regional' AND `form_7_commodity`='pfn';".format(position_data_filter()))

################################################################

    dcf7_tfn_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfn_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - National' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_tfn_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfn_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - National' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_tfn_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfn_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - National' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_tfn_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfn_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - National' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))

#################################################################

    dcf7_tfi_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfi_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - International' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_tfi_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfi_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - International' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_tfi_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfi_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - International' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_tfi_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tfi_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade Fair - International' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))

#################################################################

    dcf7_tmpr_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmpr_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions Province and Region' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_tmpr_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmpr_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions Province and Region' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_tmpr_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmpr_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions Province and Region' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_tmpr_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmpr_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions Province and Region' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))

#################################################################

    dcf7_tmn_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmn_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions National' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_tmn_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmn_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions National' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_tmn_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmn_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions National' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_tmn_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmn_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions National' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))

#################################################################

    dcf7_tmi_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmi_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions International' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_tmi_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmi_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions International' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_tmi_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmi_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions International' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_tmi_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as tmi_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Trade/Selling Missions International' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))

#################################################################

    dcf7_bmpr_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmpr_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching Province and Region' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_bmpr_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmpr_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching Province and Region' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_bmpr_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmpr_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching Province and Region' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_bmpr_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmpr_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching Province and Region' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
#################################################################

    dcf7_bmn_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmn_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching National' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_bmn_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmn_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching National' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_bmn_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmn_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching National' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_bmn_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmn_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching National' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))
#################################################################

    dcf7_bmi_coffee=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmi_coffee7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching International' AND `form_7_commodity` = 'coffee';".format(position_data_filter()))
    dcf7_bmi_coconut=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmi_coconut7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching International' AND `form_7_commodity` = 'coconut';".format(position_data_filter()))
    dcf7_bmi_cacao=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmi_cacao7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching International' AND `form_7_commodity` = 'cacao';".format(position_data_filter()))
    dcf7_bmi_PFN=db.select("SELECT COUNT(form_7_type_of_trade_promotion) as bmi_PFN7 FROM dcf_trade_promotion {} AND form_7_type_of_trade_promotion = 'Business Matching International' AND `form_7_commodity` = 'PFN';".format(position_data_filter()))

####FORM 3########################################################
    dcf3_region8_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrep8 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Vlll - Eastern Visayas' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_region8_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agri8 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Vlll - Eastern Visayas' AND `form_3_choices` LIKE '%Agri-technical%';".format(position_data_filter()))
    dcf3_region8_es=db.select("SELECT COUNT(form_3_choices) as dcf3_es8 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Vlll - Eastern Visayas' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_region8_org=db.select("SELECT COUNT(form_3_choices) as dcf3_org8 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Vlll - Eastern Visayas' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_region9_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrep9 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region lX - Zamboanga Peninsula' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_region9_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agri9 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region lX - Zamboanga Peninsula' AND `form_3_choices` LIKE '%Agri-technical%';".format(position_data_filter()))
    dcf3_region9_es=db.select("SELECT COUNT(form_3_choices) as dcf3_es9 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region lX - Zamboanga Peninsula' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_region9_org=db.select("SELECT COUNT(form_3_choices) as dcf3_org9 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region lX - Zamboanga Peninsula' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_region10_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrep10 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region X - Northern Mindanao' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_region10_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agri10 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region X - Northern Mindanao' AND `form_3_choices` LIKE '%Agri-technical%';".format(position_data_filter()))
    dcf3_region10_es=db.select("SELECT COUNT(form_3_choices) as dcf3_es10 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region X - Northern Mindanao' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_region10_org=db.select("SELECT COUNT(form_3_choices) as dcf3_org10 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region X - Northern Mindanao' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_region11_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrep11 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xl - Davao Region' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_region11_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agri11 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xl - Davao Region' AND `form_3_choices` LIKE '%Agri-technical%';".format(position_data_filter()))
    dcf3_region11_es=db.select("SELECT COUNT(form_3_choices) as dcf3_es11 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xl - Davao Region' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_region11_org=db.select("SELECT COUNT(form_3_choices) as dcf3_org11 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xl - Davao Region' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_region12_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrep12 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xll - SOCCSKSARGEN' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_region12_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agri12 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xll - SOCCSKSARGEN' AND `form_3_choices` LIKE '%Agri-technical%';".format(position_data_filter()))
    dcf3_region12_es=db.select("SELECT COUNT(form_3_choices) as dcf3_es12 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xll - SOCCSKSARGEN' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_region12_org=db.select("SELECT COUNT(form_3_choices) as dcf3_org12 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xll - SOCCSKSARGEN' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_region13_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrep13 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xlll - Caraga' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_region13_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agri13 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xlll - Caraga' AND `form_3_choices` LIKE '%Agri-Technical%';".format(position_data_filter()))
    dcf3_region13_es=db.select("SELECT COUNT(form_3_choices) as dcf3_es13 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xlll - Caraga' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_region13_org=db.select("SELECT COUNT(form_3_choices) as dcf3_org13 FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'Region Xlll - Caraga' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_regionB_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrepB FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'BARMM - Bangsamoro Autonomous Region in Muslim Mindanao' AND `form_3_choices` LIKE '%Entrepreneurial%';".format(position_data_filter()))
    dcf3_regionB_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agriB FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'BARMM - Bangsamoro Autonomous Region in Muslim Mindanao' AND `form_3_choices` LIKE '%Agri-technical%';".format(position_data_filter()))
    dcf3_regionB_es=db.select("SELECT COUNT(form_3_choices) as dcf3_esB FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'BARMM - Bangsamoro Autonomous Region in Muslim Mindanao' AND `form_3_choices` LIKE '%Extension Service%';".format(position_data_filter()))
    dcf3_regionB_org=db.select("SELECT COUNT(form_3_choices) as dcf3_orgB FROM dcf_bdsp_reg {} AND form_3_preferred_region = 'BARMM - Bangsamoro Autonomous Region in Muslim Mindanao' AND `form_3_choices` LIKE '%Organizational%';".format(position_data_filter()))

    dcf3_total_entrep=db.select("SELECT COUNT(form_3_choices) as dcf3_entrepT FROM dcf_bdsp_reg {} AND `form_3_choices` LIKE '%Entrepreneurial%' AND form_3_preferred_region !='' OR ' ' ;".format(position_data_filter()))
    dcf3_total_agri=db.select("SELECT COUNT(form_3_choices) as dcf3_agriT FROM dcf_bdsp_reg {} AND `form_3_choices` LIKE '%Agri-technical%' AND form_3_preferred_region !='' OR ' ' ;".format(position_data_filter()))
    dcf3_total_es=db.select("SELECT COUNT(form_3_choices) as dcf3_esT FROM dcf_bdsp_reg {} AND `form_3_choices` LIKE '%Extension Service%' AND form_3_preferred_region !='' OR ' ' ;".format(position_data_filter()))
    dcf3_total_org=db.select("SELECT COUNT(form_3_choices) as dcf3_orgT FROM dcf_bdsp_reg {} AND `form_3_choices` LIKE '%Organizational%' AND form_3_preferred_region !='' OR ' ' ;".format(position_data_filter()))


    dcf_form1maleip_appr=db.select("SELECT SUM(form_1_maleip) AS total_maleip_appr FROM dcf_prep_review_aprv_status {}AND `form_1_date_of_ifad_no_inssuance` !='' ;".format(position_data_filter()))
    dcf_form1femaleip_appr=db.select("SELECT SUM(form_1_femaleip) AS total_femaleip_appr FROM dcf_prep_review_aprv_status {}AND `form_1_date_of_ifad_no_inssuance` !='' ;".format(position_data_filter()))

    dcf_form1maleyouth_appr=db.select("SELECT SUM(form_1_maleyouth) AS total_maleyouth_appr FROM dcf_prep_review_aprv_status {}AND `form_1_date_of_ifad_no_inssuance` !='' ;".format(position_data_filter()))
    dcf_form1femaleyouth_appr=db.select("SELECT SUM(form_1_femaleyouth) AS total_femaleyouth_appr FROM dcf_prep_review_aprv_status {}AND `form_1_date_of_ifad_no_inssuance` !='' ;".format(position_data_filter()))

    dcf_form1male_appr=db.select("SELECT SUM(form_1_totalmale) AS total_male_appr FROM dcf_prep_review_aprv_status {}AND `form_1_date_of_ifad_no_inssuance` !='' ;".format(position_data_filter()))
    dcf_form1female_appr=db.select("SELECT SUM(form_1_totalfemale) AS total_female_appr FROM dcf_prep_review_aprv_status {}AND `form_1_date_of_ifad_no_inssuance` !='' ;" .format(position_data_filter()))


    #NEW DATA APRIL30 (FRANZ)
    dcf1_COFFEE_8=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_8_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='8';".format(position_data_filter()))
    dcf1_CACAO_8=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_8_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='8';".format(position_data_filter()))
    dcf1_COCONUT_8=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_8_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='8';".format(position_data_filter()))
    dcf1_PFN_8=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_8_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='8';".format(position_data_filter()))

    dcf1_COFFEE_9=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_9_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='9';".format(position_data_filter()))
    dcf1_CACAO_9=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_9_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='9';".format(position_data_filter()))
    dcf1_COCONUT_9=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_9_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='9';".format(position_data_filter()))
    dcf1_PFN_9=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_9_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='9';".format(position_data_filter()))
    
    dcf1_COFFEE_10=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_10_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='10';".format(position_data_filter()))
    dcf1_CACAO_10=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_10_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='10';".format(position_data_filter()))
    dcf1_COCONUT_10=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_10_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='10';".format(position_data_filter()))
    dcf1_PFN_10=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_10_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='10';".format(position_data_filter()))
    
    dcf1_COFFEE_11=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_11_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='11';".format(position_data_filter()))
    dcf1_CACAO_11=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_11_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='11';".format(position_data_filter()))
    dcf1_COCONUT_11=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_11_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='11';".format(position_data_filter()))
    dcf1_PFN_11=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_11_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='11';".format(position_data_filter()))

    dcf1_COFFEE_12=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_12_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='12';".format(position_data_filter()))
    dcf1_CACAO_12=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_12_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='12';".format(position_data_filter()))
    dcf1_COCONUT_12=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_12_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='12';".format(position_data_filter()))
    dcf1_PFN_12=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_12_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='12';".format(position_data_filter()))

    dcf1_COFFEE_13=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_13_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='13';".format(position_data_filter()))
    dcf1_CACAO_13=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_13_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='13';".format(position_data_filter()))
    dcf1_COCONUT_13=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_13_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='13';".format(position_data_filter()))
    dcf1_PFN_13=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_13_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='13';".format(position_data_filter()))

    dcf1_COFFEE_BARMM=db.select("SELECT COUNT(`form_1_commodity`) AS coffee_BARMM_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee' AND `form_1_rcus`='BARMM';".format(position_data_filter()))
    dcf1_CACAO_BARMM=db.select("SELECT COUNT(`form_1_commodity`) AS cacao_BARMM_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao' AND `form_1_rcus`='BARMM';".format(position_data_filter()))
    dcf1_COCONUT_BARMM=db.select("SELECT COUNT(`form_1_commodity`) AS coconut_BARMM_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut' AND `form_1_rcus`='BARMM';".format(position_data_filter()))
    dcf1_PFN_BARMM=db.select("SELECT COUNT(`form_1_commodity`) AS pfn_BARMM_1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn' AND `form_1_rcus`='BARMM';".format(position_data_filter()))


    #NEW DATA MAY2 (ANDY)
    dcf_form2_rcu8=db.select("SELECT COUNT(form_2_rcus) AS form2_rcu8 FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%8%' ;".format(position_data_filter()))
    dcf_form2_rcu9=db.select("SELECT COUNT(form_2_rcus) AS form2_rcu9 FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%9%' ;".format(position_data_filter()))
    dcf_form2_rcu10=db.select("SELECT COUNT(form_2_rcus) AS form2_rcu10 FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%10%' ;".format(position_data_filter()))
    dcf_form2_rcu11=db.select("SELECT COUNT(form_2_rcus) AS form2_rcu11 FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%11%' ;".format(position_data_filter()))
    dcf_form2_rcu12=db.select("SELECT COUNT(form_2_rcus) AS form2_rcu12 FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%12%' ;".format(position_data_filter()))
    dcf_form2_rcu13=db.select("SELECT COUNT(form_2_rcus) AS form2_rcu13 FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%13%' ;".format(position_data_filter()))
    dcf_form2_rcuBARMM=db.select("SELECT COUNT(form_2_rcus) AS form2_rcuBARMM FROM dcf_implementing_unit {} AND `form_2_rcus` LIKE '%BARMM%' ;".format(position_data_filter()))


    dcf_form2_rcu8_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcu8_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%8%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='' ;".format(position_data_filter()))
    dcf_form2_rcu9_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcu9_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%9%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='';".format(position_data_filter()))
    dcf_form2_rcu10_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcu10_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%10%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='';".format(position_data_filter()))
    dcf_form2_rcu11_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcu11_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%11%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='';".format(position_data_filter()))
    dcf_form2_rcu12_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcu12_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%12%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='';".format(position_data_filter()))
    dcf_form2_rcu13_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcu13_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%13%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='';".format(position_data_filter()))
    dcf_form2_rcuBARMM_nom=db.select("SELECT COUNT(DISTINCT form_2_name_owner_manager) AS form2_rcuBARMM_nom FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%BARMM%' AND `form_2_name_owner_manager` != '' AND form_2_partner_fo_engaged ='';".format(position_data_filter()))

    #NEW DATA MAY3(FRANZ)
    dcf1_COFFEE_FO=db.select("SELECT SUM(form_1_totalcooperatives + form_1_totalassociations) AS coffee_fo FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))
    dcf1_CACAO_FO=db.select("SELECT SUM(form_1_totalcooperatives + form_1_totalassociations) AS cacao_fo FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))
    dcf1_COCONUT_FO=db.select("SELECT SUM(form_1_totalcooperatives + form_1_totalassociations) AS coconut_fo FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))
    dcf1_PFN_FO=db.select("SELECT SUM(form_1_totalcooperatives + form_1_totalassociations) AS pfn_fo FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))

    #NEW DATA MAY6(ANDY)
    dcf_form2_rcu8_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcu8_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%8%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))
    dcf_form2_rcu9_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcu9_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%9%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))
    dcf_form2_rcu10_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcu10_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%10%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))
    dcf_form2_rcu11_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcu11_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%11%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))
    dcf_form2_rcu12_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcu12_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%12%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))
    dcf_form2_rcu13_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcu13_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%13%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))
    dcf_form2_rcuBARMM_fo=db.select("SELECT COUNT(DISTINCT form_2_partner_fo_engaged) AS form2_rcuBARMM_fo FROM dcf_implementing_unit {} AND form_2_rcus LIKE '%BARMM%' AND `form_2_partner_fo_engaged` !='' AND `form_2_name_owner_manager` = '' ;".format(position_data_filter()))

    dcf_form2_nom_cacao=db.select("SELECT COUNT(form_2_partner_fo_engaged) AS form2nom_cacao FROM dcf_implementing_unit {} AND form_2_commodity LIKE '%Cacao%' AND form_2_name_owner_manager ='' AND form_2_partner_fo_engaged !=''; ".format(position_data_filter()))
    dcf_form2_nom_coffee=db.select("SELECT COUNT(form_2_partner_fo_engaged) AS form2nom_coffee FROM dcf_implementing_unit {} AND form_2_commodity LIKE '%Coffee%' AND form_2_name_owner_manager ='' AND form_2_partner_fo_engaged !=''; ".format(position_data_filter()))
    dcf_form2_nom_coconut=db.select("SELECT COUNT(form_2_partner_fo_engaged) AS form2nom_coconut FROM dcf_implementing_unit {} AND form_2_commodity LIKE '%Coconut%' AND form_2_name_owner_manager ='' AND form_2_partner_fo_engaged !=''; ".format(position_data_filter()))
    dcf_form2_nom_PFN=db.select("SELECT COUNT(form_2_partner_fo_engaged) AS form2nom_PFN FROM dcf_implementing_unit {} AND form_2_commodity LIKE '%PFN%' AND form_2_name_owner_manager ='' AND form_2_partner_fo_engaged !=''; ".format(position_data_filter()))

    #NEW DATA MAY 6(FRANZ)
    dcf2_CPAs=db.select("SELECT COUNT(`form_2_date_renewed`) AS cpas_2 FROM dcf_implementing_unit {} AND form_2_date_renewed !='';".format(position_data_filter()))

    dcf2_COFFEE=db.select("SELECT COUNT(`form_2_name_owner_manager` ) AS coffee_2 FROM dcf_implementing_unit {} AND `form_2_commodity` ='coffee' AND form_2_partner_fo_engaged ='' AND form_2_name_owner_manager !='';".format(position_data_filter()))
    dcf2_CACAO=db.select("SELECT COUNT(`form_2_name_owner_manager` ) AS cacao_2 FROM dcf_implementing_unit {} AND `form_2_commodity` ='cacao' AND form_2_partner_fo_engaged ='' AND form_2_name_owner_manager !='';".format(position_data_filter()))
    dcf2_COCONUT=db.select("SELECT COUNT(`form_2_name_owner_manager` ) AS coconut_2 FROM dcf_implementing_unit {} AND `form_2_commodity` ='coconut' AND form_2_partner_fo_engaged ='' AND form_2_name_owner_manager !='';".format(position_data_filter()))
    dcf2_PFN=db.select("SELECT COUNT(`form_2_name_owner_manager` ) AS pfn_2 FROM dcf_implementing_unit {} AND `form_2_commodity` ='pfn' AND form_2_partner_fo_engaged ='' AND form_2_name_owner_manager !='';".format(position_data_filter()))

    #NEW DATA MAY 9(FRANZ)
    dcf2_CPAs_FOs=db.select("SELECT COUNT(DISTINCT `form_2_name_owner_manager`) AS cpasfos_2 FROM dcf_implementing_unit {} AND `form_2_partner_fo_engaged` !='';".format(position_data_filter()))
    dcf2_FOs_CPAs=db.select("SELECT COUNT(DISTINCT `form_2_partner_fo_engaged`) AS foscpas_2 FROM dcf_implementing_unit {} AND `form_2_name_owner_manager` !='';".format(position_data_filter()))
    dcf2_FO_MEMBERS=db.select("SELECT SUM(`form_2_total_number_fo`) AS fomember_2 FROM dcf_implementing_unit;".format(position_data_filter()))
    
    dcf2_RCU8_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcu8_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='8';".format(position_data_filter()))
    dcf2_RCU9_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcu9_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='9';".format(position_data_filter()))
    dcf2_RCU10_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcu10_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='10';".format(position_data_filter()))
    dcf2_RCU11_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcu11_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='11';".format(position_data_filter()))
    dcf2_RCU12_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcu12_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='12';".format(position_data_filter()))
    dcf2_RCU13_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcu13_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='13';".format(position_data_filter()))
    dcf2_RCUBARMM_FO=db.select("SELECT SUM(`form_2_total_number_fo`) AS rcubarmm_fo2 FROM dcf_implementing_unit {} AND `form_2_rcus`='barmm';".format(position_data_filter()))
    ######################################################################################################################
    dcf3_RCU8_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu8_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Region Vlll - Eastern Visayas';".format(position_data_filter()))
    dcf3_RCU9_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu9_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Region IX - Zamboanga Peninsula';".format(position_data_filter()))
    dcf3_RCU10_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu10_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Region X - Northern Mindanao';".format(position_data_filter()))
    dcf3_RCU11_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu11_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Region Xl - Davao Region';".format(position_data_filter()))
    dcf3_RCU12_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu12_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Region Xll - SOCCSKSARGEN';".format(position_data_filter()))
    dcf3_RCU13_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu13_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Region Xlll - Caraga';".format(position_data_filter()))
    dcf3_BARMM_ORG=db.select("SELECT COUNT(form_3_types_of_bdsp) AS barmm_org FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Organization/Firm' AND `form_3_preferred_region` = 'Barmm - Bangsamoro Autonomous Region in Muslim Mindanao';".format(position_data_filter()))

    dcf3_RCU8_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu8_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Region Vlll - Eastern Visayas';".format(position_data_filter()))
    dcf3_RCU9_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu9_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Region IX - Zamboanga Peninsula';".format(position_data_filter()))
    dcf3_RCU10_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu10_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Region X - Northern Mindanao';".format(position_data_filter()))
    dcf3_RCU11_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu11_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Region Xl - Davao Region';".format(position_data_filter()))
    dcf3_RCU12_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu12_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Region Xll - SOCCSKSARGEN';".format(position_data_filter()))
    dcf3_RCU13_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS rcu13_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Region Xlll - Caraga';".format(position_data_filter()))
    dcf3_BARMM_INDIV=db.select("SELECT COUNT(form_3_types_of_bdsp) AS barmm_indiv FROM dcf_bdsp_reg {} AND form_3_types_of_bdsp = 'Individual' AND `form_3_preferred_region` = 'Barmm - Bangsamoro Autonomous Region in Muslim Mindanao';".format(position_data_filter()))

    #NEW DATA MAY(10 FRANZ)
    dcf_MALEIP_CACAO_APPR=db.select("SELECT SUM(form_1_maleip) AS maleip_cacao1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))
    dcf_MALEYOUTH_CACAO_APPR=db.select("SELECT SUM(form_1_maleyouth) AS maleyouth_cacao1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))
    dcf_TOTALMALE_CACAO_APPR=db.select("SELECT SUM(form_1_totalmale) AS totalmale_cacao1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))

    dcf_FEMALEIP_CACAO_APPR=db.select("SELECT SUM(form_1_femaleip) AS femaleip_cacao1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))
    dcf_FEMALEYOUTH_CACAO_APPR=db.select("SELECT SUM(form_1_femaleyouth) AS femaleyouth_cacao1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))
    dcf_TOTALFEMALE_CACAO_APPR=db.select("SELECT SUM(form_1_totalfemale) AS totalfemale_cacao1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='cacao';".format(position_data_filter()))

    dcf_MALEIP_COFFEE_APPR=db.select("SELECT SUM(form_1_maleip) AS maleip_coffee1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))
    dcf_MALEYOUTH_COFFEE_APPR=db.select("SELECT SUM(form_1_maleyouth) AS maleyouth_coffee1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))
    dcf_TOTALMALE_COFFEE_APPR=db.select("SELECT SUM(form_1_totalmale) AS totalmale_coffee1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))

    dcf_FEMALEIP_COFFEE_APPR=db.select("SELECT SUM(form_1_femaleip) AS femaleip_coffee1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))
    dcf_FEMALEYOUTH_COFFEE_APPR=db.select("SELECT SUM(form_1_femaleyouth) AS femaleyouth_coffee1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))
    dcf_TOTALFEMALE_COFFEE_APPR=db.select("SELECT SUM(form_1_totalfemale) AS totalfemale_coffee1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coffee';".format(position_data_filter()))

    dcf_MALEIP_COCONUT_APPR=db.select("SELECT SUM(form_1_maleip) AS maleip_coconut1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))
    dcf_MALEYOUTH_COCONUT_APPR=db.select("SELECT SUM(form_1_maleyouth) AS maleyouth_coconut1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))
    dcf_TOTALMALE_COCONUT_APPR=db.select("SELECT SUM(form_1_totalmale) AS totalmale_coconut1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))

    dcf_FEMALEIP_COCONUT_APPR=db.select("SELECT SUM(form_1_femaleip) AS femaleip_coconut1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))
    dcf_FEMALEYOUTH_COCONUT_APPR=db.select("SELECT SUM(form_1_femaleyouth) AS femaleyouth_coconut1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))
    dcf_TOTALFEMALE_COCONUT_APPR=db.select("SELECT SUM(form_1_totalfemale) AS totalfemale_coconut1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='coconut';".format(position_data_filter()))

    dcf_MALEIP_PFN_APPR=db.select("SELECT SUM(form_1_maleip) AS maleip_pfn1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))
    dcf_MALEYOUTH_PFN_APPR=db.select("SELECT SUM(form_1_maleyouth) AS maleyouth_pfn1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))
    dcf_TOTALMALE_PFN_APPR=db.select("SELECT SUM(form_1_totalmale) AS totalmale_pfn1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))

    dcf_FEMALEIP_PFN_APPR=db.select("SELECT SUM(form_1_femaleip) AS femaleip_pfn1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))
    dcf_FEMALEYOUTH_PFN_APPR=db.select("SELECT SUM(form_1_femaleyouth) AS femaleyouth_pfn1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))
    dcf_TOTALFEMALE_PFN_APPR=db.select("SELECT SUM(form_1_totalfemale) AS totalfemale_pfn1 FROM dcf_prep_review_aprv_status {} AND form_1_date_of_ifad_no_inssuance !='' AND `form_1_commodity`='pfn';".format(position_data_filter()))

##############################################################################################################

    dcf1_TSHF_8_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_8_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_TSHF_9_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_9_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_TSHF_10_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_10_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_TSHF_11_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_11_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_TSHF_12_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_12_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_TSHF_13_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_13_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_TSHF_BARMM_APPR=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_barmm_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    
    dcf1_TSHF_8_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_8_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_TSHF_9_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_9_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_for_development !='' ;".format(position_data_filter()))
    dcf1_TSHF_10_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_10_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_TSHF_11_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_11_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_TSHF_12_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_12_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_for_development !='' ;".format(position_data_filter()))
    dcf1_TSHF_13_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_13_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_for_development !='' ;".format(position_data_filter()))
    dcf1_TSHF_BARMM_ONGOING=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_barmm_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_for_development !='';".format(position_data_filter()))
    
    dcf1_TSHF_8_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_8_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    dcf1_TSHF_9_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_9_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    dcf1_TSHF_10_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_10_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    dcf1_TSHF_11_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_11_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    dcf1_TSHF_12_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_12_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    dcf1_TSHF_13_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_13_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    dcf1_TSHF_BARMM_PIPELINE=db.select("SELECT COALESCE(SUM(`form_1_totalmale` + `form_1_totalfemale`), 0) AS tshf_barmm_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_for_development ='' AND ('form_1_finalized_approved' IS NOT NULL OR 'form_1_date_of_parallel_review' IS NOT NULL OR 'form_1_date_of_submission' IS NOT NULL OR 'form_1_date_of_rtwg' IS NOT NULL OR 'form_1_date_of_npco_cursory' IS NOT NULL);".format(position_data_filter()))
    
###################################################################### 

    dcf1_MALE_8_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_8_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_MALE_9_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_9_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_MALE_10_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_10_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_MALE_11_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_11_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_MALE_12_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_12_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_MALE_13_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_13_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_MALE_BARMM_APPR=db.select("SELECT SUM(`form_1_totalmale`) AS male_barmm_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))

    dcf1_MALE_8_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_8_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_MALE_9_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_9_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_MALE_10_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_10_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_MALE_11_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_11_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_MALE_12_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_12_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_MALE_13_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_13_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_MALE_BARMM_ONGOING=db.select("SELECT SUM(`form_1_totalmale`) AS male_barmm_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_for_development !='';".format(position_data_filter()))
    
    dcf1_MALE_8_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_8_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_MALE_9_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_9_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_MALE_10_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_10_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_MALE_11_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_11_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_MALE_12_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_12_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_MALE_13_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_13_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_MALE_BARMM_PIPELINE=db.select("SELECT SUM(`form_1_totalmale`) AS male_barmm_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))

########################################################################

    dcf1_FEMALE_8_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_8_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_FEMALE_9_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_9_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_FEMALE_10_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_10_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_FEMALE_11_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_11_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_FEMALE_12_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_12_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_FEMALE_13_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_13_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_FEMALE_BARMM_APPR=db.select("SELECT SUM(`form_1_totalfemale`) AS female_barmm_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))

    dcf1_FEMALE_8_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_8_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_FEMALE_9_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_9_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_FEMALE_10_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_10_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_FEMALE_11_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_11_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_FEMALE_12_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_12_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_FEMALE_13_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_13_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_FEMALE_BARMM_ONGOING=db.select("SELECT SUM(`form_1_totalfemale`) AS female_barmm_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_for_development !='';".format(position_data_filter()))
    
    dcf1_FEMALE_8_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_8_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_FEMALE_9_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_9_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_FEMALE_10_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_10_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_FEMALE_11_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_11_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_FEMALE_12_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_12_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_FEMALE_13_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_13_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_FEMALE_BARMM_PIPELINE=db.select("SELECT SUM(`form_1_totalfemale`) AS female_barmm_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))

##########################################################################

    dcf1_YOUTH_8_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_8_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_YOUTH_9_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_9_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_YOUTH_10_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_10_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_YOUTH_11_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_11_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_YOUTH_12_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_12_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_YOUTH_13_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_13_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_YOUTH_BARMM_APPR=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_barmm_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))

    dcf1_YOUTH_8_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_8_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_YOUTH_9_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_9_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_YOUTH_10_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_10_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_YOUTH_11_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_11_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_YOUTH_12_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_12_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_YOUTH_13_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_13_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_YOUTH_BARMM_ONGOING=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_barmm_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_for_development !='';".format(position_data_filter()))
    
    dcf1_YOUTH_8_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_8_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_YOUTH_9_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_9_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_YOUTH_10_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_10_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_YOUTH_11_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_11_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_YOUTH_12_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_12_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_YOUTH_13_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_13_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_YOUTH_BARMM_PIPELINE=db.select("SELECT SUM(`form_1_totalyouth`) AS youth_barmm_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))

###########################################################################

    dcf1_IP_8_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_8_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_IP_9_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_9_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_IP_10_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_10_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_IP_11_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_11_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_IP_12_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_12_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_IP_13_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_13_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))
    dcf1_IP_BARMM_APPR=db.select("SELECT SUM(`form_1_totalip`) AS ip_barmm_appr1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_date_of_ifad_no_inssuance !='';".format(position_data_filter()))

    dcf1_IP_8_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_8_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_IP_9_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_9_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_IP_10_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_10_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_IP_11_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_11_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_IP_12_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_12_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_IP_13_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_13_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND form_1_for_development !='';".format(position_data_filter()))
    dcf1_IP_BARMM_ONGOING=db.select("SELECT SUM(`form_1_totalip`) AS ip_barmm_ongoing1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND form_1_for_development !='';".format(position_data_filter()))
    
    dcf1_IP_8_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_8_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='8' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_IP_9_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_9_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='9' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_IP_10_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_10_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='10' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_IP_11_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_11_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='11' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_IP_12_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_12_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='12' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_IP_13_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_13_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='13' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))
    dcf1_IP_BARMM_PIPELINE=db.select("SELECT SUM(`form_1_totalip`) AS ip_barmm_pipeline1 FROM `dcf_prep_review_aprv_status` {} AND `form_1_rcus`='BARMM' AND 'form_1_finalized_approved' !='' OR 'form_1_date_of_parallel_review' !='' OR 'form_1_date_of_submission' !='' OR 'form_1_date_of_rtwg' !='' OR 'form_1_date_of_npco_cursory' !='';".format(position_data_filter()))


    dcf4_GESIFO=db.select("SELECT COUNT(cbb_types_of_training) AS gesifo FROM `dcf_capacity_building` {} AND `cbb_types_of_training`='FO-GESI';".format(position_data_filter()))
    dcf4_GESImsme=db.select("SELECT COUNT(cbb_types_of_training) AS gesimsme FROM `dcf_capacity_building` {} AND `cbb_types_of_training`='MSME-GESI';".format(position_data_filter()))
    dcf4_GESIif=db.select("SELECT COUNT(cbb_types_of_training) AS gesiif FROM `dcf_capacity_building` {} AND `cbb_types_of_training`='Individual Farmer-GESI';".format(position_data_filter()))



    dcf1_IP_apprfm=db.select("SELECT SUM(form_1_maleip + form_1_femaleip) AS total_IP_appr FROM dcf_prep_review_aprv_status  {} AND form_1_date_of_ifad_no_inssuance !='' AND form_1_commodity='coconut';".format(position_data_filter()))
    dcf1_youth_apprfm=db.select("SELECT SUM(form_1_maleyouth + form_1_femaleyouth) AS total_youth_appr FROM dcf_prep_review_aprv_status  {} AND form_1_date_of_ifad_no_inssuance !='' AND form_1_commodity='coconut';".format(position_data_filter()))

    dcf1_IP_apprfmcoffee=db.select("SELECT SUM(form_1_maleip + form_1_femaleip) AS total_IP_apprcoffee FROM dcf_prep_review_aprv_status  {} AND form_1_date_of_ifad_no_inssuance !='' AND form_1_commodity='coffee';".format(position_data_filter()))
    dcf1_youth_apprfmcoffee=db.select("SELECT SUM(form_1_maleyouth + form_1_femaleyouth) AS total_youth_apprcoffee FROM dcf_prep_review_aprv_status  {} AND form_1_date_of_ifad_no_inssuance !='' AND form_1_commodity='coffee';".format(position_data_filter()))

    dcf4_FOOEC=db.select("SELECT COUNT(cbb_types_of_training) AS FOOEC FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Organization Entrepreneurial Competency';".format(position_data_filter()))
    dcf4_FOGOV=db.select("SELECT COUNT(cbb_types_of_training) AS FOGOV FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Governance';".format(position_data_filter()))
    dcf4_FOOM=db.select("SELECT COUNT(cbb_types_of_training) AS FOOM FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Organizational Management';".format(position_data_filter()))
    dcf4_FOOP=db.select("SELECT COUNT(cbb_types_of_training) AS FOOP FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Operations';".format(position_data_filter()))
    dcf4_FOTPD=db.select("SELECT COUNT(cbb_types_of_training) AS FOTPD FROM dcf_capacity_building {} AND cbb_types_of_training LIKE '%FO-Technology and Product Development%';".format(position_data_filter()))
    dcf4_FOIMM=db.select("SELECT COUNT(cbb_types_of_training) AS FOIMM FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Institutional Marketing Management';".format(position_data_filter()))
    dcf4_FOHRM=db.select("SELECT COUNT(cbb_types_of_training) AS FOHRM FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Human Resource Management';".format(position_data_filter()))
    dcf4_FOFM=db.select("SELECT COUNT(cbb_types_of_training) AS FOFM FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Financial Management';".format(position_data_filter()))
    dcf4_FONLB=db.select("SELECT COUNT(cbb_types_of_training) AS FONLB FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Networking and Linkage-Building (External Relation; Business Membership Organization)';".format(position_data_filter()))
    dcf4_FOGESI=db.select("SELECT COUNT(cbb_types_of_training) AS FOGESI FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-GESI';".format(position_data_filter()))
    dcf4_FOSEC=db.select("SELECT COUNT(cbb_types_of_training) AS FOSEC FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Social Environment & Climate';".format(position_data_filter()))
    dcf4_FOMNR=db.select("SELECT COUNT(cbb_types_of_training) AS FOMNR FROM dcf_capacity_building {} AND cbb_types_of_training = 'FO-Managing Natural Resources';".format(position_data_filter()))

    dcf4_MSMEEC=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEEC FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Entrepreneurial Competency';".format(position_data_filter()))
    dcf4_MSMEOP=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEOP FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Operations';".format(position_data_filter()))
    dcf4_MSMEM=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEM FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Management';".format(position_data_filter()))
    dcf4_MSMETPD=db.select("SELECT COUNT(cbb_types_of_training) AS MSMETPD FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Technology and Product Development';".format(position_data_filter()))
    dcf4_MSMEMM=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEMM FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Marketing Management';".format(position_data_filter()))
    dcf4_MSMEHRM=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEHRM FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Human Resource Management';".format(position_data_filter()))
    dcf4_MSMEFM=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEFM FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Financial Management';".format(position_data_filter()))
    dcf4_MSMENLB=db.select("SELECT COUNT(cbb_types_of_training) AS MSMENLB FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Networking and Linkage-Building (External Relation; Business Membership Organization)';".format(position_data_filter()))
    dcf4_MSMEGESI=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEGESI FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-GESI';".format(position_data_filter()))
    dcf4_MSMESEC=db.select("SELECT COUNT(cbb_types_of_training) AS MSMESEC FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Social Environment & Climate';".format(position_data_filter()))
    dcf4_MSMEMNR=db.select("SELECT COUNT(cbb_types_of_training) AS MSMEMNR FROM dcf_capacity_building {} AND cbb_types_of_training = 'MSME-Managing Natural Resources';".format(position_data_filter()))

    dcf4_IFMNR=db.select("SELECT COUNT(cbb_types_of_training) AS IFMNR FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-Managing Natural Resources';".format(position_data_filter()))
    dcf4_IFMF=db.select("SELECT COUNT(cbb_types_of_training) AS IFMF FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-Managing Finances';".format(position_data_filter()))
    dcf4_IFM=db.select("SELECT COUNT(cbb_types_of_training) AS IFM FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-Marketing';".format(position_data_filter()))
    dcf4_IFI=db.select("SELECT COUNT(cbb_types_of_training) AS IFI FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-Innovation';".format(position_data_filter()))
    dcf4_IFT=db.select("SELECT COUNT(cbb_types_of_training) AS IFT FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-Teamwork';".format(position_data_filter()))
    dcf4_IFGESI=db.select("SELECT COUNT(cbb_types_of_training) AS IFGESI FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-GESI';".format(position_data_filter()))
    dcf4_IFSEC=db.select("SELECT COUNT(cbb_types_of_training) AS IFSEC FROM dcf_capacity_building {} AND cbb_types_of_training = 'Individual Farmer-Social Environment & Climate';".format(position_data_filter()))



    return {
        'dcf4_FOOEC':dcf4_FOOEC,
        'dcf4_FOGOV':dcf4_FOGOV,
        'dcf4_FOOM':dcf4_FOOM,
        'dcf4_FOOP':dcf4_FOOP,
        'dcf4_FOTPD':dcf4_FOTPD,
        'dcf4_FOIMM':dcf4_FOIMM,
        'dcf4_FOHRM':dcf4_FOHRM,
        'dcf4_FOFM':dcf4_FOFM,
        'dcf4_FONLB':dcf4_FONLB,
        'dcf4_FOGESI':dcf4_FOGESI,
        'dcf4_FOSEC':dcf4_FOSEC,
        'dcf4_FOMNR':dcf4_FOMNR,

        'dcf4_MSMEEC':dcf4_MSMEEC,
        'dcf4_MSMEOP':dcf4_MSMEOP,
        'dcf4_MSMEM':dcf4_MSMEM,
        'dcf4_MSMETPD':dcf4_MSMETPD,
        'dcf4_MSMEMM':dcf4_MSMEMM,
        'dcf4_MSMEHRM':dcf4_MSMEHRM,
        'dcf4_MSMEFM':dcf4_MSMEFM,
        'dcf4_MSMENLB':dcf4_MSMENLB,
        'dcf4_MSMEGESI':dcf4_MSMEGESI,
        'dcf4_MSMESEC':dcf4_MSMESEC,
        'dcf4_MSMEMNR':dcf4_MSMEMNR,

        'dcf4_IFMNR':dcf4_IFMNR,
        'dcf4_IFMF':dcf4_IFMF,
        'dcf4_IFM':dcf4_IFM,
        'dcf4_IFI':dcf4_IFI,
        'dcf4_IFT':dcf4_IFT,
        'dcf4_IFGESI':dcf4_IFGESI,
        'dcf4_IFSEC':dcf4_IFSEC,


        'dcf4_GESIFO':dcf4_GESIFO,
        'dcf1_IP_apprfmcoffee':dcf1_IP_apprfmcoffee,
        'dcf1_youth_apprfmcoffee':dcf1_youth_apprfmcoffee,
        'dcf_form1sextotalappr':dcf_form1sextotalappr,
        'dcf4_GESImsme':dcf4_GESImsme,
        'dcf4_GESIif':dcf4_GESIif,
        'dcf1_IP_apprfm':dcf1_IP_apprfm,
        'dcf1_youth_apprfm':dcf1_youth_apprfm,
        'dcf1_IP_8_APPR':dcf1_IP_8_APPR,
        'dcf1_IP_9_APPR':dcf1_IP_9_APPR,
        'dcf1_IP_10_APPR':dcf1_IP_10_APPR,
        'dcf1_IP_11_APPR':dcf1_IP_11_APPR,
        'dcf1_IP_12_APPR':dcf1_IP_12_APPR,
        'dcf1_IP_13_APPR':dcf1_IP_13_APPR,
        'dcf1_IP_BARMM_APPR':dcf1_IP_BARMM_APPR,

        'dcf1_IP_8_ONGOING':dcf1_IP_8_ONGOING,
        'dcf1_IP_9_ONGOING':dcf1_IP_9_ONGOING,
        'dcf1_IP_10_ONGOING':dcf1_IP_10_ONGOING,
        'dcf1_IP_11_ONGOING':dcf1_IP_11_ONGOING,
        'dcf1_IP_12_ONGOING':dcf1_IP_12_ONGOING,
        'dcf1_IP_13_ONGOING':dcf1_IP_13_ONGOING,
        'dcf1_IP_BARMM_ONGOING':dcf1_IP_BARMM_ONGOING,

        'dcf1_IP_8_PIPELINE':dcf1_IP_8_PIPELINE,
        'dcf1_IP_9_PIPELINE':dcf1_IP_9_PIPELINE,
        'dcf1_IP_10_PIPELINE':dcf1_IP_10_PIPELINE,
        'dcf1_IP_11_PIPELINE':dcf1_IP_11_PIPELINE,
        'dcf1_IP_12_PIPELINE':dcf1_IP_12_PIPELINE,
        'dcf1_IP_13_PIPELINE':dcf1_IP_13_PIPELINE,
        'dcf1_IP_BARMM_PIPELINE':dcf1_IP_BARMM_PIPELINE,
        'dcf1_YOUTH_8_APPR':dcf1_YOUTH_8_APPR,
        'dcf1_YOUTH_9_APPR':dcf1_YOUTH_9_APPR,
        'dcf1_YOUTH_10_APPR':dcf1_YOUTH_10_APPR,
        'dcf1_YOUTH_11_APPR':dcf1_YOUTH_11_APPR,
        'dcf1_YOUTH_12_APPR':dcf1_YOUTH_12_APPR,
        'dcf1_YOUTH_13_APPR':dcf1_YOUTH_13_APPR,
        'dcf1_YOUTH_BARMM_APPR':dcf1_YOUTH_BARMM_APPR,

        'dcf1_YOUTH_8_ONGOING':dcf1_YOUTH_8_ONGOING,
        'dcf1_YOUTH_9_ONGOING':dcf1_YOUTH_9_ONGOING,
        'dcf1_YOUTH_10_ONGOING':dcf1_YOUTH_10_ONGOING,
        'dcf1_YOUTH_11_ONGOING':dcf1_YOUTH_11_ONGOING,
        'dcf1_YOUTH_12_ONGOING':dcf1_YOUTH_12_ONGOING,
        'dcf1_YOUTH_13_ONGOING':dcf1_YOUTH_13_ONGOING,
        'dcf1_YOUTH_BARMM_ONGOING':dcf1_YOUTH_BARMM_ONGOING,

        'dcf1_YOUTH_8_PIPELINE':dcf1_YOUTH_8_PIPELINE,
        'dcf1_YOUTH_9_PIPELINE':dcf1_YOUTH_9_PIPELINE,
        'dcf1_YOUTH_10_PIPELINE':dcf1_YOUTH_10_PIPELINE,
        'dcf1_YOUTH_11_PIPELINE':dcf1_YOUTH_11_PIPELINE,
        'dcf1_YOUTH_12_PIPELINE':dcf1_YOUTH_12_PIPELINE,
        'dcf1_YOUTH_13_PIPELINE':dcf1_YOUTH_13_PIPELINE,
        'dcf1_YOUTH_BARMM_PIPELINE':dcf1_YOUTH_BARMM_PIPELINE,
        'dcf1_FEMALE_8_APPR':dcf1_FEMALE_8_APPR,
        'dcf1_FEMALE_9_APPR':dcf1_FEMALE_9_APPR,
        'dcf1_FEMALE_10_APPR':dcf1_FEMALE_10_APPR,
        'dcf1_FEMALE_11_APPR':dcf1_FEMALE_11_APPR,
        'dcf1_FEMALE_12_APPR':dcf1_FEMALE_12_APPR,
        'dcf1_FEMALE_13_APPR':dcf1_FEMALE_13_APPR,
        'dcf1_FEMALE_BARMM_APPR':dcf1_FEMALE_BARMM_APPR,

        'dcf1_FEMALE_8_ONGOING':dcf1_FEMALE_8_ONGOING,
        'dcf1_FEMALE_9_ONGOING':dcf1_FEMALE_9_ONGOING,
        'dcf1_FEMALE_10_ONGOING':dcf1_FEMALE_10_ONGOING,
        'dcf1_FEMALE_11_ONGOING':dcf1_FEMALE_11_ONGOING,
        'dcf1_FEMALE_12_ONGOING':dcf1_FEMALE_12_ONGOING,
        'dcf1_FEMALE_13_ONGOING':dcf1_FEMALE_13_ONGOING,
        'dcf1_FEMALE_BARMM_ONGOING':dcf1_FEMALE_BARMM_ONGOING,

        'dcf1_FEMALE_8_PIPELINE':dcf1_FEMALE_8_PIPELINE,
        'dcf1_FEMALE_9_PIPELINE':dcf1_FEMALE_9_PIPELINE,
        'dcf1_FEMALE_10_PIPELINE':dcf1_FEMALE_10_PIPELINE,
        'dcf1_FEMALE_11_PIPELINE':dcf1_FEMALE_11_PIPELINE,
        'dcf1_FEMALE_12_PIPELINE':dcf1_FEMALE_12_PIPELINE,
        'dcf1_FEMALE_13_PIPELINE':dcf1_FEMALE_13_PIPELINE,
        'dcf1_FEMALE_BARMM_PIPELINE':dcf1_FEMALE_BARMM_PIPELINE,
        'dcf1_MALE_8_APPR':dcf1_MALE_8_APPR,
        'dcf1_MALE_9_APPR':dcf1_MALE_9_APPR,
        'dcf1_MALE_10_APPR':dcf1_MALE_10_APPR,
        'dcf1_MALE_11_APPR':dcf1_MALE_11_APPR,
        'dcf1_MALE_12_APPR':dcf1_MALE_12_APPR,
        'dcf1_MALE_13_APPR':dcf1_MALE_13_APPR,
        'dcf1_MALE_BARMM_APPR':dcf1_MALE_BARMM_APPR,

        'dcf1_MALE_8_ONGOING':dcf1_MALE_8_ONGOING,
        'dcf1_MALE_9_ONGOING':dcf1_MALE_9_ONGOING,
        'dcf1_MALE_10_ONGOING':dcf1_MALE_10_ONGOING,
        'dcf1_MALE_11_ONGOING':dcf1_MALE_11_ONGOING,
        'dcf1_MALE_12_ONGOING':dcf1_MALE_12_ONGOING,
        'dcf1_MALE_13_ONGOING':dcf1_MALE_13_ONGOING,
        'dcf1_MALE_BARMM_ONGOING':dcf1_MALE_BARMM_ONGOING,

        'dcf1_MALE_8_PIPELINE':dcf1_MALE_8_PIPELINE,
        'dcf1_MALE_9_PIPELINE':dcf1_MALE_9_PIPELINE,
        'dcf1_MALE_10_PIPELINE':dcf1_MALE_10_PIPELINE,
        'dcf1_MALE_11_PIPELINE':dcf1_MALE_11_PIPELINE,
        'dcf1_MALE_12_PIPELINE':dcf1_MALE_12_PIPELINE,
        'dcf1_MALE_13_PIPELINE':dcf1_MALE_13_PIPELINE,
        'dcf1_MALE_BARMM_PIPELINE':dcf1_MALE_BARMM_PIPELINE,
        'dcf1_TSHF_8_APPR':dcf1_TSHF_8_APPR,
        'dcf1_TSHF_9_APPR':dcf1_TSHF_9_APPR,
        'dcf1_TSHF_10_APPR':dcf1_TSHF_10_APPR,
        'dcf1_TSHF_11_APPR':dcf1_TSHF_11_APPR,
        'dcf1_TSHF_12_APPR':dcf1_TSHF_12_APPR,
        'dcf1_TSHF_13_APPR':dcf1_TSHF_13_APPR,
        'dcf1_TSHF_BARMM_APPR':dcf1_TSHF_BARMM_APPR,

        'dcf1_TSHF_8_ONGOING':dcf1_TSHF_8_ONGOING,
        'dcf1_TSHF_9_ONGOING':dcf1_TSHF_9_ONGOING,
        'dcf1_TSHF_10_ONGOING':dcf1_TSHF_10_ONGOING,
        'dcf1_TSHF_11_ONGOING':dcf1_TSHF_11_ONGOING,
        'dcf1_TSHF_12_ONGOING':dcf1_TSHF_12_ONGOING,
        'dcf1_TSHF_13_ONGOING':dcf1_TSHF_13_ONGOING,
        'dcf1_TSHF_BARMM_ONGOING':dcf1_TSHF_BARMM_ONGOING,

        'dcf1_TSHF_8_PIPELINE':dcf1_TSHF_8_PIPELINE,
        'dcf1_TSHF_9_PIPELINE':dcf1_TSHF_9_PIPELINE,
        'dcf1_TSHF_10_PIPELINE':dcf1_TSHF_10_PIPELINE,
        'dcf1_TSHF_11_PIPELINE':dcf1_TSHF_11_PIPELINE,
        'dcf1_TSHF_12_PIPELINE':dcf1_TSHF_12_PIPELINE,
        'dcf1_TSHF_13_PIPELINE':dcf1_TSHF_13_PIPELINE,
        'dcf1_TSHF_BARMM_PIPELINE':dcf1_TSHF_BARMM_PIPELINE,
        #NEW DATA MAY(10 FRANZ)
        'dcf_MALEIP_CACAO_ APPR':dcf_MALEIP_CACAO_APPR,
        'dcf_MALEYOUTH_CACAO_APPR':dcf_MALEYOUTH_CACAO_APPR,
        'dcf_TOTALMALE_CACAO_APPR':dcf_TOTALMALE_CACAO_APPR,
        'dcf_FEMALEIP_CACAO_APPR':dcf_FEMALEIP_CACAO_APPR,
        'dcf_FEMALEYOUTH_CACAO_APPR':dcf_FEMALEYOUTH_CACAO_APPR,
        'dcf_TOTALFEMALE_CACAO_APPR':dcf_TOTALFEMALE_CACAO_APPR,
        
        'dcf_MALEIP_COFFEE_APPR':dcf_MALEIP_COFFEE_APPR,
        'dcf_MALEYOUTH_COFFEE_APPR':dcf_MALEYOUTH_COFFEE_APPR,
        'dcf_TOTALMALE_COFFEE_APPR':dcf_TOTALMALE_COFFEE_APPR,
        'dcf_FEMALEIP_COFFEE_APPR':dcf_FEMALEIP_COFFEE_APPR,
        'dcf_FEMALEYOUTH_COFFEE_APPR':dcf_FEMALEYOUTH_COFFEE_APPR,
        'dcf_TOTALFEMALE_COFFEE_APPR':dcf_TOTALFEMALE_COFFEE_APPR,

        'dcf_MALEIP_COCONUT_APPR':dcf_MALEIP_COCONUT_APPR,
        'dcf_MALEYOUTH_COCONUT_APPR':dcf_MALEYOUTH_COCONUT_APPR,
        'dcf_TOTALMALE_COCONUT_APPR':dcf_TOTALMALE_COCONUT_APPR,
        'dcf_FEMALEIP_COCONUT_APPR':dcf_FEMALEIP_COCONUT_APPR,
        'dcf_FEMALEYOUTH_COCONUT_APPR':dcf_FEMALEYOUTH_COCONUT_APPR,
        'dcf_TOTALFEMALE_COCONUT_APPR':dcf_TOTALFEMALE_COCONUT_APPR,

        'dcf_MALEIP_PFN_APPR':dcf_MALEIP_PFN_APPR,
        'dcf_MALEYOUTH_PFN_APPR':dcf_MALEYOUTH_PFN_APPR,
        'dcf_TOTALMALE_PFN_APPR':dcf_TOTALMALE_PFN_APPR,
        'dcf_FEMALEIP_PFN_APPR':dcf_FEMALEIP_PFN_APPR,
        'dcf_FEMALEYOUTH_PFN_APPR':dcf_FEMALEYOUTH_PFN_APPR,
        'dcf_TOTALFEMALE_PFN_APPR':dcf_TOTALFEMALE_PFN_APPR,

        #NEW DATA MAY 9(FRANZ)
        'dcf3_RCU8_ORG':dcf3_RCU8_ORG,
        'dcf3_RCU9_ORG':dcf3_RCU9_ORG,
        'dcf3_RCU10_ORG':dcf3_RCU10_ORG,
        'dcf3_RCU11_ORG':dcf3_RCU11_ORG,
        'dcf3_RCU12_ORG':dcf3_RCU12_ORG,
        'dcf3_RCU13_ORG':dcf3_RCU13_ORG,
        'dcf3_BARMM_ORG':dcf3_BARMM_ORG,

        'dcf3_RCU8_INDIV':dcf3_RCU8_INDIV,
        'dcf3_RCU9_INDIV':dcf3_RCU9_INDIV,
        'dcf3_RCU10_INDIV':dcf3_RCU10_INDIV,
        'dcf3_RCU11_INDIV':dcf3_RCU11_INDIV,
        'dcf3_RCU12_INDIV':dcf3_RCU12_INDIV,
        'dcf3_RCU13_INDIV':dcf3_RCU13_INDIV,
        'dcf3_BARMM_INDIV':dcf3_BARMM_INDIV,
    #############################################
        'dcf2_CPAs_FOs':dcf2_CPAs_FOs,
        'dcf2_FOs_CPAs':dcf2_FOs_CPAs,
        'dcf2_FO_MEMBERS':dcf2_FO_MEMBERS,

        'dcf2_RCU8_FO':dcf2_RCU8_FO,
        'dcf2_RCU9_FO':dcf2_RCU9_FO,
        'dcf2_RCU10_FO':dcf2_RCU10_FO,
        'dcf2_RCU11_FO':dcf2_RCU11_FO,
        'dcf2_RCU12_FO':dcf2_RCU12_FO,
        'dcf2_RCU13_FO':dcf2_RCU13_FO,
        'dcf2_RCUBARMM_FO':dcf2_RCUBARMM_FO,

        #NEW DATA MAY 6(FRANZ)
        'dcf2_CPAs':dcf2_CPAs,

        'dcf2_COFFEE':dcf2_COFFEE,
        'dcf2_CACAO':dcf2_CACAO,
        'dcf2_COCONUT':dcf2_COCONUT,
        'dcf2_PFN':dcf2_PFN,

        #NEW DATA MAY6(ANDY)
        'dcf_form2_rcu8_fo' :dcf_form2_rcu8_fo,
        'dcf_form2_rcu9_fo' :dcf_form2_rcu9_fo,
        'dcf_form2_rcu10_fo' :dcf_form2_rcu10_fo,
        'dcf_form2_rcu11_fo' :dcf_form2_rcu11_fo,
        'dcf_form2_rcu12_fo' :dcf_form2_rcu12_fo,
        'dcf_form2_rcu13_fo' :dcf_form2_rcu13_fo,
        'dcf_form2_rcuBARMM_fo' :dcf_form2_rcuBARMM_fo,

        'dcf_form2_nom_cacao' :dcf_form2_nom_cacao,
        'dcf_form2_nom_coffee' :dcf_form2_nom_coffee,
        'dcf_form2_nom_coconut' :dcf_form2_nom_coconut,
        'dcf_form2_nom_PFN' :dcf_form2_nom_PFN,

        #NEW DATA MAY3(FRANZ)
        'dcf1_COFFEE_FO':dcf1_COFFEE_FO,
        'dcf1_CACAO_FO':dcf1_CACAO_FO,
        'dcf1_COCONUT_FO':dcf1_COCONUT_FO,
        'dcf1_PFN_FO':dcf1_PFN_FO,

        #NEW DATA MAY2 (ANDY)
        'dcf_form2_rcu8' :dcf_form2_rcu8,
        'dcf_form2_rcu9' :dcf_form2_rcu9,
        'dcf_form2_rcu10' :dcf_form2_rcu10,
        'dcf_form2_rcu11' :dcf_form2_rcu11,
        'dcf_form2_rcu12' :dcf_form2_rcu12,
        'dcf_form2_rcu13' :dcf_form2_rcu13,
        'dcf_form2_rcuBARMM' :dcf_form2_rcuBARMM,

        'dcf_form2_rcu8_nom' :dcf_form2_rcu8_nom,
        'dcf_form2_rcu9_nom' :dcf_form2_rcu9_nom,
        'dcf_form2_rcu10_nom' :dcf_form2_rcu10_nom,
        'dcf_form2_rcu11_nom' :dcf_form2_rcu11_nom,
        'dcf_form2_rcu12_nom' :dcf_form2_rcu12_nom,
        'dcf_form2_rcu13_nom' :dcf_form2_rcu13_nom,
        'dcf_form2_rcuBARMM_nom' :dcf_form2_rcuBARMM_nom,

        #NEW DATA APRIL30
        'dcf1_COFFEE_8':dcf1_COFFEE_8,
        'dcf1_CACAO_8':dcf1_CACAO_8,
        'dcf1_COCONUT_8':dcf1_COCONUT_8,
        'dcf1_PFN_8':dcf1_PFN_8,

        'dcf1_COFFEE_9':dcf1_COFFEE_9,
        'dcf1_CACAO_9':dcf1_CACAO_9,
        'dcf1_COCONUT_9':dcf1_COCONUT_9,
        'dcf1_PFN_9':dcf1_PFN_9,

        'dcf1_COFFEE_10':dcf1_COFFEE_10,
        'dcf1_CACAO_10':dcf1_CACAO_10,
        'dcf1_COCONUT_10':dcf1_COCONUT_10,
        'dcf1_PFN_10':dcf1_PFN_10,

        'dcf1_COFFEE_11':dcf1_COFFEE_11,
        'dcf1_CACAO_11':dcf1_CACAO_11,
        'dcf1_COCONUT_11':dcf1_COCONUT_11,
        'dcf1_PFN_11':dcf1_PFN_11,

        'dcf1_COFFEE_12':dcf1_COFFEE_12,
        'dcf1_CACAO_12':dcf1_CACAO_12,
        'dcf1_COCONUT_12':dcf1_COCONUT_12,
        'dcf1_PFN_12':dcf1_PFN_12,

        'dcf1_COFFEE_13':dcf1_COFFEE_13,
        'dcf1_CACAO_13':dcf1_CACAO_13,
        'dcf1_COCONUT_13':dcf1_COCONUT_13,
        'dcf1_PFN_13':dcf1_PFN_13,

        'dcf1_COFFEE_BARMM':dcf1_COFFEE_BARMM,
        'dcf1_CACAO_BARMM':dcf1_CACAO_BARMM,
        'dcf1_COCONUT_BARMM':dcf1_COCONUT_BARMM,
        'dcf1_PFN_BARMM':dcf1_PFN_BARMM,
        #END OF DATA APRIL30

        'dcf_form1maleip_appr' :dcf_form1maleip_appr,
        'dcf_form1femaleip_appr' :dcf_form1femaleip_appr,
        'dcf_form1maleyouth_appr' :dcf_form1maleyouth_appr,
        'dcf_form1femaleyouth_appr' :dcf_form1femaleyouth_appr,
        'dcf_form1male_appr' :dcf_form1male_appr,
        'dcf_form1female_appr' :dcf_form1female_appr,

        'dcf3_total_entrep': dcf3_total_entrep,
        'dcf3_total_agri': dcf3_total_agri,
        'dcf3_total_es': dcf3_total_es,
        'dcf3_total_org': dcf3_total_org,
        'dcf3_region8_entrep' :dcf3_region8_entrep,
        'dcf3_region8_agri' :dcf3_region8_agri,
        'dcf3_region8_es' :dcf3_region8_es,
        'dcf3_region8_org' :dcf3_region8_org,

        'dcf3_region9_entrep' :dcf3_region9_entrep,
        'dcf3_region9_agri' :dcf3_region9_agri,
        'dcf3_region9_es' :dcf3_region9_es,
        'dcf3_region9_org' :dcf3_region9_org,

        'dcf3_region10_entrep' :dcf3_region10_entrep,
        'dcf3_region10_agri' :dcf3_region10_agri,
        'dcf3_region10_es' :dcf3_region10_es,
        'dcf3_region10_org' :dcf3_region10_org,

        'dcf3_region11_entrep' :dcf3_region11_entrep,
        'dcf3_region11_agri' :dcf3_region11_agri,
        'dcf3_region11_es' :dcf3_region11_es,
        'dcf3_region11_org' :dcf3_region11_org,

        'dcf3_region12_entrep' :dcf3_region12_entrep,
        'dcf3_region12_agri' :dcf3_region12_agri,
        'dcf3_region12_es' :dcf3_region12_es,
        'dcf3_region12_org' :dcf3_region12_org,

        'dcf3_region13_entrep' :dcf3_region13_entrep,
        'dcf3_region13_agri' :dcf3_region13_agri,
        'dcf3_region13_es' :dcf3_region13_es,
        'dcf3_region13_org' :dcf3_region13_org,

        'dcf3_regionB_entrep' :dcf3_regionB_entrep,
        'dcf3_regionB_agri' :dcf3_regionB_agri,
        'dcf3_regionB_es' :dcf3_regionB_es,
        'dcf3_regionB_org' :dcf3_regionB_org,

        'dcf4_TOT':dcf4_TOT,
        'dcf7_TFPCOFFEE':dcf7_TFPCOFFEE,
        'dcf7_TFPCACAO':dcf7_TFPCACAO,
        'dcf7_TFPCOCONUT':dcf7_TFPCOCONUT,
        'dcf7_TFPPFN':dcf7_TFPPFN,
        'dcf7_TFRCOFFEE':dcf7_TFRCOFFEE,
        'dcf7_TFRCACAO':dcf7_TFRCACAO,
        'dcf7_TFRCOCONUT':dcf7_TFRCOCONUT,       
        'dcf7_TFRPFN':dcf7_TFRPFN,
        'dcf7_tfn_coffee':dcf7_tfn_coffee,
        'dcf7_tfn_coconut':dcf7_tfn_coconut,
        'dcf7_tfn_cacao':dcf7_tfn_cacao,
        'dcf7_tfn_PFN':dcf7_tfn_PFN,
        'dcf7_tfi_coffee':dcf7_tfi_coffee,
        'dcf7_tfi_coconut':dcf7_tfi_coconut,
        'dcf7_tfi_cacao':dcf7_tfi_cacao,
        'dcf7_tfi_PFN':dcf7_tfi_PFN,
        'dcf7_tmpr_coffee':dcf7_tmpr_coffee,
        'dcf7_tmpr_cacao':dcf7_tmpr_cacao,
        'dcf7_tmpr_coconut':dcf7_tmpr_coconut,
        'dcf7_tmpr_PFN':dcf7_tmpr_PFN,
        'dcf7_tmn_coffee':dcf7_tmn_coffee,
        'dcf7_tmn_coconut':dcf7_tmn_coconut,
        'dcf7_tmn_cacao':dcf7_tmn_cacao,
        'dcf7_tmn_PFN':dcf7_tmn_PFN,
        'dcf7_tmi_coffee':dcf7_tmi_coffee,
        'dcf7_tmi_coconut':dcf7_tmi_coconut,
        'dcf7_tmi_cacao':dcf7_tmi_cacao,
        'dcf7_tmi_PFN':dcf7_tmi_PFN,
        'dcf7_bmpr_coffee':dcf7_bmpr_coffee,
        'dcf7_bmpr_coconut':dcf7_bmpr_coconut,
        'dcf7_bmpr_cacao':dcf7_bmpr_cacao,
        'dcf7_bmpr_PFN':dcf7_bmpr_PFN,
        'dcf7_bmn_coffee':dcf7_bmn_coffee,
        'dcf7_bmn_coconut':dcf7_bmn_coconut,
        'dcf7_bmn_cacao':dcf7_bmn_cacao,
        'dcf7_bmn_PFN':dcf7_bmn_PFN,
        'dcf7_bmi_coffee':dcf7_bmi_coffee,
        'dcf7_bmi_coconut':dcf7_bmi_coconut,
        'dcf7_bmi_cacao':dcf7_bmi_cacao,
        'dcf7_bmi_PFN':dcf7_bmi_PFN,
        'dcf7_TA':dcf7_TA,
        'dcf7_TFP':dcf7_TFP,
        'dcf7_TFR':dcf7_TFR,
        'dcf7_TFN':dcf7_TFN,
        'dcf7_TFI':dcf7_TFI,
        'dcf7_TSMPR':dcf7_TSMPR,
        'dcf7_TSMN':dcf7_TSMN,
        'dcf7_TSMI':dcf7_TSMI,
        'dcf7_BMPR':dcf7_BMPR,
        'dcf7_BMN':dcf7_BMN,
        'dcf7_BMI':dcf7_BMI,
        'dcf10_FO':dcf10_FO,
        'dcf10_MSME':dcf10_MSME,
        'dcf10_NOT':dcf10_NOT,
        'dcf_form10_male':dcf_form10_male,
        'dcf_form10_female':dcf_form10_female,

######## RAPID CODE ####################################################################################################
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
        'over_all_commodity_count10':over_all_commodity_count10,
        'over_all_commodity_count11':over_all_commodity_count11,
        'typebdsp':typebdsp,
        'form1_data_sep':form1_data_sep,
        'form1_data_oct':form1_data_oct,
        'form1_data_nov':form1_data_nov,
        'form1_data_dec':form1_data_dec,
        'form1_data_jan':form1_data_jan,
        'form1_percentages':form1_percentages,
        'form1_thismonth':form1_thismonth,
        'form1_lastmonth':form1_lastmonth,
        'form1_subperc':form1_subperc,
        'form2_data_sep':form2_data_sep,
        'form2_data_oct':form2_data_oct,
        'form2_data_nov':form2_data_nov,
        'form2_data_dec':form2_data_dec,
        'form2_data_jan':form2_data_jan,
        'form2_percentages':form2_percentages,
        'form2_thismonth':form2_thismonth,
        'form2_lastmonth':form2_lastmonth,
        'form2_subperc':form2_subperc,
        'form3_data_sep':form3_data_sep,
        'form3_data_oct':form3_data_oct,
        'form3_data_nov':form3_data_nov,
        'form3_data_dec':form3_data_dec,
        'form3_data_jan':form3_data_jan,
        'form3_percentages':form3_percentages,
        'form3_thismonth':form3_thismonth,
        'form3_lastmonth':form3_lastmonth,
        'form3_subperc':form3_subperc,
        'form4_data_sep':form4_data_sep,
        'form4_data_oct':form4_data_oct,
        'form4_data_nov':form4_data_nov,
        'form4_data_dec':form4_data_dec,
        'form4_data_jan':form4_data_jan,
        'form4_percentages':form4_percentages,
        'form4_thismonth':form4_thismonth,
        'form4_lastmonth':form4_lastmonth,
        'form4_subperc':form4_subperc,
        'form5_data_sep':form5_data_sep,
        'form5_data_oct':form5_data_oct,
        'form5_data_nov':form5_data_nov,
        'form5_data_dec':form5_data_dec,
        'form5_data_jan':form5_data_jan,
        'form5_percentages':form5_percentages,
        'form5_thismonth':form5_thismonth,
        'form5_lastmonth':form5_lastmonth,
        'form5_subperc':form5_subperc,
        'form6_data_sep':form6_data_sep,
        'form6_data_oct':form6_data_oct,
        'form6_data_nov':form6_data_nov,
        'form6_data_dec':form6_data_dec,
        'form6_data_jan':form6_data_jan,
        'form6_percentages':form6_percentages,
        'form6_thismonth':form6_thismonth,
        'form6_lastmonth':form6_lastmonth,
        'form6_subperc':form6_subperc,
        'form7_data_sep':form7_data_sep,
        'form7_data_oct':form7_data_oct,
        'form7_data_nov':form7_data_nov,
        'form7_data_dec':form7_data_dec,
        'form7_data_jan':form7_data_jan,
        'form7_percentages':form7_percentages,
        'form7_thismonth':form7_thismonth,
        'form7_lastmonth':form7_lastmonth,
        'form7_subperc':form7_subperc,
        'form9_data_sep':form9_data_sep,
        'form9_data_oct':form9_data_oct,
        'form9_data_nov':form9_data_nov,
        'form9_data_dec':form9_data_dec,
        'form9_data_jan':form9_data_jan,
        'form9_percentages':form9_percentages,
        'form9_thismonth':form9_thismonth,
        'form9_lastmonth':form9_lastmonth,
        'form9_subperc':form9_subperc,
        'form10_data_sep':form10_data_sep,
        'form10_data_oct':form10_data_oct,
        'form10_data_nov':form10_data_nov,
        'form10_data_dec':form10_data_dec,
        'form10_data_jan':form10_data_jan,
        'form10_percentages':form10_percentages,
        'form10_thismonth':form10_thismonth,
        'form10_lastmonth':form10_lastmonth,
        'form10_subperc':form10_subperc,
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
        'dcf_form10female':dcf_form10female,
        'dcf_form10male':dcf_form10male,
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
        'dcf_form7total':dcf_form7total,
        'form1_data_feb':form1_data_feb,
        'form2_data_feb':form2_data_feb,
        'form3_data_feb':form3_data_feb,
        'form4_data_feb':form4_data_feb,
        'form5_data_feb':form5_data_feb,
        'form6_data_feb':form6_data_feb,
        'form7_data_feb':form7_data_feb,
        'form9_data_feb':form9_data_feb,
        'form10_data_feb':form10_data_feb,
        'form11_data_feb':form11_data_feb,
        'dcf_form9capb':dcf_form9capb,
        'dcf_form9meetings':dcf_form9meetings,
        'dcf_form9policy':dcf_form9policy,
        'dcf_form9budg':dcf_form9budg,
        'dcf_form11ip':dcf_form11ip,
        'dcf_form11youth':dcf_form11youth,
        'dcf_form11pwd':dcf_form11pwd,
        'dcf_form11sc':dcf_form11sc,
        'dcf_form11female':dcf_form11female,
        'dcf_form11male':dcf_form11male,
        'dcf_form6actualbudget':dcf_form6actualbudget,
        'form1_data_mar':form1_data_mar,
        'form2_data_mar':form2_data_mar,
        'form3_data_mar':form3_data_mar,
        'form4_data_mar':form4_data_mar,
        'form5_data_mar':form5_data_mar,
        'form6_data_mar':form6_data_mar,
        'form7_data_mar':form7_data_mar,
        'form9_data_mar':form9_data_mar,
        'form10_data_mar':form10_data_mar,
        'form11_data_mar':form11_data_mar,
        'form1_data_apr':form1_data_apr,
        'form2_data_apr':form2_data_apr,
        'form3_data_apr':form3_data_apr,
        'form4_data_apr':form4_data_apr,
        'form5_data_apr':form5_data_apr,
        'form6_data_apr':form6_data_apr,
        'form7_data_apr':form7_data_apr,
        'form9_data_apr':form9_data_apr,
        'form10_data_apr':form10_data_apr,
        'form11_data_apr':form11_data_apr,
        'form1_data_may':form1_data_may,
        'form2_data_may':form2_data_may,
        'form3_data_may':form3_data_may,
        'form4_data_may':form4_data_may,
        'form5_data_may':form5_data_may,
        'form6_data_may':form6_data_may,
        'form7_data_may':form7_data_may,
        'form9_data_may':form9_data_may,
        'form10_data_may':form10_data_may,
        'form11_data_may':form11_data_may,
        'form1_data_june':form1_data_june,
        'form2_data_june':form2_data_june,
        'form3_data_june':form3_data_june,
        'form4_data_june':form4_data_june,
        'form5_data_june':form5_data_june,
        'form6_data_june':form6_data_june,
        'form7_data_june':form7_data_june,
        'form9_data_june':form9_data_june,
        'form10_data_june':form10_data_june,
        'form11_data_june':form11_data_june,

        'dips_listdcf1':dips_listdcf1,
        'form1_datatabledip': form1_datatabledip

    }



def position_data_filter():
    _filter = "WHERE 1 "
    JOB = session["USER_DATA"][0]["job"].lower()

    if(JOB in "admin" or JOB in "super admin" or session["USER_DATA"][0]['sg_info']['user_group']=="NATIONAL" or session["USER_DATA"][0]['sg_info']['user_group']=="ALL_OVERVIEW"):
        session["USER_DATA"][0]["office"] = "NPCO"
        _filter = "WHERE 1 "
    else:
        session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
        _filter = "WHERE `upload_by` in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])

    return _filter
