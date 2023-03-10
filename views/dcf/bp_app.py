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
from views.dcf.form_insert import insert_form5 as insertData5
from views.dcf.form_insert import insert_form1 as insertData1
from views.dcf.form_insert import insert_form3 as insertData3
from views.dcf.form_insert import insert_form2 as insertData2
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

@app.route('/dcf/<form>')
def form1(form):
    return render_template('includes/forms/{}.html'.format(form),user_data=session["USER_DATA"][0])

@app.route('/dcf_spreadsheet')
def dcf_spreadsheet():
    return render_template("dcf_spreadsheet.html",user_data=session["USER_DATA"][0])

@app.route('/insert_form4', methods = ['POST'])
def insert_form4():
    insertData4.insert_form4(request)
    return redirect("/form4")

@app.route('/insert_form5', methods = ['POST'])
def insert_form5():
    insertData5.insert_form5(request)
    return redirect("/form5")

@app.route('/insert_form1', methods = ['POST'])
def insert_form1():
    insertData1.insert_form1(request)
    return redirect("/form1")

@app.route('/insert_form3', methods = ['POST'])
def insert_form3():
    insertData3.insert_form3(request)
    return redirect("/form3")


@app.route('/insert_form2', methods = ['POST'])
def insert_form2():
    insertData2.insert_form2(request)
    return redirect("/form2")

# if __name__ == "__main__":
#     app.run(debug=True)
