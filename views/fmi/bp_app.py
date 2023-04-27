from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file

app = Blueprint("fmi",__name__,template_folder="fmi_page")
def is_on_session(): return ('USER_DATA' in session)

@app.route('/fmi_dashboard')
def fmi_dashboard():
    return render_template("fmi_dashboard.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_a')
def fmi_form_a():
    return render_template("fmi_includes/forms/fmi_form_a.html",user_data=session["USER_DATA"][0])


