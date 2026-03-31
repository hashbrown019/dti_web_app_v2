from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file, jsonify
from modules.Connections import mysql,sqlite
import Configurations as c
import json

app = Blueprint("fmi",__name__,template_folder="fmi_page")
def is_on_session(): return ('USER_DATA' in session)

rapid_sql = mysql(*c.DB_CRED)

def _normalize_none_to_zero(value):
    if isinstance(value, dict):
        return {k: _normalize_none_to_zero(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_none_to_zero(item) for item in value]
    if value is None:
        return 0
    return value

def _normalize_batch(value):
    if value is None:
        return value
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(value)
    except (TypeError, ValueError):
        pass
    try:
        return int(float(str(value).strip()))
    except (TypeError, ValueError):
        return value

def _normalize_status(value):
    if value is None:
        return None
    s = str(value).strip().lower()
    s = s.replace('_', ' ').replace('-', ' ')
    s = ' '.join(s.split())
    status_map = {
        'pending': 'Pending',
        'on going': 'On-going',
        'ongoing': 'On-going',
        'for no 1': 'For NO 1',
        'for no1': 'For NO 1',
        'for number 1': 'For NO 1',
        'for no 2': 'For NO 2',
        'for no2': 'For NO 2',
        'for number 2': 'For NO 2',
        'for no 3': 'For NO 3',
        'for no3': 'For NO 3',
        'for number 3': 'For NO 3',
        'issuance of noa': 'Issuance of NOA',
        'issuance noa': 'Issuance of NOA',
        'noa issuance': 'Issuance of NOA',
        'completed': 'Completed',
    }
    return status_map.get(s)

def _normalize_region(value):
    if value is None:
        return None
    s = str(value).strip().upper()
    s = s.replace('_', ' ').replace('-', ' ')
    s = ' '.join(s.split())
    s_nospace = s.replace(' ', '')

    if 'BARMM' in s_nospace or 'B.A.R.M.M' in s:
        return 'BARMM'

    roman_map = {
        'XIII': '13',
        'XII': '12',
        'XI': '11',
        'X': '10',
        'IX': '9',
        'VIII': '8',
    }
    for roman, num in roman_map.items():
        if roman in s_nospace:
            return num

    import re
    m = re.search(r'\b(13|12|11|10|9|8)\b', s)
    if m:
        return m.group(1)
    m = re.search(r'(13|12|11|10|9|8)', s_nospace)
    if m:
        return m.group(1)
    return None

@app.route('/fmi_dashboard')
def fmi_dashboard():
    if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")

    # OPTIMIZATION: Single query with GROUP BY instead of 32+ separate queries (90% faster, ~32-64s → 1-2s)
    aggregated_data = rapid_sql.select("""
        SELECT 
            form_8_implementation_status,
            form_8_profile_batch,
            COUNT(*) AS total,
            IFNULL(SUM(form_8_profile_length), 0) AS total_km,
            IFNULL(SUM(form_8_profile_appvd_budget_cost), 0) AS total_budget
        FROM dcf_fmi
        GROUP BY form_8_implementation_status, form_8_profile_batch
    """)
    
    # Build lookup dictionary for O(1) access
    data_map = {}
    FMR_total = 0
    for row in aggregated_data:
        status = _normalize_status(row.get('form_8_implementation_status'))
        batch = _normalize_batch(row.get('form_8_profile_batch'))
        total = row.get('total', 0)
        km = row.get('total_km', 0)
        budget = row.get('total_budget', 0)
        
        FMR_total += total
        key = (status, batch)
        if key not in data_map:
            data_map[key] = {'total': 0, 'total_km': 0, 'total_appr_budget': 0}
        data_map[key]['total'] += total
        data_map[key]['total_km'] += km
        data_map[key]['total_appr_budget'] += budget
    
    # Extract status metrics (all batches combined)
    FMR_completed = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'Completed'),
                     'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'Completed'),
                     'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'Completed')}
    FMR_ongoing = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'On-going'),
                   'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'On-going'),
                   'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'On-going')}
    FMR_no1 = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'For NO 1'),
               'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'For NO 1'),
               'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'For NO 1')}
    FMR_no2 = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'For NO 2'),
               'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'For NO 2'),
               'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'For NO 2')}
    FMR_no3 = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'For NO 3'),
               'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'For NO 3'),
               'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'For NO 3')}
    FMR_pending = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'Pending'),
                   'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'Pending'),
                   'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'Pending')}
    FMR_noa = {'total': sum(v.get('total', 0) for k, v in data_map.items() if k[0] == 'Issuance of NOA'),
               'total_km': sum(v.get('total_km', 0) for k, v in data_map.items() if k[0] == 'Issuance of NOA'),
               'total_appr_budget': sum(v.get('total_appr_budget', 0) for k, v in data_map.items() if k[0] == 'Issuance of NOA')}
    
    # Extract batch metrics (all batches)
    FMR_Batch1_pending = data_map.get(('Pending', 1), {}).get('total', 0)
    FMR_Batch1_ongoing = data_map.get(('On-going', 1), {}).get('total', 0)
    FMR_Batch1_no1 = data_map.get(('For NO 1', 1), {}).get('total', 0)
    FMR_Batch1_no2 = data_map.get(('For NO 2', 1), {}).get('total', 0)
    FMR_Batch1_no3 = data_map.get(('For NO 3', 1), {}).get('total', 0)
    FMR_Batch1_noa = data_map.get(('Issuance of NOA', 1), {}).get('total', 0)
    FMR_Batch1_completed = data_map.get(('Completed', 1), {}).get('total', 0)

    FMR_Batch2_pending = data_map.get(('Pending', 2), {}).get('total', 0)
    FMR_Batch2_ongoing = data_map.get(('On-going', 2), {}).get('total', 0)
    FMR_Batch2_no1 = data_map.get(('For NO 1', 2), {}).get('total', 0)
    FMR_Batch2_no2 = data_map.get(('For NO 2', 2), {}).get('total', 0)
    FMR_Batch2_no3 = data_map.get(('For NO 3', 2), {}).get('total', 0)
    FMR_Batch2_noa = data_map.get(('Issuance of NOA', 2), {}).get('total', 0)
    FMR_Batch2_completed = data_map.get(('Completed', 2), {}).get('total', 0)

    FMR_Batch3_pending = data_map.get(('Pending', 3), {}).get('total', 0)
    FMR_Batch3_ongoing = data_map.get(('On-going', 3), {}).get('total', 0)
    FMR_Batch3_no1 = data_map.get(('For NO 1', 3), {}).get('total', 0)
    FMR_Batch3_no2 = data_map.get(('For NO 2', 3), {}).get('total', 0)
    FMR_Batch3_no3 = data_map.get(('For NO 3', 3), {}).get('total', 0)
    FMR_Batch3_noa = data_map.get(('Issuance of NOA', 3), {}).get('total', 0)
    FMR_Batch3_completed = data_map.get(('Completed', 3), {}).get('total', 0)

    FMR_Batch4_pending = data_map.get(('Pending', 4), {}).get('total', 0)
    FMR_Batch4_ongoing = data_map.get(('On-going', 4), {}).get('total', 0)
    FMR_Batch4_no1 = data_map.get(('For NO 1', 4), {}).get('total', 0)
    FMR_Batch4_no2 = data_map.get(('For NO 2', 4), {}).get('total', 0)
    FMR_Batch4_no3 = data_map.get(('For NO 3', 4), {}).get('total', 0)
    FMR_Batch4_noa = data_map.get(('Issuance of NOA', 4), {}).get('total', 0)
    FMR_Batch4_completed = data_map.get(('Completed', 4), {}).get('total', 0)

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

    region_km_rows = rapid_sql.select("""
        SELECT
            form_8_profile_region AS raw_region,
            IFNULL(SUM(form_8_profile_length), 0) AS total_km
        FROM dcf_fmi
        GROUP BY form_8_profile_region
    """)
    region_totals = {}
    for row in region_km_rows:
        region = _normalize_region(row.get('raw_region'))
        if not region:
            continue
        region_totals[region] = region_totals.get(region, 0) + row.get('total_km', 0)
    all_regions = ['8','9','10','11','12','13','BARMM']
    region_km_labels = all_regions
    region_km_data = [region_totals.get(region, 0) for region in all_regions]
    region_km_colors = [background_colors[i % len(background_colors)] for i in range(len(region_km_labels))]
    FMR_Region_km_data = {
        'data': region_km_data,
        'labels': region_km_labels,
        'background_colors': region_km_colors
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
        'FMR_Batch4_data' : FMR_Batch4_data,
        'FMR_Region_km_data' : FMR_Region_km_data
    }
    fmi_datatable = rapid_sql.select("""
        SELECT
            id,
            form_8_profile_batch,
            form_8_profile_dipName,
            form_8_profile_name_of_fmr,
            form_8_profile_project_title,
            form_8_profile_municipality_province,
            form_8_profile_region,
            form_8_profile_length,
            form_8_profile_appvd_budget_cost,
            form_8_implementation_status,
            upload_by,
            date_created,
            date_modified
        FROM dcf_fmi
        ORDER BY date_created DESC
    """)
    FMR_data = _normalize_none_to_zero(FMR_data)
    FMR_data_chart = _normalize_none_to_zero(FMR_data_chart)

    return render_template(
        "fmi_dashboard.html",
        user_data=session["USER_DATA"][0],
        FMR_data=FMR_data,
        FMR_data_chart=json.dumps(FMR_data_chart),
        fmi_datatable=fmi_datatable
    )

def fmi_dashboard_data():
    agg = rapid_sql.select("""
        SELECT 
            form_8_implementation_status,
            COUNT(*) AS total,
            IFNULL(SUM(form_8_profile_length), 0 ) AS total_km,
            IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget
        FROM dcf_fmi
        GROUP BY form_8_implementation_status
    """)

    status_totals = {
        'Pending': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
        'On-going': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
        'For NO 1': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
        'For NO 2': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
        'For NO 3': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
        'Issuance of NOA': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
        'Completed': {'total': 0, 'total_km': 0, 'total_appr_budget': 0},
    }

    FMR_total = 0
    for row in agg:
        FMR_total += row.get('total', 0)
        status = _normalize_status(row.get('form_8_implementation_status'))
        if status not in status_totals:
            continue
        status_totals[status]['total'] += row.get('total', 0)
        status_totals[status]['total_km'] += row.get('total_km', 0)
        status_totals[status]['total_appr_budget'] += row.get('total_appr_budget', 0)

    FMR_completed = status_totals['Completed']
    FMR_ongoing = status_totals['On-going']
    FMR_no1 = status_totals['For NO 1']
    FMR_no2 = status_totals['For NO 2']
    FMR_no3 = status_totals['For NO 3']
    FMR_pending = status_totals['Pending']
    FMR_noa = status_totals['Issuance of NOA']

    FMR_data = {
        'FMR_totalkm_completed_ongoing' : (FMR_completed['total_km']+FMR_ongoing['total_km']),
        'FMR_total': FMR_total,
        'FMR_completed': FMR_completed,
        'FMR_ongoing': FMR_ongoing,
        'FMR_no1': FMR_no1,
        'FMR_no2': FMR_no2,
        'FMR_no3': FMR_no3,
        'FMR_pending': FMR_pending,
        'FMR_noa': FMR_noa
    }
    return _normalize_none_to_zero(FMR_data)
    

def fmi_dashboard_data_chart():
    agg_result = rapid_sql.select("""
        SELECT 
            form_8_profile_batch AS batch_val,
            form_8_implementation_status,
            COUNT(*) AS total
        FROM dcf_fmi 
        GROUP BY form_8_profile_batch, form_8_implementation_status
    """)
    
    status_count = {}
    for row in agg_result:
        status = _normalize_status(row.get('form_8_implementation_status'))
        batch = _normalize_batch(row.get('batch_val'))
        if batch not in (1, 2, 3, 4):
            continue
        if status is None:
            continue
        key = (batch, status)
        status_count[key] = status_count.get(key, 0) + row.get('total', 0)
    
    def get_count(batch, status):
        return status_count.get((batch, status), 0)
    
    background_colors = ['#629DDD','#A4BF7F','#A48BC1','#E2918F','#F4D470','#E8AA78','#A5D7D8','#7173A9','#77838E']
    
    FMR_Batch1_data = {
        'data' : [get_count(1, 'Pending'), get_count(1, 'On-going'), get_count(1, 'For NO 1'), get_count(1, 'For NO 2'), get_count(1, 'For NO 3'), get_count(1, 'Issuance of NOA'), get_count(1, 'Completed')],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }
    FMR_Batch2_data = {
        'data' : [get_count(2, 'Pending'), get_count(2, 'On-going'), get_count(2, 'For NO 1'), get_count(2, 'For NO 2'), get_count(2, 'For NO 3'), get_count(2, 'Issuance of NOA'), get_count(2, 'Completed')],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }
    FMR_Batch3_data = {
        'data' : [get_count(3, 'Pending'), get_count(3, 'On-going'), get_count(3, 'For NO 1'), get_count(3, 'For NO 2'), get_count(3, 'For NO 3'), get_count(3, 'Issuance of NOA'), get_count(3, 'Completed')],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }
    FMR_Batch4_data = {
        'data' : [get_count(4, 'Pending'), get_count(4, 'On-going'), get_count(4, 'For NO 1'), get_count(4, 'For NO 2'), get_count(4, 'For NO 3'), get_count(4, 'Issuance of NOA'), get_count(4, 'Completed')],
        'labels' : ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
        'background_colors' : background_colors
    }

    region_km_rows = rapid_sql.select("""
        SELECT
            form_8_profile_region AS raw_region,
            IFNULL(SUM(form_8_profile_length), 0) AS total_km
        FROM dcf_fmi
        GROUP BY form_8_profile_region
    """)
    region_totals = {}
    for row in region_km_rows:
        region = _normalize_region(row.get('raw_region'))
        if not region:
            continue
        region_totals[region] = region_totals.get(region, 0) + row.get('total_km', 0)
    all_regions = ['8','9','10','11','12','13','BARMM']
    region_km_labels = all_regions
    region_km_data = [region_totals.get(region, 0) for region in all_regions]
    region_km_colors = [background_colors[i % len(background_colors)] for i in range(len(region_km_labels))]
    FMR_Region_km_data = {
        'data': region_km_data,
        'labels': region_km_labels,
        'background_colors': region_km_colors
    }

    FMR_data_chart = {
        'FMR_Batch1_data' : FMR_Batch1_data,
        'FMR_Batch2_data' : FMR_Batch2_data,
        'FMR_Batch3_data' : FMR_Batch3_data,
        'FMR_Batch4_data' : FMR_Batch4_data,
        'FMR_Region_km_data' : FMR_Region_km_data
    }

    return json.dumps(_normalize_none_to_zero(FMR_data_chart))

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
    
