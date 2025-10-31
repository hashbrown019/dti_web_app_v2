from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file, jsonify
from modules.Connections import mysql,sqlite
import Configurations as c
import json

app = Blueprint("fmi",__name__,template_folder="fmi_page")
def is_on_session(): return ('USER_DATA' in session)

rapid_sql = mysql(*c.DB_CRED)

@app.route('/fmi_dashboard')
def fmi_dashboard():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")

    FMR_total = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi")[0]['total']
    
    FMR_completed = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget FROM dcf_fmi WHERE `form_8_implementation_status`='Completed'")[0]
    FMR_ongoing = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget  FROM dcf_fmi WHERE `form_8_implementation_status`='On-going'")[0]
    FMR_no1 = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 1'")[0]
    FMR_no2 = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 2'")[0]
    FMR_no3 = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 3'")[0]
    FMR_pending = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget FROM dcf_fmi WHERE `form_8_implementation_status`='Pending'")[0]
    FMR_noa = rapid_sql.select("SELECT COUNT(*) AS total, IFNULL(SUM(form_8_profile_length), 0 ) AS total_km, IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget FROM dcf_fmi WHERE `form_8_implementation_status`='Issuance of NOA'")[0]
    
    FMR_Batch1_pending = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Pending' AND `form_8_profile_batch`=1")[0]['total']
    FMR_Batch1_ongoing = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='On-going' AND `form_8_profile_batch`=1")[0]['total']
    FMR_Batch1_no1 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 1' AND `form_8_profile_batch`=1")[0]['total']
    FMR_Batch1_no2 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 2' AND `form_8_profile_batch`=1")[0]['total']
    FMR_Batch1_no3 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 3' AND `form_8_profile_batch`=1")[0]['total']
    FMR_Batch1_noa = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Issuance of NOA' AND `form_8_profile_batch`=1")[0]['total']
    FMR_Batch1_completed = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Completed' AND `form_8_profile_batch`=1")[0]['total']

    FMR_Batch2_pending = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Pending' AND `form_8_profile_batch`=2")[0]['total']
    FMR_Batch2_ongoing = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='On-going' AND `form_8_profile_batch`=2")[0]['total']
    FMR_Batch2_no1 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 1' AND `form_8_profile_batch`=2")[0]['total']
    FMR_Batch2_no2 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 2' AND `form_8_profile_batch`=2")[0]['total']
    FMR_Batch2_no3 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 3' AND `form_8_profile_batch`=2")[0]['total']
    FMR_Batch2_noa = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Issuance of NOA' AND `form_8_profile_batch`=2")[0]['total']
    FMR_Batch2_completed = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Completed' AND `form_8_profile_batch`=2")[0]['total']

    FMR_Batch3_pending = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Pending' AND `form_8_profile_batch`=3")[0]['total']
    FMR_Batch3_ongoing = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='On-going' AND `form_8_profile_batch`=3")[0]['total']
    FMR_Batch3_no1 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 1' AND `form_8_profile_batch`=3")[0]['total']
    FMR_Batch3_no2 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 2' AND `form_8_profile_batch`=3")[0]['total']
    FMR_Batch3_no3 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 3' AND `form_8_profile_batch`=3")[0]['total']
    FMR_Batch3_noa = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Issuance of NOA' AND `form_8_profile_batch`=3")[0]['total']
    FMR_Batch3_completed = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Completed' AND `form_8_profile_batch`=3")[0]['total']

    FMR_Batch4_pending = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Pending' AND `form_8_profile_batch`=4")[0]['total']
    FMR_Batch4_ongoing = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='On-going' AND `form_8_profile_batch`=4")[0]['total']
    FMR_Batch4_no1 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 1' AND `form_8_profile_batch`=4")[0]['total']
    FMR_Batch4_no2 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 2' AND `form_8_profile_batch`=4")[0]['total']
    FMR_Batch4_no3 = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='For NO 3' AND `form_8_profile_batch`=4")[0]['total']
    FMR_Batch4_noa = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Issuance of NOA' AND `form_8_profile_batch`=4")[0]['total']
    FMR_Batch4_completed = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi WHERE `form_8_implementation_status`='Completed' AND `form_8_profile_batch`=4")[0]['total']

    background_colors = ['#629DDD','#A4BF7F','#A48BC1','#E2918F','#F4D470','#E8AA78','#A5D7D8','#7173A9','#77838E']

    FMR_Batch1_data = {
        'data' : [FMR_Batch1_pending,FMR_Batch1_ongoing,FMR_Batch1_no1,FMR_Batch1_no2,FMR_Batch1_no3,FMR_Batch1_noa,FMR_Batch1_completed],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }
    FMR_Batch2_data = {
        'data' : [FMR_Batch2_pending,FMR_Batch2_ongoing,FMR_Batch2_no1,FMR_Batch2_no2,FMR_Batch2_no3,FMR_Batch2_noa,FMR_Batch2_completed],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }
    FMR_Batch3_data = {
        'data' : [FMR_Batch3_pending,FMR_Batch3_ongoing,FMR_Batch3_no1,FMR_Batch3_no2,FMR_Batch3_no3,FMR_Batch3_noa,FMR_Batch3_completed],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }
    FMR_Batch4_data = {
        'data' : [FMR_Batch4_pending,FMR_Batch4_ongoing,FMR_Batch4_no1,FMR_Batch4_no2,FMR_Batch4_no3,FMR_Batch4_noa,FMR_Batch4_completed],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }

    FMR_data = {
        'FMR_totalkm_completed_ongoing' : (FMR_completed['total_km']+FMR_ongoing['total_km']),
        'FMR_total': FMR_total,
        'FMR_completed': FMR_completed,
        'FMR_ongoing': FMR_ongoing,
        'FMR_no1': FMR_no1,
        'FMR_no2': FMR_no2,
        'FMR_no3': FMR_no3,
        'FMR_pending': FMR_pending,
        'FMR_noa': FMR_noa,
        'FMR_Batch1_data': FMR_Batch1_data
    }
    FMR_data_chart = {
        'FMR_Batch1_data' : FMR_Batch1_data,
        'FMR_Batch2_data' : FMR_Batch2_data,
        'FMR_Batch3_data' : FMR_Batch3_data,
        'FMR_Batch4_data' : FMR_Batch4_data
    }
    return render_template("fmi_dashboard.html",user_data=session["USER_DATA"][0], FMR_data=FMR_data,FMR_data_chart=json.dumps(FMR_data_chart))

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
    