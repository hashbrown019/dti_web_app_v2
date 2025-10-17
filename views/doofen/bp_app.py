from datetime import date, datetime
from flask import Blueprint, render_template, request, session, redirect, jsonify, Response, send_file
from flask_session import Session
import xlsxwriter
from modules.Connections import mysql,sqlite
from modules.Req_Brorn_util import string_websafe
import Configurations as c
import os, random, json, shutil, base64, sys, warnings, csv, xlrd
from controllers.outbound import outbound as outb
from controllers.inbound import inbound as inb
from controllers.inbound import data_cleaning as  d_c
from werkzeug.utils import secure_filename
from controllers.engine_excel_to_sql import form_excel_a_handler
import os, random, json
import pandas as pd
import openpyxl
from datetime import datetime
import pandas as pd
from tqdm import tqdm

app = Blueprint("doofen",__name__,template_folder='pages')

_excel = form_excel_a_handler(__name__)
rapid_mysql = mysql(*c.DB_CRED)

outbound = outb(app,rapid_mysql,session)
inbound = inb(app,rapid_mysql,session)
data_clean = d_c(app,rapid_mysql,session)
record_counter = 0
# app = Flask(__name__)
	
@app.route("/formb")
@c.login_auth_web()
def index():
	return redirect("/formb/dashboard")
	
@app.route("/formb/dashboard")
@c.login_auth_web()
def dashboard():
	return dashboardv2()
	# return render_template('index.html',USER_DATA=session["USER_DATA"][0],num_fo_sex=get_num_fo_sex())

@app.route("/formbembed/e",methods=["GET"])
@c.login_auth_web()
def embed():
	return render_template('embed_b.html',page=request.args['page'],USER_DATA=session["USER_DATA"][0],num_fo_sex=get_num_fo_sex())

@app.route("/formb/dashboardv2")
@c.login_auth_web()
def dashboardv2():
	return render_template('dashboard_main.html',USER_DATA=session["USER_DATA"][0],num_fo_sex=get_num_fo_sex())

@app.route('/set_data_b/<table>', methods=['POST'])
@c.login_auth_web()
def set_data_b(table):
    # Grab everything at the start
    form_data = request.form.to_dict(flat=True)
    print("===> incoming form_data:", form_data)

    rec_id = form_data.pop("id", "").strip()
    # Remove keys with empty column names
    form_data = {k: v.strip() for k, v in form_data.items() if k.strip() != ""}

    col = ""
    val = ""
    args = ""

    if rec_id == "":  # INSERT
        for k, v in form_data.items():
            col += ",`{}`".format(k)
            val += ",'{}'".format(v.replace("'", "''"))
        sql = "INSERT INTO `{}` (`uploaded_by`{}) VALUES ('{}'{})".format(
            table, col, session["USER_DATA"][0]["id"], val
        )
    else:  # UPDATE
        for k, v in form_data.items():
            args += ",`{}`='{}'".format(k, v.replace("'", "''"))
        sql = "UPDATE `{}` SET {} ,date_modified=CURRENT_TIMESTAMP WHERE `id`='{}';".format(
            table, args[1:], rec_id
        )

    result = rapid_mysql.do(sql)
    if isinstance(result, dict) and result.get('response') == 'error':
        status = 'failed'
        msg = result.get('message')
        last_row_id = None
    else:
        status = 'success'
        msg = 'Data was added to the database'
        last_row_id = result

    return jsonify({"status": status, "msg": msg, "id": last_row_id})

@app.route("/formb/get_list_fo",methods=["POST","GET"])
@c.login_auth_web()
def get_list_fo():
	sql_form = '''
	SELECT 
		`form_b`.`id` as 'db_id',
		`form_b`.`organization_registered_name`,
		`form_b`.`office_business_adrress`,
		`form_b`.`types_of_organization`,
		`form_b`.`registering_agencies`,
		`users`.`name` as 'inputed_by',
		`users`.`rcu` as 'rcu'
	FROM `form_b` 
	INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
	ORDER BY `form_b`.`id` DESC;'''.format(Filter.position_data_filter())
	resp = rapid_mysql.select(sql_form,False)
	return resp

@app.route("/formb/get_num_fo_sex",methods=["POST","GET"])
@c.login_auth_web()
def get_num_fo_sex():
    sql_form_gender = '''
    SELECT 
        SUM(CASE WHEN `form_b`.`respondents_gender` = 'Male' THEN 1 ELSE 0 END) AS male,
        SUM(CASE WHEN `form_b`.`respondents_gender` = 'Female' THEN 1 ELSE 0 END) AS female
    FROM `form_b`
    INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id`
    {};
    '''.format(Filter.position_data_filter())

    gender_stats = rapid_mysql.select(sql_form_gender, True)[0]

    male = int(gender_stats['male'] or 0)
    female = int(gender_stats['female'] or 0)

    sql_form_mngmnt = '''
        SELECT 
            SUM(CASE WHEN respondents_gender = 'Male' THEN 1 ELSE 0 END) AS total_male_mngmnt,
            SUM(CASE WHEN respondents_gender = 'Female' THEN 1 ELSE 0 END) AS total_female_mngmnt
        FROM `form_b`
            INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id`
            WHERE respondents_designation_in_the_organization IS NOT NULL
            AND TRIM(respondents_designation_in_the_organization) <> ''
            AND UPPER(TRIM(respondents_designation_in_the_organization)) <> 'N/A'
    {};'''.format(Filter.position_data_filter().replace('WHERE', 'AND', 1))

    mngmt_stats = rapid_mysql.select(sql_form_mngmnt, True)[0]
    mngmt_male = int(mngmt_stats.get('total_male_mngmnt') or 0)
    mngmt_female = int(mngmt_stats.get('total_female_mngmnt') or 0)

    sql_form_b_count = '''
    SELECT COUNT(*) as 'total_form_b'
    FROM `form_b` 
    INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} 
    ;'''.format(Filter.position_data_filter())
    total_form_b = rapid_mysql.select(sql_form_b_count,True)[0]['total_form_b']
    total_form_b = total_form_b if total_form_b not in ["null",None,"None"] else 0

    res = {
        "male":male,
        "female":female,
        'mngmt_male':int(str(mngmt_male).split(".")[0]),
        'mngmt_female':int(str(mngmt_female).split(".")[0]),
        'total_form_b': total_form_b
    }

    return res

@app.route("/download_excel/<excel_file>",methods=["POST","GET"])
@c.login_auth_web()
def download_excel(excel_file):
	# excel_file = request.form['file']
	# print(excel_file)
	def_name = excel_file.split("@@")[2]
	excel_file = excel_file.replace("@@","#")
	return send_file(c.RECORDS+"/objects/spreadsheets/migrated/"+excel_file, as_attachment=True,download_name=def_name)

@app.route("/download_excel_from_notif/<excel_file>",methods=["POST","GET"])
@c.login_auth_web()
def download_excel_from_notif(excel_file):
	return send_file(c.RECORDS+"/objects/spreadsheets/exports/"+excel_file, as_attachment=True,download_name=excel_file)

@app.route("/delete_excel_b", methods=["POST", "GET"])
@c.login_auth_web()
def delete_excel():
    excel_file = request.form['file']
    excel_file_db = excel_file.replace("@@", "#")
    shutil.move(
        os.path.join(c.RECORDS, "objects/spreadsheets/migrated", excel_file_db),
        os.path.join(c.RECORDS, "objects/spreadsheets/deleted", excel_file_db)
    )

    sql = "DELETE FROM `form_b` WHERE `filename`='{}';".format(excel_file_db)
    rapid_mysql.do(sql)
    return jsonify({"status": "done"})

    
@app.route("/by_app/get_uploaded_excel",methods=["POST","GET"])
@c.login_auth_web()
def by_app_get_uploaded_excel():
    _sql = """
        SELECT filename AS `key`, COUNT(filename) AS `total`
        FROM form_b
        WHERE uploaded_by = {}
        AND filename IS NOT NULL
        AND filename LIKE '%#%#%'  -- only real uploaded files
        GROUP BY filename;
    """.format(session["USER_DATA"][0]['id'])
    upld_excel = rapid_mysql.select(_sql)
    return upld_excel

@app.route("/excel_upload_b",methods=["POST","GET"])
@c.login_auth_web()
def excel_upload_b():
	today = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
	uploader = request.form['uploader']
	excel_ = request.files
	UPLOAD_NAME = "NONE"
	for excel in excel_:
		f = excel_[excel]
		UPLOAD_NAME = uploader+"#"+today+"#"+secure_filename(f.filename)
		f.save(os.path.join(c.RECORDS+"/objects/spreadsheets/queued/",UPLOAD_NAME ))
	uploadstate = excel_popu_individual_b(UPLOAD_NAME)
	return uploadstate

@app.route("/formb/get_list_fo_full", methods=["POST", "GET"])
@c.login_auth_web()
def get_list_fo_full():
    sql_form = '''
    SELECT 
        `form_b`.`id` as 'db_id',
        `form_b`.*,
        `users`.`name` as 'inputed_by',
        `users`.`rcu` as 'rcu'
    FROM `form_b` 
    INNER JOIN `users` ON `form_b`.`uploaded_by` = `users`.`id` {} ;'''.format(Filter.position_data_filter())
    resp = rapid_mysql.select(sql_form)
    df_nested_list = pd.json_normalize(resp)
    df = pd.DataFrame(df_nested_list)
    file_path = c.RECORDS + "objects/spreadsheets_b/exported/formb.xlsx"
    writer = pd.ExcelWriter(file_path, engine='xlsxwriter') 
    df.to_excel(writer, sheet_name='Form B Data', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Form B Data']
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'fg_color': '#00cc66',
        'border': 1
    })
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        column_width = max(df[value].astype(str).map(len).max(), len(value))
        worksheet.set_column(col_num, col_num, column_width)
    writer.close()
    file_name_exported = "formb.xlsx"
    return send_file(file_path, as_attachment=True, download_name=file_name_exported)
# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================
def create_excel(DATA,path,formname):
	print(" Using Dynamic Function")
	DATE_NOW = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
	USER_ID = session["USER_DATA"][0]["id"]
	# dict_= json.loads(res)
	# df_nested_list = pd.DataFrame.from_dict(DATA, orient="index")
	print(" *  Generating DATA FRAME ")
	df_nested_list = pd.json_normalize(DATA)
	# print(res[0])
	# print(df_nested_list)
	print(" *  Writing to spreadsheet ")
	FILE_NAME_EXPORTED = '{}_{}_{}.xlsx'.format(USER_ID,formname,DATE_NOW)
	__TO_DL_EXCEL = path + FILE_NAME_EXPORTED
	print(f" *  Writing path [{__TO_DL_EXCEL}]")

	writer = pd.ExcelWriter(__TO_DL_EXCEL) 
	print(" *  Saving spreadsheet. . .  ")
	df_nested_list.to_excel(writer, sheet_name='mobile_imports',index=False )
	writer.save()
	print(" *  Saving spreadsheet DOne ")
	return {"Status":"done","file_name":FILE_NAME_EXPORTED}
# ==============================================================
# ==============================================================
# ==============================================================
# ==============================================================
@app.route("/formb/get_ind_fo",methods=["POST","GET"])
@c.login_auth_web()
def get_ind_fo():
	ids = request.form['id']
	sql_form = "SELECT * FROM `form_b` WHERE `id`={};".format(ids)
	ind = rapid_mysql.select(sql_form)
	return jsonify(ind)

@app.route("/formb/delete_item",methods=["POST","GET"])
@c.login_auth_web()
def delete_item():
	ids = request.form['id']
	sql_form = "DELETE FROM `form_b` WHERE `id`={};".format(ids)
	ind = rapid_mysql.do(sql_form)
	return jsonify(ind)

@app.route("/formb/excel_upload",methods=["POST","GET"])
@c.login_auth_web()
def excel_upload():
	today = str(datetime.today()).replace("-","_").replace(" ","_").replace(":","_").replace(".","_")
	uploader = request.form['uploader']
	excel_ = request.files
	UPLOAD_NAME = "NONE"
	for excel in excel_:
		f = excel_[excel]
		UPLOAD_NAME = uploader+"#"+today+"#"+secure_filename(f.filename)
		f.save(os.path.join(c.RECORDS+"/objects/spreadsheets/queued/",UPLOAD_NAME ))
	uploadstate = excel_popu_individual_b(UPLOAD_NAME)
	return uploadstate

@app.route('/api/get_dip_names', methods=['GET'])
def get_dip_names():
    try:
        query = """
            SELECT form_1_name_dip, form_1_commodity 
            FROM dcf_prep_review_aprv_status 
            WHERE form_1_name_dip IS NOT NULL AND form_1_name_dip != '' 
            GROUP BY form_1_name_dip, form_1_commodity 
            ORDER BY form_1_name_dip ASC
        """
        result = rapid_mysql.select(query)
        dip_data = [dict(form_1_name_dip=row['form_1_name_dip'], form_1_commodity=row['form_1_commodity']) for row in result]
        return jsonify(dip_data)
    except Exception as e:
        print(f"Error fetching DIP names: {e}")
        return jsonify({"error": "Error fetching DIP names"}), 500

def get_all_uploaded_excel_data_f_b():
    return excel_popu_b()

def excel_popu_b():
    msg = "Unfinished"
    status = "Unfinished"
    record_counter = 0
    dir_path = c.RECORDS+"/objects/spreadsheets/queued/"
    FROM_EXCEL_RPOFILES = {}
    counter = 0
    for path in os.listdir(dir_path):
        PATH__ = os.path.join(dir_path, path)
        if os.path.isfile(PATH__):  
            fn_ = path.split(".")[len(path.split("."))-1]
            if(fn_ not in "._DELETED_FILE_"):
                file_name =  PATH__ 
                sheet =  "VC FORM B" 
                print("\n= Scanning [{}]".format(path))
                try:
                    resp = push_mysql_b(readRows(file_name, sheet),path)
                    if(resp["err"]):
                        msg = "Error in Moving to Database"
                        status = "failed"
                        return resp["msg"]
                    else:
                        move_to_done_files(path)
                        FROM_EXCEL_RPOFILES[resp["data"]["file"]] = resp["data"]["count"]
                        msg = "Moved to Database"
                        status = "success"
                    counter = counter + 1
                except Exception as e:
                    if("No sheet named <'VC FORM B'>" in str(e)):
                        print("  --- ERROR in XLRD Parser (ignoring file [{}]) || {}".format(path,e))
                        move_to_failed_files(path)
                        msg = "No <'VC FORM B'> Found"
                        status = "failed"
                    elif("Unsupported format, or corrupt file" in str(e)):
                        print("  --- ERROR in XLRD Parser (ignoring file [{}]) || {}".format(path,e))
                        move_to_failed_files(path)
                        msg = "Corrupt File \n {e}"
                        status = "failed"
                    else:
                        raise e
    return {"status":status,"msg":msg,"success_files":FROM_EXCEL_RPOFILES}

def excel_popu_individual_b(_NAME_):
    msg = "Unfinished"
    status = "Unfinished"
    record_counter = 0
    dir_path = c.RECORDS+"/objects/spreadsheets/queued/"
    FROM_EXCEL_RPOFILES = {}
    counter = 0
    PATH__ = os.path.join(dir_path, _NAME_)
    data = None  
    if os.path.isfile(PATH__):
        file_name = PATH__
        sheet =  "VC FORM B" 
        print("\n= Scanning [{}]".format(_NAME_))
        try:
            rows = readRows(file_name, sheet)
            resp = push_mysql_b(rows, _NAME_)
            move_to_done_files(_NAME_)
            data = resp
            msg = "Transaction finished. Please be patient as the data uploaded will take time to display in the list or in the dashboard."
            status = "success"
            counter = counter + 1
        except Exception as e:
            data = "none" 
            msg = "[{}]".format(e)
            status = "failed"
            print(e)
    print(" * Done excel process")
    return {"status":status,"msg":msg,"success_files":FROM_EXCEL_RPOFILES,"data":data}

def push_mysql_b(rows, uploaded_by):
    excel_b_heads = get_all_uploaded_excel_data_heads_b()  # no uploaded_by or filename here
    err = False
    RESP = "None"

    CONN = rapid_mysql.db_ready()
    inserted_count = 0
    loads_ = tqdm(range(len(rows)))
    ret_data = {"file": uploaded_by, "count": 0}

    for row_num in loads_:
        try:
            row = rows[row_num]
            if not isinstance(row, (list, tuple)):
                row = list(row)
            first_cell = str(row[0]).strip() if len(row) > 0 else ""
            if first_cell in ["", " ", "None", "nan", "NaN"]:
                continue

            max_cols = min(len(excel_b_heads), len(row))
            fields = []
            vals = []

            for idx in range(max_cols):
                head = excel_b_heads[idx].strip()
                val = row[idx]
                s = str(val).replace("\\", "").replace("'", "''").replace('"', "")
                fields.append(f"`{head}`")
                vals.append(f"'{s}'")

            if not fields:
                continue

            fields_sql = ",".join(fields)
            vals_sql = ",".join(vals)

            uploader_id = uploaded_by.split("#")[0] if "#" in uploaded_by else uploaded_by
            filename_db = uploaded_by  

            sql = (
                f"INSERT INTO `form_b` (`uploaded_by`,`filename`,{fields_sql}) "
                f"VALUES ('{uploader_id}','{filename_db}',{vals_sql});"
            )

            resp = rapid_mysql.do_(sql, CONN)
            loads_.desc = f" -FileData[{inserted_count+1}] file[{uploaded_by}]"
            inserted_count += 1

            if isinstance(resp, dict) and "response" in resp:
                err = True
                RESP = resp
                break

        except Exception as e:
            print(f"[push_mysql_b] Error inserting row #{row_num}: {e}")
            print("Row content:", row)
            err = True
            RESP = {"error": str(e), "row_num": row_num, "row": row}
            break

    try:
        CONN.commit()
    except Exception as e:
        print("[push_mysql_b] commit error:", e)
        err = True
        RESP = {"error": str(e)}

    ret_data["count"] = inserted_count
    return {"err": err, "msg": RESP, "data": ret_data}

def get_all_uploaded_excel_data_heads_b():
	excel_f_b_heads = c.RECORDS+"/settings/db_sql_excel_form_b.head"
	reader = open(excel_f_b_heads,"r");excel_f_b_heads = json.loads(reader.read());reader.close()
	return excel_f_b_heads

def readRows(file, s_):
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name(s_)
    data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
    return data[6:]  

def move_to_done_files(FILENAME):
	# shutil.copy(
	shutil.move(
		c.RECORDS+"/objects/spreadsheets/queued/{}".format(FILENAME),
		# c.RECORDS+"/objects/spreadsheets/_temp_/{}".format(FILENAME),
		c.RECORDS+"/objects/spreadsheets/migrated/{}".format(FILENAME)
	)
	return "Done"

def move_to_failed_files(FILENAME):
	# shutil.copy(
	shutil.move(
		c.RECORDS+"/objects/spreadsheets/queued/{}".format(FILENAME),
		# c.RECORDS+"/objects/spreadsheets/_temp_/{}".format(FILENAME),
		c.RECORDS+"/objects/spreadsheets/failed/{}".format(FILENAME)
	)
	return "Done"

def readRowsHeads(file, s_):
	# wb = xlrd.open_workbook(file,encoding_override='utf-8')
	wb = xlrd.open_workbook(file)
	sheet = wb.sheet_by_name(s_)
	data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
	counter = 0
	return data[1:4]

class Filter:
	def position_data_filter():
		_filter = "WHERE 1 "
		JOB = session["USER_DATA"][0]["job"].lower()

		if(JOB in "admin" or JOB in "super admin"):
			session["USER_DATA"][0]["office"] = "NPCO"
			_filter = "WHERE 1 "
		else:
			session["USER_DATA"][0]["office"] = "Regional ({})".format(session["USER_DATA"][0]["rcu"])
			_filter = "WHERE  `uploaded_by` in ( SELECT id from users WHERE rcu='{}' )".format(session["USER_DATA"][0]["rcu"])
		return _filter

	def strct_dic(dict_):
		new_dict_ = {};
		for data in dict_:new_dict_[data['key']] = data['total']
		return json.loads(json.dumps(new_dict_))

	def strct_clean(dict_):
		new_dict_ = {};
		for data in dict_:new_dict_[data['key']] = data['total']
		return Filter.clean(json.loads(json.dumps(new_dict_)))

	def clean(dict_):
		new_dict_ = {};
		for key in dict_:
			KEY = key.lower().replace(" ","").replace(".","").replace("/","").replace("\\","").replace("-","").replace("*","").replace(",","").replace("(","").replace(")","").replace("&","")
			if(KEY not in new_dict_):
				new_dict_[KEY] = 0
			new_dict_[KEY] = new_dict_[KEY]+dict_[key]
			
		return json.loads(json.dumps(new_dict_))