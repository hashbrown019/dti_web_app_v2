from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file
from decimal import Decimal
import pandas as pd
from tqdm import tqdm
from time import sleep
import xlrd
import json
from werkzeug.utils import secure_filename
import os
from views.dcf.form_insert import insert_form4 as insertData4
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0
app = Blueprint("dcf",__name__,template_folder="pages")

def is_on_session(): return ('USER_DATA' in session)

@app.route('/dcf_dashboard')
def dcf_dashboard():
    return render_template("dcf_dashboard.html",user_data=session["USER_DATA"][0])

@app.route('/dcf_forms')
def dcf_forms():
    return redirect("/dcf_forms")

@app.route('/form1')
def form1():
    return render_template('includes/forms/form1.html',user_data=session["USER_DATA"][0])

@app.route('/form2')
def form2():
    return render_template('form2.html')

@app.route('/form3')
def form3():
    return render_template('form3.html')

@app.route('/form4')
def form4():
    return render_template('includes/forms/form4.html',user_data=session["USER_DATA"][0])

@app.route('/form5')
def form5():
    return render_template('includes/forms/form5.html',user_data=session["USER_DATA"][0])

@app.route('/form6')
def form6():
    return redirect('form6.html')

@app.route('/form7')
def form7():
    return redirect('form7.html')

@app.route('/form8')
def form8():
    return redirect('form8.html')

@app.route('/form9')
def form9():
    return redirect('form9.html')

@app.route('/form10')
def form10():
    return redirect('form10.html')

@app.route('/form11')
def form11():
    return redirect('form11.html')

@app.route('/form12')
def form12():
    return redirect('form12.html')

@app.route('/insert_form4', methods = ['POST'])
def insert_form4():
    insertData4.insert_form4(request)
    return redirect("/form4")




# if __name__ == "__main__":
#     app.run(debug=True)
