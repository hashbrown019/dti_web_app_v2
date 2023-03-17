from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def updateform7(request):

    if request.method == 'POST':
        id = request.form['id']
        form_7_implementing_unit = request.form['form_7_implementing_unit']
        form_7_title_trade_promotion = request.form['form_7_title_trade_promotion']
        form_7_type_of_trade_promotion = request.form['form_7_type_of_trade_promotion']
        form_7_dip_indicate = request.form['form_7_dip_indicate']
        form_7_start_date = request.form['form_7_start_date']
        form_7_end_date = request.form['form_7_end_date']
        form_7_name_of_po = request.form['form_7_name_of_po']
        form_7_amount = request.form['form_7_amount']
        form_7_venue = request.form['form_7_venue']
        form_7_rapid_actual_budget = request.form['form_7_rapid_actual_budget']
        form_7_name_of_beneficiary = request.form['form_7_name_of_beneficiary']
        form_7_commodity = request.form['form_7_commodity']
        form_7_msme = request.form['form_7_msme']
        form_7_fo = request.form['form_7_fo']
        form_7_farmer = request.form['form_7_farmer']
        form_7_male = request.form['form_7_male']
        form_7_female = request.form['form_7_female']
        form_7_pwd = request.form['form_7_pwd']
        form_7_youth = request.form['form_7_youth']
        form_7_ip = request.form['form_7_ip']
        form_7_sc = request.form['form_7_sc']
        form_7_type_of_products = request.form['form_7_type_of_products']
        form_7_name_of_buyer = request.form['form_7_name_of_buyer']
        form_7_cash_sales = request.form['form_7_cash_sales']
        form_7_booked_sales = request.form['form_7_booked_sales']
        form_7_under_negotiations = request.form['form_7_under_negotiations']
        form_7_total_autosum  = request.form.get('form_7_total_autosum')

        sql = """UPDATE dcf_trade_promotion
               SET form_7_implementing_unit='{}',form_7_title_trade_promotion='{}',form_7_type_of_trade_promotion='{}',form_7_dip_indicate='{}',form_7_start_date='{}',form_7_end_date='{}',form_7_name_of_po='{}',form_7_amount='{}',form_7_venue='{}',form_7_rapid_actual_budget='{}',form_7_name_of_beneficiary='{}',form_7_commodity='{}',form_7_msme='{}',form_7_fo='{}',form_7_farmer='{}',form_7_male='{}',form_7_female='{}',form_7_pwd='{}',form_7_youth='{}',form_7_ip='{}',form_7_sc='{}',form_7_type_of_products='{}',form_7_name_of_buyer='{}',form_7_cash_sales='{}',form_7_booked_sales='{}',form_7_under_negotiations='{}',form_7_total_autosum='{}'
               WHERE id={}
            """.format(form_7_implementing_unit,form_7_title_trade_promotion,form_7_type_of_trade_promotion,form_7_dip_indicate,form_7_start_date,form_7_end_date,form_7_name_of_po,form_7_amount,form_7_venue,form_7_rapid_actual_budget,form_7_name_of_beneficiary,form_7_commodity,form_7_msme,form_7_fo,form_7_farmer,form_7_male,form_7_female,form_7_pwd,form_7_youth,form_7_ip,form_7_sc,form_7_type_of_products,form_7_name_of_buyer,form_7_cash_sales,form_7_booked_sales,form_7_under_negotiations,form_7_total_autosum, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)