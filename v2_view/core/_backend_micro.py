from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql, sqlite
import Configurations as c
import os
import json

from v2_view.core import dash_api
from v2_view.core import dash_script
from v2_view.core import _backend_sub

app = Blueprint("_micro", __name__, template_folder='pages')
rapid_mysql = mysql(*c.DB_CRED)


class _main:
    def __init__(self, arg):
        super(_main, self).__init__()
        self.arg = arg
#--dynamic insert------------------------------------------------------------------------------------------------
    @app.route("/insert/<TABLE>", methods=["POST", "GET"])
    def insert(TABLE):
        coloumn = ""
        values = ""
        for ids in request.form:
            coloumn += f",`{ids}`"
            values += f",'{request.form[ids]}' "
        res = rapid_mysql.do(f"INSERT {TABLE} ({coloumn[1:]}) VALUES ({values[1:]})")
        return jsonify(res)
#--micro------------------------------------------------------------------------------------------------
    @app.route("/mis-v4-micro/test", methods=["POST", "GET"])
    @c.login_auth_web()
    def micro_index():
        return {"status": "test auth", "session": session["USER_DATA"][0]}

    @app.route("/micro_test", methods=["GET"])
    def micro_test():
        return {"status": "test no auth"}
#--dip tracker------------------------------------------------------------------------------------------------
    @app.route("/view-tracker-dip-main-content")
    def view_tracker_dip_main_content():
        dipData = rapid_mysql.select("SELECT * FROM dcf_prep_review_aprv_status")
        return jsonify(dipData)
#--sales tracker----------------------------------------------------------------------------------------------
    @app.route("/micro/tabl-get-data", methods=["GET", "POST"])
    def core_tracker_sales():
        ids = request.form['id']
        tbl = request.form['tbl']
        cpa = rapid_mysql.select(f"SELECT * FROM `{tbl}` WHERE `id`={ids};")
        return jsonify(cpa)

    @app.route("/micro/get_formB_data", methods=["GET", "POST"])
    def get_formB_data():
        condition = request.form['condition']
        formBData = rapid_mysql.select(f"SELECT * FROM `form_b` {condition};")
        return jsonify(formBData)

    @app.route("/micro/insert_sales_tracker", methods=["POST"])
    def insert_sales_tracker():
        try:
            field_mapping = {
                "nameSTID": "ST_id",
                "nameID": "CPA_id",
                "nameRCU": "ST_rcu",
                "namePCU": "ST_pcu",
                "nameCOMMODITY": "ST_commodity",
                "nameDIP": "ST_nameofdip",
                "nameFO": "ST_nameof_fo",
                "af-msme": "ST_af_msme",
                "addressFO": "ST_address_fo",
                "productType": "ST_product_type",
                "vs": "ST_vol_supplied",
                "aveP": "ST_ave_price",
                "totalTransaction": "ST_total_transaction",
                "incentives": "ST_incentives_provided",
                "date": "ST_date",
            }
            columns = []
            values = []
            for form_field, db_column in field_mapping.items():
                if form_field in request.form:
                    columns.append(f"`{db_column}`")
                    values.append(f"'{request.form[form_field]}'")
            if not columns:
                return jsonify({"status": "error", "message": "No valid data provided"}), 400
            query = f"INSERT INTO `sales_tracker` ({', '.join(columns)}) VALUES ({', '.join(values)})"
            res = rapid_mysql.do(query)
            return jsonify({"status": "success", "message": "Data inserted successfully", "result": res})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
#--grievance------------------------------------------------------------------------------------------------
@app.route("/get_grievance_data")
@c.login_auth_web()
def get_grievance_data():
    try:
        record_id = request.args.get('id') 
        if record_id:
            query = f"SELECT * FROM grievance WHERE Id = {record_id}"
        else:
            query = "SELECT * FROM grievance"
        grievance_data = rapid_mysql.select(query)
        if record_id and not grievance_data:
            return jsonify({"status": "error", "message": "No data found for the given ID"}), 404
        return jsonify(grievance_data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/get_entry/<int:id>', methods=['GET'])
def get_entry(id):
    entry = rapid_mysql.select(str(id)) 
    if entry:
        return jsonify(entry)
    else:
        return jsonify({"error": "Entry not found"}), 404

@app.route("/delete_grievance_data/<int:id>", methods=["DELETE"])
def delete_grievance_data(id):
    try:
        query = f"DELETE FROM grievance WHERE Id = {id}"
        result = rapid_mysql.do(query)
        if result is not None: 
            return jsonify({"status": "success", "message": "Record deleted successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to delete the record"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/update_grievance_data/<int:id>", methods=["POST"])
def update_grievance_data(id):
    try:
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        if not isinstance(data, dict):
            return jsonify({"status": "error", "message": "Invalid data format"}), 400
        update_fields = ", ".join([f"`{key}` = '{value}'" for key, value in data.items()])
        query = f"UPDATE grievance SET {update_fields} WHERE Id = {id}"
        result = rapid_mysql.do(query)
        if result is not None:  
            return jsonify({"status": "success", "message": "Record updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to update the record"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/grievance-table", methods=["GET"])
def grievance_table():
    return redirect("mis-v4/core-grievance-monitoring?table")

@app.route("/insert/grievance", methods=["POST"])
@c.login_auth_web() 
def insert_grievance():
    try:
        user_data = session.get("USER_DATA", [{}])[0]
        created_by = user_data.get("id") 
        data = request.form.to_dict()
        data["created_by"] = created_by 
        columns = ", ".join([f"`{key}`" for key in data.keys()])
        values = ", ".join([f"'{value}'" for value in data.values()])
        query = f"INSERT INTO grievance ({columns}) VALUES ({values})"
        result = rapid_mysql.do(query)
        if result is not None:
            return jsonify({"status": "success", "message": "Grievance submitted successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to submit grievance"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

#SALES TRACKER TABLE ------------------------------------------------------    
@app.route("/sales-tracker-table", methods=["GET"])
def sales_tracker_table():
    return render_template("sales-tracker-table.html")

@app.route("/view-sales-tracker-table/all/<int:ids>", methods=["GET"])
def view_all_sales_tracker_table(ids):
    try:
        stData = rapid_mysql.select(f"SELECT * FROM sales_tracker WHERE CPA_id = {ids}")
        if stData:
            print("Fetched Data:", stData)
            return jsonify(stData)
        else:
            return jsonify({"status": "error", "message": "No records found"}), 404
    except Exception as e:
        print("Error:", str(e)) 
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/view-sales-tracker-table/<int:st_id>", methods=["GET"])
def view_single_sales_tracker_table(st_id):
    try:
        stData = rapid_mysql.select(f"SELECT * FROM sales_tracker WHERE ST_id = {st_id} LIMIT 1")
        if stData:
            print("Fetched Data:", stData[0])
            return jsonify(stData[0]) 
        else:
            return jsonify({"status": "error", "message": "Record not found"}), 404
    except Exception as e:
        print("Error:", str(e)) 
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/delete_sales_tracker_entry/<int:st_id>", methods=["DELETE"])
def delete_sales_tracker_entry(st_id):
    try:
        query = f"DELETE FROM sales_tracker WHERE ST_id = {st_id}"
        result = rapid_mysql.do(query)
        if result is not None:
            return jsonify({"status": "success", "message": "Record deleted successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to delete the record"}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/update_sales_tracker/<int:st_id>", methods=["POST"])
def update_sales_tracker(st_id):
    try:
        field_mapping = {
            "nameID": "CPA_id",
            "nameRCU": "ST_rcu",
            "namePCU": "ST_pcu",
            "nameCOMMODITY": "ST_commodity",
            "nameDIP": "ST_nameofdip",
            "nameFO": "ST_nameof_fo",
            "addressFO": "ST_address_fo",
            "af-msme": "ST_af_msme",
            "productType": "ST_product_type",
            "vs": "ST_vol_supplied",
            "aveP": "ST_ave_price",
            "totalTransaction": "ST_total_transaction",
            "incentives": "ST_incentives_provided",
            "date": "ST_date",
        }
        update_fields = []
        for form_field, db_column in field_mapping.items():
            if form_field in request.form:
                update_fields.append(f"`{db_column}` = '{request.form[form_field]}'")
        if not update_fields:
            return jsonify({"status": "error", "message": "No valid data provided"}), 400
        query = f"UPDATE `sales_tracker` SET {', '.join(update_fields)} WHERE `ST_id` = {st_id}"
        res = rapid_mysql.do(query)
        return jsonify({"status": "success", "message": "Data updated successfully", "result": res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500