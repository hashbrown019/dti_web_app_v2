from datetime import date, datetime
import io
from flask import Blueprint, Response, render_template, request, session, redirect, jsonify, send_file, url_for
from flask_session import Session
import pandas as pd
import xlsxwriter
from modules.Connections import mysql, sqlite
import Configurations as c
import os
import json
import uuid
from werkzeug.utils import secure_filename

app = Blueprint("_micro", __name__, template_folder='pages')
rapid_mysql = mysql(*c.DB_CRED)

# --- Configuration for file uploads ---
UPLOAD_FOLDER = 'static/uploads/grievances' # Define your upload folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'} # Allowed file extensions

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class _main:
    def __init__(self, arg):
        super(_main, self).__init__()
        self.arg = arg
#--dynamic insert------------------------------------------------------------------------------------------------
    @app.route("/insert/<TABLE>", methods=["POST", "GET"])
    def insert(TABLE):
        coloumn = ""
        values = ""

        if TABLE == 'grievance' and 'grievance_image' in request.files:
            file = request.files['grievance_image']
            if file and allowed_file(file.filename):
                ext = os.path.splitext(file.filename)[1]
                filename = f"{uuid.uuid4()}{ext}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                coloumn += ",`grievance_image`"
                values += f",'{url_for('static', filename=f'uploads/grievances/{filename}')}'"
            else:
                return jsonify({"status": "error", "message": "Invalid file type or no file selected"}), 400

        for ids in request.form:
            coloumn += f",`{ids}`"
            values += f",'{request.form[ids]}'"

        if TABLE == 'grievance' and 'created_by' not in request.form and 'USER_DATA' in session:
            coloumn += ",`created_by`"
            values += f",'{session['USER_DATA'][0]['id']}'"

        res = rapid_mysql.do(f"INSERT {TABLE} ({coloumn[1:]}) VALUES ({values[1:]})")

        if res:
            return jsonify({"status": "success", "message": "Data inserted successfully", "result": res})
        else:
            return jsonify({"status": "error", "message": "Failed to insert data", "result": res}), 500

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
                "TotalSales": "ST_totalsales",
                "addressFO": "ST_address_fo",
                "productType": "ST_product_type",
                "vs": "ST_vol_supplied",
                "aveP": "ST_ave_price",
                "totalTransaction": "ST_total_transaction",
                "incentives": "ST_incentives_provided",
                "date": "ST_date",
            }
            columns = ["`upload_by`"]
            values = [f"'{session['USER_DATA'][0]['id']}'"]  # Add the current user's ID to the upload_by column
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
            query = f"SELECT * FROM grievance WHERE id = {int(record_id)}"
        else:
            query = "SELECT * FROM grievance"
        grievance_data = rapid_mysql.select(query)
        if record_id and not grievance_data:
            return jsonify({"status": "error", "message": "Record not found"}), 404
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
        update_fields = []
        
        # Handle file upload if present
        if 'grievance_image' in request.files:
            file = request.files['grievance_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                update_fields.append(f"`grievance_image` = '{url_for('static', filename=f'uploads/grievances/{filename}')}'")
            elif file.filename == '': # No new file selected, but the input was present
                pass # Do nothing, keep existing image path
            else:
                return jsonify({"status": "error", "message": "Invalid file type"}), 400
        
        # Process other form data
        for key, value in request.form.items():
            # Exclude the file input from this loop if already handled
            if key == 'grievance_image':
                continue
            update_fields.append(f"`{key}` = '{value}'")
        
        # Add date_modified and created_by for update
        update_fields.append(f"`date_modified` = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")
        if 'USER_DATA' in session:
            update_fields.append(f"`created_by` = '{session['USER_DATA'][0]['id']}'")


        if not update_fields:
            return jsonify({"status": "error", "message": "No data provided for update"}), 400

        query = f"UPDATE grievance SET {', '.join(update_fields)} WHERE Id = {id}"
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

@app.route('/export_grievance_data', methods=['GET'])
@c.login_auth_web()
def export_grievance_data():
    headers = [
        "ID", "Complainant", "Beneficiary", "Organization", "Phone Number", "EMAIL", "DIP Name", "Gender", "Age", "Sector",
        "Implementing Unit", "Address", "Mailing Address", "Guidance", "Confidential Means of Reception", "Confidential Identity", "Confidential Reason", "Raised Date",
        "Project Concern", "Staff Name", "Position", "Staff Contact", "Staff Implementing Unit", "Delegated Staff Name", 
        "Delegated Staff Implementing Unit", "Fact Finding Results", "Appeals",
        "Settlement", "Status", "Timestamp Created", "Timestamp Modified", "Created By", "Document Path" # Added Document Path
    ]
    user = session["USER_DATA"][0]
    user_id = user.get("id")
    user_type = user.get("type", "")
    # If admin or assign person (id==1), export all, else only user's data
    if str(user_id) == "1" or user_type.lower() == "admin":
        query = (
            "SELECT g.`id`, g.`complainant_1_fullname`, g.`complainant_1_beneficiary_category`, g.`complainant_1_organization`, "
            "g.`complainant_1_phone`, g.`complainant_1_email`, g.`complainant_1_dip_name`, g.`complainant_1_gender`, "
            "g.`complainant_1_age`, g.`complainant_1_sector`, g.`complainant_1_implementing_unit`, g.`complainant_1_address`, "
            "g.`complainant_1_mailing_address`, g.`complainant_1_additional_guidance`, g.`confidentiality_means_of_reception`, g.`confidentiality_identity`, "
            "g.`confidentiality_reason`, g.`complaint_raised_date`, g.`project_concern_description`, g.`staff_name`, "
            "g.`staff_position`, g.`staff_contact`, g.`staff_implementing_unit`, "
            "g.`delegated_staff_name`, g.`delegated_implementing_unit`, g.`fact_finding_results`, g.`appeals`, g.`settlement`, "
            "g.`grievance_status`, g.`date_created`, g.`date_modified`, u.`name` as `created_by`, g.`grievance_image` " # Added grievance_image
            "FROM grievance g "
            "INNER JOIN users u ON g.`created_by` = u.`id`"
        )
    else:
        query = (
            "SELECT g.`id`, g.`complainant_1_fullname`, g.`complainant_1_beneficiary_category`, g.`complainant_1_organization`, "
            "g.`complainant_1_phone`, g.`complainant_1_email`, g.`complainant_1_dip_name`, g.`complainant_1_gender`, "
            "g.`complainant_1_age`, g.`complainant_1_sector`, g.`complainant_1_implementing_unit`, g.`complainant_1_address`, "
            "g.`complainant_1_mailing_address`, g.`complainant_1_additional_guidance`, g.`confidentiality_means_of_reception`, "
            "g.`confidentiality_identity`, g.`confidentiality_reason`, g.`complaint_raised_date`, g.`project_concern_description`, "
            "g.`staff_name`, g.`staff_position`, g.`staff_contact`, g.`staff_implementing_unit`, "
            "g.`delegated_staff_name`, g.`delegated_implementing_unit`, g.`fact_finding_results`, g.`appeals`, g.`settlement`, "
            "g.`grievance_status`, g.`date_created`, g.`date_modified`, u.`name` as `created_by`, g.`grievance_image` " # Added grievance_image
            "FROM grievance g "
            "INNER JOIN users u ON g.`created_by` = u.`id` "
            f"WHERE g.`created_by` = {int(user_id)}"
        )
    data = rapid_mysql.select(query)
    df = pd.DataFrame(data)
    if not df.empty:
        # Ensure the number of columns matches the number of headers
        if len(df.columns) > len(headers):
            df = df.iloc[:, :len(headers)]
        elif len(df.columns) < len(headers):
            df.columns = headers[:len(df.columns)]
        else:
            df.columns = headers
        df = df.astype(str).replace({'NaT': '', 'nan': '', 'None': ''})
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet('Grievance')
    header_format = workbook.add_format({
        'bold': True, 'text_wrap': True, 'valign': 'vcenter', 'align': 'center',
        'fg_color': '#00cc66', 'border': 1
    })
    for col_num, header_text in enumerate(headers):
        worksheet.write(0, col_num, header_text, header_format)
    for row_num, row in enumerate(df.itertuples(index=False, name=None), 1):
        for col_num, cell_value in enumerate(row):
            worksheet.write(row_num, col_num, str(cell_value) if cell_value not in [None, 'NaT', 'nan'] else "")
    for idx, col in enumerate(headers):
        header_length = len(str(col)) + 2
        if not df.empty:
            data_max_length = df.iloc[:, idx].astype(str).apply(len).max()
        else:
            data_max_length = 0
        max_len = min(max(header_length, data_max_length), 40)
        worksheet.set_column(idx, idx, max_len)
    workbook.close()
    output.seek(0)
    return send_file(output, download_name="grievance_export.xlsx", as_attachment=True)

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
            "nameSTID": "ST_id",
            "nameID": "CPA_id",
            "nameRCU": "ST_rcu",
            "namePCU": "ST_pcu",
            "nameCOMMODITY": "ST_commodity",
            "nameDIP": "ST_nameofdip",
            "nameFO": "ST_nameof_fo",
            "TotalSales": "ST_totalsales",
            "af-msme": "ST_af_msme",
            "addressFO": "ST_address_fo",
            "productType": "ST_product_type",
            "vs": "ST_vol_supplied",
            "aveP": "ST_ave_price",
            "totalTransaction": "ST_total_transaction",
            "incentives": "ST_incentives_provided",
            "date": "ST_date",
        }
        # Add the current user's ID to the `upload_by` column
        update_fields = [f"`upload_by` = '{session['USER_DATA'][0]['id']}'"]

        # Map form fields to database columns
        for form_field, db_column in field_mapping.items():
            if form_field in request.form:
                update_fields.append(f"`{db_column}` = '{request.form[form_field]}'")
        if not update_fields:
            return jsonify({"status": "error", "message": "No valid data provided"}), 400

        # Construct the SQL UPDATE query
        query = f"UPDATE `sales_tracker` SET {', '.join(update_fields)} WHERE `ST_id` = {st_id}"
        res = rapid_mysql.do(query)
        return jsonify({"status": "success", "message": "Data updated successfully", "result": res})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route("/get_salesT_data")
@c.login_auth_web()
def get_salesT_data():
    try:
        record_id = request.args.get('id') 
        if record_id:
            query = f"SELECT * FROM sales_tracker WHERE Id = {record_id}"
        else:
            query = "SELECT * FROM sales_tracker"
        sales_data = rapid_mysql.select(query)
        if record_id and not sales_data:
            return jsonify({"status": "error", "message": "No data found for the given ID"}), 404
        return jsonify(sales_data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
#PROFILING FORM A------------------------------------------------------------------------------------------------
@app.route('/export_form_a', methods=['GET'])
@c.login_auth_web()
def export_form_a():
    query = ('''SELECT
            `excel_import_form_a`.`id`,
            `excel_import_form_a`.`user_id`,
            `excel_import_form_a`.`DEV_@_ID_@_ID`,
            CONCAT(
                `excel_import_form_a`.`frmer_prof_@_basic_Info_@_First_name`, ' ',
                `excel_import_form_a`.`frmer_prof_@_basic_Info_@_Middle_name`, ' ',
                `excel_import_form_a`.`frmer_prof_@_basic_Info_@_Last_name`, ' ',
                `excel_import_form_a`.`frmer_prof_@_basic_Info_@_Extension_name`
            ) AS full_name,
            `excel_import_form_a`.`frmer_prof_@_basic_Info_@_Sex`,
            `excel_import_form_a`.`frmer_prof_@_basic_Info_@_Mobile_number`,
            `excel_import_form_a`.`frmer_prof_@_basic_Info_@_email_address`,
            `excel_import_form_a`.`frmer_prof_@_basic_Info_@_birthday`,
            `excel_import_form_a`.`frmer_prof_@_basic_Info_@_bday_not_sure`,
            `excel_import_form_a`.`frmer_prof_@_basic_Info_@_civil_status`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_is_head_og_household`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_name_head_household`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_head_hh_name`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_head_hh_relationship`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_head_hh_sex`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_head_hh_pwd`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_head_hh_ofw`,
            `excel_import_form_a`.`frmer_prof_@_hh_Head_Info_@_head_hh_ip`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_longitude`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_latitude`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_region`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_province`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_city_municipality`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_brgy`,
            `excel_import_form_a`.`frmer_prof_@_frmer_addr_@_purok_sitio_street`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_primary_crop`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_DIP_name`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_Farmer_pwd`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_Farmer_ofw`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_farmer_ip`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_years_farming`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_Name_coop`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_position_in_coop`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_coop_mem_since`,
            `excel_import_form_a`.`frmer_prof_@_Farming_Basic_Info_@_is_listed_in_RSBSA`,
            `excel_import_form_a`.`frmer_prof_@_educ_@_highest_educational_attainment`,
            `excel_import_form_a`.`frmer_prof_@_educ_@_Vocational_Skills`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_Longitude`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_Latitude`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_region`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_province`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_municipality`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_Brgy`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_street_purok_sitio`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_declared_area_Ha`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_is_intercroping`,
            `excel_import_form_a`.`farm_info@_Farm_Basic_Info_@_Primary_crop`,
            `excel_import_form_a`.`farm_info@_Topography_@_slop_area_in_ha_greater_18_degrees`,
            `excel_import_form_a`.`farm_info@_Topography_@_flat_lain_area_in_hectares`,
            `excel_import_form_a`.`farm_info@_Trees_@_No_bearing_trees_planted`,
            `excel_import_form_a`.`farm_info@_Trees_@_No_bearing_non_trees_planted`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_Sole_ownership`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_co_ownership`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_CLOA_individual_EP`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_stewardship`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_usufruct`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_tenancy`,
            `excel_import_form_a`.`farm_info@_Land_Tenurial_Status_in_Ha_@_others`,
            `excel_import_form_a`.`farm_info@_Primary_Crop_Info_@_Ave_Prod_vol_w018_2019_kg_cycle`,
            `excel_import_form_a`.`farm_info@_Primary_Crop_Info_@_Crop_total_land_area_covered_Ha`,
            `excel_import_form_a`.`farm_info@_Primary_Crop_Info_@_Crop_No_Cycle_`,
            `excel_import_form_a`.`farm_info@_Secondary_Crop_Info_@_Secondary_Crop_if_Any`,
            `excel_import_form_a`.`farm_info@_Secondary_Crop_Info_@_Ave_Prod_vol_w018_2019_kg_cycle`,
            `excel_import_form_a`.`farm_info@_Secondary_Crop_Info_@_Crop_total_land_area_covered_Ha`,
            `excel_import_form_a`.`farm_info@_Secondary_Crop_Info_@_Crop_No_Cycle_`,
            `excel_import_form_a`.`farm_info@_Area_land_for_Expansion_@_Sloping_`,
            `excel_import_form_a`.`farm_info@_Area_land_for_Expansion_@_Flat_Plain`,
            `excel_import_form_a`.`farm_info@_area_land_for_rehabilitation_@_Sloping`,
            `excel_import_form_a`.`farm_info@_area_land_for_rehabilitation_@_flat_plain`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_0_14_per_Gender_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_0_14_per_Gender_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_15_30_per_Gender_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_15_30_per_Gender_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_31_59_per_Gender_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_31_59_per_Gender_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_60_above_per_Gender_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_HH_mem_Age_60_above_per_Gender_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_PWD_HH_Mem_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_PWD_HH_Mem_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_OFW_HH_Mem_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_OFW_HH_Mem_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_PWD_IP_Mem_@_No_Male`,
            `excel_import_form_a`.`farm_info@_num_PWD_IP_Mem_@_no_Female`,
            `excel_import_form_a`.`farm_info@_num_PWD_IP_Mem_@_List_IP_in_HH`,
            `excel_import_form_a`.`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Primary_Crop_`,
            `excel_import_form_a`.`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Secondary_Crop_`,
            `excel_import_form_a`.`farm_info@_hh_Income_Farm_@_Est_year_Income_Php_Lvstock_Fish_etc`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_fam_Remittnaces`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_Employment`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_Skilled_Labor`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_Business`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_Social_Pension`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_Pantawid_Beneficary`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_Other_Subsidies`,
            `excel_import_form_a`.`farm_info@_Household_Income_Non_Farming_@_If_Others_specify`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Farmer_farm_info_@_Does_Farmer_Keep_Records`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Farmer_farm_info_@_Crop_Cycle_Per_year`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Labor_Cost_P_Cycle_@_Land_Dev_Prep`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Labor_Cost_P_Cycle_@_Crop_Maintenance_Acts`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Labor_Cost_P_Cycle_@_Crop_Harvesting`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Labor_Cost_P_Cycle_@_Post_Harvest_Acts`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Mtrls_inpts_P_Cyc_@_Land_Dev_Prep`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Mtrls_inpts_P_Cyc_@_Crop_Mntnce_Acts`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Mtrls_inpts_P_Cyc_@_Crop_Harvesting`,
            `excel_import_form_a`.`prod_Cost_Per_Crop_@_Mtrls_inpts_P_Cyc_@_Post_Harv_Acts`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_fam_Workers_@_Youth`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_fam_Workers_@_Senior_Citizen`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_fam_Workers_@_PWD`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_fam_Workers_@_OFW`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_fam_Workers_@_IP`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_fam_Workers_@_Youth`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_fam_Workers_@_Senior_Citizen`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_fam_Workers_@_PWD`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_fam_Workers_@_OFW`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_fam_Workers_@_IP`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_Non_fam_Workers_@_Youth`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_Non_fam_Workers_@_Senior_Citizen`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_Non_fam_Workers_@_PWD`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_Non_fam_Workers_@_OFW`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Male_Non_fam_Workers_@_IP`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_Non_fam_Workers_@_Youth`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_Non_fam_Workers_@_Sr_Citizen`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_Non_fam_Workers_@_PWD`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_Non_fam_Workers_@_OFW`,
            `excel_import_form_a`.`Workers_Laborers_@_num_Fem_Non_fam_Workers_@_IP`,
            `excel_import_form_a`.`Workers_Laborers_@_IP_WORKERS_@_IP_g_Present_fam_Workers`,
            `excel_import_form_a`.`Workers_Laborers_@_IP_WORKERS_@_IP_g_Present_NON_fam_Workers`,
            `excel_import_form_a`.`Workers_Laborers_@_Worker_Income_@_Male_fam_Income_Yearly`,
            `excel_import_form_a`.`Workers_Laborers_@_Worker_Income_@_Fem_fam_Income_Yearly`,
            `excel_import_form_a`.`Workers_Laborers_@_Worker_Income_@_Male_NON_fam_Income_Yearly`,
            `excel_import_form_a`.`Workers_Laborers_@_Worker_Income_@_Fem_NON_fam_Income_Yearly`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_@_Type_PH_Faci_Equipnt`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_@_Name_Equipnt_Faci`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_Addresses_@_Longitude`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_Addresses_@_Latitude`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_Addresses_@_Region`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_Addresses_@_Province`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_Addresses_@_City_Muni`,
            `excel_import_form_a`.`Post_Harv_@_PH_Faci_Equipnt_Addresses_@_st_prkk_sitio`,
            `excel_import_form_a`.`Post_Harv_@_PH_Prod_Out_@_PH_Product_Form`,
            `excel_import_form_a`.`Post_Harv_@_PH_Prod_Out_@_Cap_qty`,
            `excel_import_form_a`.`Post_Harv_@_PH_Prod_Out_@_Cap_unit_kg_metric_tons_sac_crate_box`,
            `excel_import_form_a`.`Post_Harv_@_PH_Prod_Out_@_Cap_Freq_hr_daymonth_year_cyc_harv`,
            `excel_import_form_a`.`Mrktng_Sales_@_Primary_crop_Prod_@_Primary_crop_Prod_Type`,
            `excel_import_form_a`.`Mrktng_Sales_@_Primary_crop_Prod_@_Primary_crop_Product_Dlvry`,
            `excel_import_form_a`.`Mrktng_Sales_@_Name_Primary_Crop_DistrPoint_@_Farmers_Org`,
            `excel_import_form_a`.`Mrktng_Sales_@_Name_Primary_Crop_DistrPoint_@_SME`,
            `excel_import_form_a`.`Mrktng_Sales_@_Name_Primary_Crop_DistrPoint_@_Anchor_Firm`,
            `excel_import_form_a`.`Mrktng_Sales_@_Name_Primary_Crop_DistrPoint_@_Negosyo_Center`,
            `excel_import_form_a`.`Mrktng_Sales_@_Name_Primary_Crop_DistrPoint_@_Others`,
            `excel_import_form_a`.`Mrktng_Sales_@_Mrkt_@_Payterms_Cnsgnmnt_Cash_Cred_Other`,
            `excel_import_form_a`.`Mrktng_Sales_@_Mrkt_@_Buyer_Type_Trdr_Conso_Processor_Other`,
            `excel_import_form_a`.`Mrktng_Sales_@_Mrkt_@_Farm_Gate_Price_FGP_on_Php`,
            `excel_import_form_a`.`Mrktng_Sales_@_Mrkt_@_Unit_Kg_Metric_tons_Sack_box`,
            `excel_import_form_a`.`Acs_to_Finc_@_Crop_Insurance_@_Crop_Insurance_yes_No`,
            `excel_import_form_a`.`Acs_to_Finc_@_Loan_Bank_@_Name_Govt_Bank_LBP_DBP_if_any`,
            `excel_import_form_a`.`Acs_to_Finc_@_Loan_Bank_@_Type_Loan`,
            `excel_import_form_a`.`Acs_to_Finc_@_Loan_Non_Bank_@_Name_Private_Bank_if_any`,
            `excel_import_form_a`.`Acs_to_Finc_@_Loan_Non_Bank_@_Type_Loan`,
            `excel_import_form_a`.`Acs_to_Finc_@_Loan_Others_@_Loan_Init_Rltives_Informal_Lndrs`,
            `excel_import_form_a`.`Acs_to_Finc_@_Loan_Others_@_Type_Loan`,
            `excel_import_form_a`.`Acs_to_Finc_@_Depo_@_Type_Depo_if_any`,
            `excel_import_form_a`.`Acs_to_Finc_@_Depo_@_Name_bank_if_the_FSP_is_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Depo_@_Name_non_bank_if_the_FSP_is_non_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Insurance_@_Type_Insurance_if_any`,
            `excel_import_form_a`.`Acs_to_Finc_@_Insurance_@_Name_bank_if_the_FSP_is_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Insurance_@_Name_non_bank_if_the_FSP_is_non_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Paymnts_Util_@_Type_Payments_if_any`,
            `excel_import_form_a`.`Acs_to_Finc_@_Paymnts_Util_@_Name_bank_if_the_FSP_is_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Paymnts_Util_@_Name_non_bank_if_FSP_is_non_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Remittances_OFW_@_Name_Non_Bank_FSP`,
            `excel_import_form_a`.`Acs_to_Finc_@_Others_@_Name_bank_if_the_FSP_is_Bank`,
            `excel_import_form_a`.`Acs_to_Finc_@_Others_@_Name_non_bank_if_the_FSP_is_non_Bank`,
            `excel_import_form_a`.`Competency_@_Core_@_num_Farm_Relate_Trainings_last_2_3_years`,
            `excel_import_form_a`.`Competency_@_Core_@_List_Value_Chain`,
            `excel_import_form_a`.`Competency_@_Core_@_Farm_Certification_Acquired_if_any`,
            `excel_import_form_a`.`Competency_@_src_info@_ls_Medium_source_information`,
            `excel_import_form_a`.`Competency_@_src_info@_ls_frequency_Medium_source_info_`,
            `excel_import_form_a`.`Competency_@_Others_@_Owns_what_Type_Mobile_Phone`,
            `excel_import_form_a`.`Competency_@_Others_@_Support_Needed_to_improve_farm_prodcvty`,
            `excel_import_form_a`.`Competency_@_Others_@_Farmer_Comments_about_Rapid`,
            `excel_import_form_a`.`Others_@_Others_@_Enumerator_Remarks`,
            `excel_import_form_a`.`Others_@_Others_@_Others_1`,
            `excel_import_form_a`.`Others_@_Others_@_Others_2`,
            `excel_import_form_a`.`Others_@_Others_@_Others_3`,
            `excel_import_form_a`.`Others_@_Others_@_Others_4`,
            `excel_import_form_a`.`Others_@_Others_@_Others_5`,
            `excel_import_form_a`.`Others_@_Others_@_Others_6`,
            `excel_import_form_a`.`v2_date_enum`,
            `excel_import_form_a`.`v2_name_enum`,
            `excel_import_form_a`.`v2_workers_total_fam_female`,
            `excel_import_form_a`.`v2_workers_total_fam_male`,
            `excel_import_form_a`.`v2_workers_total_nonfam_female`,
            `excel_import_form_a`.`v2_workers_total_nonfam_male`,
            `excel_import_form_a`.`v2_access_crop_insur_name_fsp_access`,
            `excel_import_form_a`.`v2_interv_capbuild`,
            `excel_import_form_a`.`v2_interv_expansion`,
            `excel_import_form_a`.`v2_interv_rehab`,
            `excel_import_form_a`.`v2_interv_prod_inv`,
            `excel_import_form_a`.`v2_interv_fmi`,
            `excel_import_form_a`.`file_name`,
            `users`.`name` AS 'Uploaded By'
        FROM excel_import_form_a
        LEFT JOIN users ON `excel_import_form_a`.`user_id` = `users`.`id`
    ''')

    headers = [
        "ID", "User ID", "DEV @ ID @ ID", "Full Name", "Sex",
        "Mobile Number", "Email Address", "Birthday", "Birthday Not Sure",
        "Civil Status", "Is Head of Household", "Name of Household Head",
        "Head HH Name", "Head HH Relationship", "Head HH Sex", "Head HH PWD",
        "Head HH OFW", "Head HH IP", "Longitude", "Latitude", "Region", "Province",
        "City/Municipality", "Barangay", "Purok/Sitio/Street", "Primary Crop",
        "DIP Name", "Farmer PWD", "Farmer OFW", "Farmer IP", "Years Farming",
        "Name Coop", "Position in Coop", "Coop Mem Since", "Is Listed in RSBSA",
        "Highest Educational Attainment", "Vocational Skills", "Farm Longitude",
        "Farm Latitude", "Farm Region", "Farm Province", "Farm Municipality",
        "Farm Barangay", "Farm Street/Purok/Sitio", "Declared Area (Ha)",
        "Is Intercropping", "Primary Crop", "Slope Area (>18 Degrees) (Ha)",
        "Flat Plain Area (Ha)", "No Bearing Trees Planted", "No Bearing Non-Trees",
        "Land Tenure - Sole Ownership", "Land Tenure - Co-Ownership",
        "Land Tenure - CLOA Individual EP", "Land Tenure - Stewardship",
        "Land Tenure - Usufruct", "Land Tenure - Tenancy", "Land Tenure - Others",
        "Primary Crop Avg Prod Vol 2018-2019 (kg/cycle)", "Primary Crop Land Area Covered (Ha)",
        "Primary Crop No Cycle", "Secondary Crop", "Secondary Crop Avg Prod Vol 2018-2019",
        "Secondary Crop Land Area Covered (Ha)", "Secondary Crop No Cycle",
        "Area for Expansion - Sloping", "Area for Expansion - Flat Plain",
        "Area for Rehabilitation - Sloping", "Area for Rehabilitation - Flat Plain",
        "HH Members Age 0-14 Male", "HH Members Age 0-14 Female",
        "HH Members Age 15-30 Male", "HH Members Age 15-30 Female",
        "HH Members Age 31-59 Male", "HH Members Age 31-59 Female",
        "HH Members Age 60+ Male", "HH Members Age 60+ Female",
        "PWD HH Members Male", "PWD HH Members Female",
        "OFW HH Members Male", "OFW HH Members Female",
        "PWD/IP HH Members Male", "PWD/IP HH Members Female", "List IP in HH",
        "Farm Income Primary Crop (PHP)", "Farm Income Secondary Crop (PHP)",
        "Livestock/Fish Income (PHP)", "Family Remittances", "Employment Income",
        "Skilled Labor Income", "Business Income", "Social Pension",
        "Pantawid Beneficiary", "Other Subsidies", "Other Subsidies Specify",
        "Farmer Keeps Records", "Crop Cycle per Year", "Land Dev Prep Labor Cost",
        "Crop Maintenance Labor Cost", "Harvesting Labor Cost", "Post Harvest Labor Cost",
        "Land Dev Prep Materials Cost", "Crop Maintenance Materials Cost",
        "Harvesting Materials Cost", "Post Harvest Materials Cost",
        "Male Family Workers Youth", "Male Family Workers Senior Citizen",
        "Male Family Workers PWD", "Male Family Workers OFW", "Male Family Workers IP",
        "Female Family Workers Youth", "Female Family Workers Senior Citizen",
        "Female Family Workers PWD", "Female Family Workers OFW", "Female Family Workers IP",
        "Male Non-Family Workers Youth", "Male Non-Family Workers Senior Citizen",
        "Male Non-Family Workers PWD", "Male Non-Family Workers OFW", "Male Non-Family Workers IP",
        "Female Non-Family Workers Youth", "Female Non-Family Workers Senior Citizen",
        "Female Non-Family Workers PWD", "Female Non-Family Workers OFW", "Female Non-Family Workers IP",
        "IP Present in Family Workers", "IP Present in Non-Family Workers",
        "Male Family Worker Income Yearly", "Female Family Worker Income Yearly",
        "Male Non-Family Worker Income Yearly", "Female Non-Family Worker Income Yearly",
        "PH Facility Type", "PH Equipment Name", "PH Facility Longitude",
        "PH Facility Latitude", "PH Facility Region", "PH Facility Province",
        "PH Facility City/Municipality", "PH Facility Street/Purok/Sitio",
        "PH Product Form", "PH Capacity Quantity", "PH Capacity Unit",
        "PH Capacity Frequency", "Sales Product Type", "Sales Product Delivery",
        "Distribution Point - Farmers Org", "Distribution Point - SME",
        "Distribution Point - Anchor Firm", "Distribution Point - Negosyo Center",
        "Distribution Point - Others", "Payment Terms", "Buyer Type",
        "Farm Gate Price (PHP)", "Unit of Measure", "Crop Insurance",
        "Loan Bank - Govt Bank Name", "Loan Bank - Loan Type",
        "Loan Non-Bank - Private Bank Name", "Loan Non-Bank - Loan Type",
        "Loan Others - Informal Lenders", "Loan Others - Loan Type",
        "Deposit Type", "Deposit Bank Name", "Deposit Non-Bank Name",
        "Insurance Type", "Insurance Bank Name", "Insurance Non-Bank Name",
        "Payments Util Type", "Payments Util Bank Name", "Payments Util Non-Bank Name",
        "OFW Remittance FSP", "Others Bank Name", "Others Non-Bank Name",
        "Number of Trainings Last 2-3 Years", "List Value Chain",
        "Farm Certification Acquired", "Source Medium Info",
        "Source Medium Frequency", "Mobile Phone Type",
        "Support Needed to Improve Productivity", "Farmer Comments about RAPID",
        "Enumerator Remarks", "Others 1", "Others 2", "Others 3", "Others 4", "Others 5", "Others 6",
        "Date Enumerated", "Enumerator Name", "Total Fam Female", "Total Fam Male",
        "Total Non-Fam Female", "Total Non-Fam Male", "Access Crop Insurer Name",
        "Intervention - Capacity Building", "Intervention - Expansion",
        "Intervention - Rehabilitation", "Intervention - Production Investment",
        "Intervention - FMI", "File Name", "Uploaded By"
    ]
    def generate_excel_data():
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'constant_memory': True})
        worksheet = workbook.add_worksheet('dcf_form_a_exported_file')
        header_format = workbook.add_format({
            'bold': True,'text_wrap': True,'valign': 'vcenter','align': 'center','fg_color': '#00cc66','border': 1
        })
        for col_num, header_text in enumerate(headers):
            worksheet.write(0, col_num, header_text, header_format)
        offset = 0
        chunk_size = 1000
        row_num = 1
        adaptive_chunk = True 
        while True:
            try:
                query_with_limit = query + f" LIMIT {chunk_size} OFFSET {offset}"
                data_chunk = rapid_mysql.select(query_with_limit)
                if not data_chunk:
                    break
                df_chunk = pd.DataFrame(data_chunk)
                num_columns_in_df = len(df_chunk.columns)
                num_expected_headers = len(headers)

                if num_columns_in_df != num_expected_headers:
                    print(
                        f"Column count mismatch! DataFrame has {num_columns_in_df} columns, expected {num_expected_headers}."
                    )
                    if num_columns_in_df > num_expected_headers:
                        df_chunk = df_chunk.iloc[:, :num_expected_headers]
                    elif num_columns_in_df < num_expected_headers:
                        local_headers = headers[:num_columns_in_df]
                        df_chunk.columns = local_headers
                    else:
                        df_chunk.columns = headers
                else:
                    df_chunk.columns = headers
                for row_data in df_chunk.itertuples(index=False, name=None):
                    for col_num, cell_value in enumerate(row_data):
                        worksheet.write(row_num, col_num, cell_value)
                    row_num += 1
                for idx, col in enumerate(df_chunk.columns):
                    header_length = len(str(col)) + 2
                    series = df_chunk[col].astype(str)
                    data_max_length = series.apply(len).max()
                    max_len = min(max(header_length, data_max_length), 40) 
                    worksheet.set_column(idx, idx, max_len)
                offset += chunk_size
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)
                if adaptive_chunk:
                    if len(df_chunk) < 100 and chunk_size > 500: 
                        chunk_size -= 100
                        print(f"Decreasing chunk size to {chunk_size}")
                    elif len(df_chunk) > 900 and chunk_size < 3000:  
                        chunk_size += 100
                        print(f"Increasing chunk size to {chunk_size}")
            except Exception as e:
                print(f"Error during Excel data generation: {e}")
                yield f"Error: {e}".encode()
                break

        workbook.close()
        yield output.getvalue()
    def generate_response():
        try:
            return Response(
                generate_excel_data(),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers={'Content-Disposition': 'attachment; filename=dcf_form_a_exported_file.xlsx'}
            )
        except Exception as e:
            print(f"Error creating response: {e}")
            return "An error occurred while generating the Excel file.", 500 
    return generate_response()