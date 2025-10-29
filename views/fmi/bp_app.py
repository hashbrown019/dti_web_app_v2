from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file
import Configurations as c

app = Blueprint("fmi",__name__,template_folder="fmi_page")
def is_on_session(): return ('USER_DATA' in session)

@app.route('/fmi_dashboard')
def fmi_dashboard():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_dashboard.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_a')
def fmi_form_a():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/fmi_form_a.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_b')
def fmi_form_b():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/fmi_form_b.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_c1')
def fmi_form_c1():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/fmi_form_c1.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_c2')
def fmi_form_c2():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/fmi_form_c2.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_d')
def fmi_form_d():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/fmi_form_d.html",user_data=session["USER_DATA"][0])

@app.route('/fmi_form_e')
def fmi_form_e():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/fmi_form_e.html",user_data=session["USER_DATA"][0])

@app.route('/project_profile')
def project_profile():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
    return render_template("fmi_includes/forms/project_profile.html",user_data=session["USER_DATA"][0])
    