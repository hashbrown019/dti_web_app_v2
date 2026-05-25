from datetime import date, datetime
from flask import Blueprint, Response, render_template, request, session, redirect, jsonify, send_file
from flask_session import Session
from modules.Connections import mysql,sqlite
import Configurations as c
import os
import json
from views.dcfv2.dashboard.display_dataform import displayform

# from flask_babel import Babel, format_currency

app = Blueprint("_dashboard",__name__,template_folder='templates')
rapid_sql = mysql(*c.DB_CRED)
api_key = "dtirapid@2025!"

def _normalize_none_to_zero(value):
    if isinstance(value, dict):
        return {k: _normalize_none_to_zero(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_none_to_zero(item) for item in value]
    if value is None:
        return 0
    return value

def _safe_percentage(count, total):
    return round((count / total) * 100, 4) if total else None

def _build_dashboard_summary_data():
    background_colors = ['#629DDD','#A4BF7F','#A48BC1','#E2918F','#F4D470','#E8AA78','#A5D7D8','#7173A9','#77838E']
    background_colors_comm = ['#8D5630', '#D9BDAB', '#D36E4C', '#FFD60C']

    shf_row = rapid_sql.select("""
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(`frmer_prof_@_basic_Info_@_Sex`='Male'), 0) AS total_male,
            COALESCE(SUM(`frmer_prof_@_basic_Info_@_Sex`='Female'), 0) AS total_female,
            COALESCE(SUM(`frmer_prof_@_basic_Info_@_sectoral_data`='IP'), 0) AS total_ip,
            COALESCE(SUM(`frmer_prof_@_basic_Info_@_sectoral_data`='Youth'), 0) AS total_youth,
            COALESCE(SUM(`frmer_prof_@_basic_Info_@_sectoral_data`='PWD'), 0) AS total_pwd,
            COALESCE(SUM(`frmer_prof_@_basic_Info_@_sectoral_data`='SC'), 0) AS total_sc,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('8','xiii','region8','region 8')), 0) AS region_8,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('9','ix','region9','region 9')), 0) AS region_9,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('10','x','region10','region 10')), 0) AS region_10,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('11','xi','region11','region 11')), 0) AS region_11,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('12','xii','region12','region 12')), 0) AS region_12,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('13','xiii','region13','region 13')), 0) AS region_13,
            COALESCE(SUM(`frmer_prof_@_frmer_addr_@_region` IN('BARMM')), 0) AS region_barmm,
            COALESCE(SUM(`frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cacao%'), 0) AS pc_cacao,
            COALESCE(SUM(`frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coconut%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Copra%'), 0) AS pc_coconut,
            COALESCE(SUM(`frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coffee%'), 0) AS pc_coffee,
            COALESCE(SUM(`frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%BananaCardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Calamansi%'), 0) AS pc_pfn,
            COALESCE(SUM(`frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cacao%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coconut%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Copra%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coffee%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%BananaCardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Calamansi%'), 0) AS pc_untagged
        FROM excel_import_form_a
    """)[0]
    shf_hh_row = rapid_sql.select("""
        SELECT
            COALESCE(SUM(eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex`='Male'), 0) AS male_total,
            COALESCE(SUM(eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex`='Female'), 0) AS female_total,
            COALESCE(SUM(eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex`!='Male' AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex`!='Female'), 0) AS untagged_total
        FROM __data_link_1 dl
        INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id
        WHERE dl.db_table='dcf_capacity_building'
    """)[0]
    shf_all_region = [
        _safe_percentage(shf_row['region_8'], shf_row['total']),
        _safe_percentage(shf_row['region_9'], shf_row['total']),
        _safe_percentage(shf_row['region_10'], shf_row['total']),
        _safe_percentage(shf_row['region_11'], shf_row['total']),
        _safe_percentage(shf_row['region_12'], shf_row['total']),
        _safe_percentage(shf_row['region_13'], shf_row['total']),
        _safe_percentage(shf_row['region_barmm'], shf_row['total'])
    ]

    fo_row = rapid_sql.select("""
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(types_of_organization='Cooperative'), 0) AS total_coop,
            COALESCE(SUM(types_of_organization='Association'), 0) AS total_assoc,
            COALESCE(SUM(types_of_organization='Others'), 0) AS total_others,
            IFNULL(SUM(organizational_total_overall), 0) AS total_members,
            IFNULL(SUM(organizational_total_male), 0) AS total_male,
            IFNULL(SUM(organizational_total_female), 0) AS total_female,
            COALESCE(SUM(`organizational_commodity` LIKE '%Cacao%'), 0) AS pc_cacao,
            COALESCE(SUM(`organizational_commodity` LIKE '%Coconut%' OR `organizational_commodity` LIKE '%Copra%'), 0) AS pc_coconut,
            COALESCE(SUM(`organizational_commodity` LIKE '%Coffee%'), 0) AS pc_coffee,
            COALESCE(SUM(`organizational_commodity` LIKE '%Banana%' OR `organizational_commodity` LIKE '%Banana Cardava%' OR `organizational_commodity` LIKE '%BananaCardava%' OR `organizational_commodity` LIKE '%Cardava%' OR `organizational_commodity` LIKE '%Calamansi%'), 0) AS pc_pfn,
            COALESCE(SUM(`organizational_commodity` NOT LIKE '%Cacao%' AND `organizational_commodity` NOT LIKE '%Coconut%' AND `organizational_commodity` NOT LIKE '%Copra%' AND `organizational_commodity` NOT LIKE '%Coffee%' AND `organizational_commodity` NOT LIKE '%Banana%' AND `organizational_commodity` NOT LIKE '%Banana Cardava%' AND `organizational_commodity` NOT LIKE '%BananaCardava%' AND `organizational_commodity` NOT LIKE '%Cardava%' AND `organizational_commodity` NOT LIKE '%Calamansi%'), 0) AS pc_untagged
        FROM form_b
    """)[0]
    fo_region_row = rapid_sql.select("""
        SELECT
            COALESCE(SUM(u.rcu IN('RCU8','RCU 8')), 0) AS region_8,
            COALESCE(SUM(u.rcu IN('RCU9','RCU 9')), 0) AS region_9,
            COALESCE(SUM(u.rcu IN('RCU10','RCU 10')), 0) AS region_10,
            COALESCE(SUM(u.rcu IN('RCU11','RCU 11')), 0) AS region_11,
            COALESCE(SUM(u.rcu IN('RCU12','RCU 12')), 0) AS region_12,
            COALESCE(SUM(u.rcu IN('RCU13','RCU 13')), 0) AS region_13,
            COALESCE(SUM(u.rcu IN('BARMM')), 0) AS region_barmm
        FROM form_b fb
        INNER JOIN users u ON u.id=fb.uploaded_by
    """)[0]
    fo_all_region = [
        _safe_percentage(fo_region_row['region_8'], fo_row['total']),
        _safe_percentage(fo_region_row['region_9'], fo_row['total']),
        _safe_percentage(fo_region_row['region_10'], fo_row['total']),
        _safe_percentage(fo_region_row['region_11'], fo_row['total']),
        _safe_percentage(fo_region_row['region_12'], fo_row['total']),
        _safe_percentage(fo_region_row['region_13'], fo_row['total']),
        _safe_percentage(fo_region_row['region_barmm'], fo_row['total'])
    ]

    msme_row = rapid_sql.select("""
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(`type_enterprise` IN ('Micro','Micro (3M below)')), 0) AS pc_micro,
            COALESCE(SUM(`type_enterprise` IN ('Small','Small (3-15M)')), 0) AS pc_small,
            COALESCE(SUM(`type_enterprise` IN ('Medium','Medium (15.1M-100M)')), 0) AS pc_medium,
            COALESCE(SUM(`type_enterprise` IN ('Large','Large (Above 100M)')), 0) AS pc_large,
            COALESCE(SUM(`industry_cluster` LIKE '%Cacao%'), 0) AS ic_cacao,
            COALESCE(SUM(`industry_cluster` LIKE '%Coconut%' OR `industry_cluster` LIKE '%Copra%'), 0) AS ic_coconut,
            COALESCE(SUM(`industry_cluster` LIKE '%Coffee%'), 0) AS ic_coffee,
            COALESCE(SUM(`industry_cluster` LIKE '%Banana%' OR `industry_cluster` LIKE '%Banana Cardava%' OR `industry_cluster` LIKE '%BananaCardava%' OR `industry_cluster` LIKE '%Cardava%' OR `industry_cluster` LIKE '%Calamansi%'), 0) AS ic_pfn,
            COALESCE(SUM(`industry_cluster` NOT LIKE '%Cacao%' AND `industry_cluster` NOT LIKE '%Coconut%' AND `industry_cluster` NOT LIKE '%Copra%' AND `industry_cluster` NOT LIKE '%Coffee%' AND `industry_cluster` NOT LIKE '%Banana%' AND `industry_cluster` NOT LIKE '%Banana Cardava%' AND `industry_cluster` NOT LIKE '%BananaCardava%' AND `industry_cluster` NOT LIKE '%Cardava%' AND `industry_cluster` NOT LIKE '%Calamansi%'), 0) AS ic_untagged
        FROM form_c
    """)[0]
    msme_region_row = rapid_sql.select("""
        SELECT
            COALESCE(SUM(u.rcu IN('RCU8','RCU 8')), 0) AS region_8,
            COALESCE(SUM(u.rcu IN('RCU9','RCU 9')), 0) AS region_9,
            COALESCE(SUM(u.rcu IN('RCU10','RCU 10')), 0) AS region_10,
            COALESCE(SUM(u.rcu IN('RCU11','RCU 11')), 0) AS region_11,
            COALESCE(SUM(u.rcu IN('RCU12','RCU 12')), 0) AS region_12,
            COALESCE(SUM(u.rcu IN('RCU13','RCU 13')), 0) AS region_13,
            COALESCE(SUM(u.rcu IN('BARMM')), 0) AS region_barmm
        FROM form_c fc
        INNER JOIN users u ON u.id=fc.upload_by
    """)[0]
    msme_all_region = [
        _safe_percentage(msme_region_row['region_8'], msme_row['total']),
        _safe_percentage(msme_region_row['region_9'], msme_row['total']),
        _safe_percentage(msme_region_row['region_10'], msme_row['total']),
        _safe_percentage(msme_region_row['region_11'], msme_row['total']),
        _safe_percentage(msme_region_row['region_12'], msme_row['total']),
        _safe_percentage(msme_region_row['region_13'], msme_row['total']),
        _safe_percentage(msme_region_row['region_barmm'], msme_row['total'])
    ]

    fmr_total = rapid_sql.select("SELECT COUNT(*) AS total FROM dcf_fmi")[0]['total']
    fmr_status_rows = rapid_sql.select("""
        SELECT
            `form_8_implementation_status` AS status,
            COUNT(*) AS total,
            IFNULL(SUM(form_8_profile_length), 0 ) AS total_km,
            IFNULL(SUM(form_8_profile_appvd_budget_cost), 0 ) AS total_appr_budget
        FROM dcf_fmi
        GROUP BY `form_8_implementation_status`
    """)
    fmr_status_map = {row['status']: row for row in fmr_status_rows}
    fmr_empty = {'total': 0, 'total_km': 0, 'total_appr_budget': 0}
    fmr_completed = fmr_status_map.get('Completed', fmr_empty)
    fmr_ongoing = fmr_status_map.get('On-going', fmr_empty)
    fmr_no1 = fmr_status_map.get('For NO 1', fmr_empty)
    fmr_no2 = fmr_status_map.get('For NO 2', fmr_empty)
    fmr_no3 = fmr_status_map.get('For NO 3', fmr_empty)
    fmr_pending = fmr_status_map.get('Pending', fmr_empty)
    fmr_noa = fmr_status_map.get('Issuance of NOA', fmr_empty)

    batch_status_order = ['Pending', 'On-going', 'For NO 1', 'For NO 2', 'For NO 3', 'Issuance of NOA', 'Completed']
    fmr_batch_map = {1: {s: 0 for s in batch_status_order}, 2: {s: 0 for s in batch_status_order}, 3: {s: 0 for s in batch_status_order}, 4: {s: 0 for s in batch_status_order}}
    fmr_batch_rows = rapid_sql.select("""
        SELECT `form_8_profile_batch` AS batch_no, `form_8_implementation_status` AS status, COUNT(*) AS total
        FROM dcf_fmi
        WHERE `form_8_profile_batch` IN (1,2,3,4)
        GROUP BY `form_8_profile_batch`, `form_8_implementation_status`
    """)
    for row in fmr_batch_rows:
        if row['batch_no'] in fmr_batch_map and row['status'] in fmr_batch_map[row['batch_no']]:
            fmr_batch_map[row['batch_no']][row['status']] = row['total']

    def _batch_payload(batch_no):
        return {
            'data': [fmr_batch_map[batch_no][status] for status in batch_status_order],
            'labels': ['Pending','Ongoing','For NO 1','For NO 2','For NO 3','Issuance  of NOA','Completed'],
            'background_colors': background_colors
        }

    fmi_data = {
        'FMR_totalkm_completed_ongoing': (fmr_completed['total_km'] + fmr_ongoing['total_km']),
        'FMR_total': fmr_total,
        'FMR_completed': {'total': fmr_completed['total'], 'total_km': fmr_completed['total_km'], 'total_appr_budget': fmr_completed['total_appr_budget']},
        'FMR_ongoing': {'total': fmr_ongoing['total'], 'total_km': fmr_ongoing['total_km'], 'total_appr_budget': fmr_ongoing['total_appr_budget']},
        'FMR_no1': {'total': fmr_no1['total'], 'total_km': fmr_no1['total_km'], 'total_appr_budget': fmr_no1['total_appr_budget']},
        'FMR_no2': {'total': fmr_no2['total'], 'total_km': fmr_no2['total_km'], 'total_appr_budget': fmr_no2['total_appr_budget']},
        'FMR_no3': {'total': fmr_no3['total'], 'total_km': fmr_no3['total_km'], 'total_appr_budget': fmr_no3['total_appr_budget']},
        'FMR_pending': {'total': fmr_pending['total'], 'total_km': fmr_pending['total_km'], 'total_appr_budget': fmr_pending['total_appr_budget']},
        'FMR_noa': {'total': fmr_noa['total'], 'total_km': fmr_noa['total_km'], 'total_appr_budget': fmr_noa['total_appr_budget']},
        'FMR_Batch_data': {
            'FMR_Batch1_data': _batch_payload(1),
            'FMR_Batch2_data': _batch_payload(2),
            'FMR_Batch3_data': _batch_payload(3),
            'FMR_Batch4_data': _batch_payload(4)
        }
    }

    return {
        'SHF': {
            'SHF_Total': shf_row['total'],
            'SHF_Total_Male': shf_row['total_male'],
            'SHF_Total_Female': shf_row['total_female'],
            'SHF_Total_IP': shf_row['total_ip'],
            'SHF_Total_PWD': shf_row['total_pwd'],
            'SHF_Total_Youth': shf_row['total_youth'],
            'SHF_Total_SC': shf_row['total_sc'],
            'SHF_byRegion': {'labels': ['R-8','R-9','R-10','R-11','R-12','R-13','BARMM'], 'data': shf_all_region, 'background_colors': background_colors},
            'SHF_PC_data': {'labels': ['Cacao','Coconut','Coffee','PFN'], 'data': [shf_row['pc_cacao'], shf_row['pc_coconut'], shf_row['pc_coffee'], shf_row['pc_pfn'], shf_row['pc_untagged']], 'background_colors': background_colors_comm},
            'SHF_HH_Head_data': {'labels': ['Male','Female','Untagged'], 'data': [shf_hh_row['male_total'], shf_hh_row['female_total'], shf_hh_row['untagged_total']], 'background_colors': background_colors}
        },
        'FO': {
            'FO_Total': fo_row['total'],
            'FO_Total_Coop': fo_row['total_coop'],
            'FO_Total_Assoc': fo_row['total_assoc'],
            'FO_Total_Members': fo_row['total_members'],
            'FO_Total_Male': fo_row['total_male'],
            'FO_Total_Female': fo_row['total_female'],
            'FO_byRegion': {'labels': ['R-8','R-9','R-10','R-11','R-12','R-13','BARMM'], 'data': fo_all_region, 'background_colors': background_colors},
            'FO_byOrgType': {'labels': ['Association','Cooperative','Others'], 'data': [fo_row['total_assoc'], fo_row['total_coop'], fo_row['total_others']], 'background_colors': background_colors},
            'FO_PC_data': {'labels': ['Cacao','Coconut','Coffee','PFN'], 'data': [fo_row['pc_cacao'], fo_row['pc_coconut'], fo_row['pc_coffee'], fo_row['pc_pfn'], fo_row['pc_untagged']], 'background_colors': background_colors_comm}
        },
        'MSME': {
            'MSME_Total': msme_row['total'],
            'MSME_byRegion': {'labels': ['R-8','R-9','R-10','R-11','R-12','R-13','BARMM'], 'data': msme_all_region, 'background_colors': background_colors},
            'MSME_PC_data': {'labels': ['Micro','Small','Medium','Large'], 'data': [msme_row['pc_micro'], msme_row['pc_small'], msme_row['pc_medium'], msme_row['pc_large']], 'background_colors': background_colors},
            'MSME_IC_data': {'labels': ['Cacao','Coconut','Coffee','PFN'], 'data': [msme_row['ic_cacao'], msme_row['ic_coconut'], msme_row['ic_coffee'], msme_row['ic_pfn'], msme_row['ic_untagged']], 'background_colors': background_colors_comm}
        },
        'FMI': fmi_data
    }

class _main:
    def __init__(self, arg):
        
        super(_main, self).__init__()
        self.arg = arg

    @app.route("/dashboard_summary", methods=["POST","GET"])
    def system_page():
        return jsonify(_normalize_none_to_zero(_build_dashboard_summary_data()))
    
    @app.route("/dashboard_analytic_shf", methods=["GET"])
    def dashboard_analytic_shf():
        key = request.headers.get("x-api-key")
        if key != api_key:
            return jsonify({"error": "Unauthorized"}), 401

        # 📥 Get query params (default: page=1, limit=100)
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))

        # 🧮 Calculate offset
        offset = (page - 1) * limit

        # 📊 Fetch paginated data
        query = f"SELECT * FROM excel_import_form_a LIMIT {limit} OFFSET {offset}"
        SHF_Data = rapid_sql.select(query)

        # 📦 Return with metadata
        return jsonify({
            "page": page,
            "limit": limit,
            "data": SHF_Data
        })
    
    @app.route("/dashboard_analytic_fo", methods=["GET"])
    def dashboard_analytic_fo():
        key = request.headers.get("x-api-key")
        if key != api_key:
            return jsonify({"error": "Unauthorized"}), 401

        # 📥 Get query params (default: page=1, limit=100)
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))

        # 🧮 Calculate offset
        offset = (page - 1) * limit

        # 📊 Fetch paginated data
        query = f"SELECT * FROM form_b LIMIT {limit} OFFSET {offset}"
        SHF_Data = rapid_sql.select(query)

        # 📦 Return with metadata
        return jsonify({
            "page": page,
            "limit": limit,
            "data": SHF_Data
        })
    
    @app.route("/dashboard_analytic_msme", methods=["GET"])
    def dashboard_analytic_msme():
        key = request.headers.get("x-api-key")
        if key != api_key:
            return jsonify({"error": "Unauthorized"}), 401

        # 📥 Get query params (default: page=1, limit=100)
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 100))

        # 🧮 Calculate offset
        offset = (page - 1) * limit

        # 📊 Fetch paginated data
        query = f"SELECT * FROM form_c LIMIT {limit} OFFSET {offset}"
        SHF_Data = rapid_sql.select(query)

        # 📦 Return with metadata
        return jsonify({
            "page": page,
            "limit": limit,
            "data": SHF_Data
        })