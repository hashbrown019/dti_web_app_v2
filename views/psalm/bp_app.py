from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session
from modules.Connections import mysql
from decimal import Decimal
from flask_session import Session
from views.psalm.dashboard import display_data as displayData
from views.psalm.dashboard import filter_data as filterData
from views.psalm.formc_insert import insert_data as insertData
from views.psalm.dashboard import update_data as updateData
from views.psalm.spreadsheet import import_excel as import_csv
import Configurations as c
import xlrd
from werkzeug.utils import secure_filename
import os

db = mysql(*c.DB_CRED)
db.err_page = 0
app = Blueprint("form_c",__name__,template_folder="pages")

def is_on_session(): return ('USER_DATA' in session)

@app.route('/formc')
def index():
    return render_template("index.html")

@app.route('/importcsv',methods = ['GET','POST'])
def importcsv():
    import_csv.importcsv(request)
    return redirect("/spreadsheet")

@app.route('/insert', methods = ['POST'])
def insert():
    insertData.insert(request)
    return redirect("/cform")
    


@app.route('/update',methods=['POST','GET'])
def update():
    updateData.update(request)
    return redirect("/formcdashboard")




@app.route("/formcdashboard")
def formcdashboard():
    disp = displayData.display()
    return render_template("formcdashboard.html",**disp)

@app.route("/formcdashboardfilter",methods=['POST','GET'])
def formcdashboardfilter():
    filt = filterData.data_filter(request)
    return render_template("formcdashboardfilter.html",**filt)

@app.route("/menu")
def menu():
    if(is_on_session()):
        return render_template("menu.html",user_data=session["USER_DATA"][0])
    else:
        return redirect("/login?force_url=1")


@app.route("/cform")
def cform():
    return render_template("formc.html")


@app.route("/spreadsheet")
def spreadsheet():
    return render_template("spreadsheet.html")


if __name__ == "__main__":
    app.run(debug=True)

    # sample edit