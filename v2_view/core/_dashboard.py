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

class _main:
    def __init__(self, arg):
        super(_main, self).__init__()
        self.arg = arg

    @app.route("/dashboard_summary", methods=["POST","GET"])
    def system_page():

        # SMALL HOLDER FARMERS
        SHF_Total = rapid_sql.select("SELECT COUNT(*) AS total FROM excel_import_form_a")
        SHF_Total_Male = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_Sex`='Male'")
        SHF_Total_Female = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_Sex`='Female'")
        SHF_Total_IP = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='IP'")
        SHF_Total_Youth = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='Youth'")
        SHF_Total_PWD = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='PWD'")
        SHF_Total_SC = rapid_sql.select("SELECT COUNT(*) AS total FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='SC'")
        
        SHF_byRegion_8 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('8','xiii','region8','region 8')")
        SHF_byRegion_9 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('9','ix','region9','region 9')")
        SHF_byRegion_10 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('10','x','region10','region 10')")
        SHF_byRegion_11 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('11','xi','region11','region 11')")
        SHF_byRegion_12 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('12','xii','region12','region 12')")
        SHF_byRegion_13 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('13','xiii','region13','region 13')")
        SHF_byRegion_barmm = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('BARMM')")
        
        SHF_allRegion = [SHF_byRegion_8[0]['percTotal'],SHF_byRegion_9[0]['percTotal'],SHF_byRegion_10[0]['percTotal'],SHF_byRegion_11[0]['percTotal'],SHF_byRegion_12[0]['percTotal'],SHF_byRegion_13[0]['percTotal'],SHF_byRegion_barmm[0]['percTotal']]
        
        SHF_PC_cacao = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cacao%'")
        SHF_PC_coconut = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coconut%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Copra%'")
        SHF_PC_coffee = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coffee%'")
        SHF_PC_pfn = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%BananaCardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Calamansi%'")
        SHF_PC_untagged = rapid_sql.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cacao%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coconut%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Copra%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coffee%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%BananaCardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Calamansi%'")

        SHF_PC_data = [SHF_PC_cacao[0]['total'],SHF_PC_coconut[0]['total'],SHF_PC_coffee[0]['total'],SHF_PC_pfn[0]['total'],SHF_PC_untagged[0]['total']]

        SHF_total_HH_head_male = rapid_sql.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` = 'Male' WHERE dl.db_table='dcf_capacity_building'")
        SHF_total_HH_head_female = rapid_sql.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` = 'Female' WHERE dl.db_table='dcf_capacity_building'")
        SHF_total_HH_head_untagged = rapid_sql.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` != 'Male' AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` != 'Female' WHERE dl.db_table='dcf_capacity_building'")

        SHF_total_HH_head_data = [SHF_total_HH_head_male[0]['total'],SHF_total_HH_head_female[0]['total'],SHF_total_HH_head_untagged[0]['total']];

        # FARMER ORGANIZATION
        FO_Total = rapid_sql.select("SELECT COUNT(*) AS total FROM form_b")
        FO_Total_Coop = rapid_sql.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Cooperative'")
        FO_Total_Assoc = rapid_sql.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Association'")
        FO_Total_Others = rapid_sql.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Others'")
        FO_Total_Members = rapid_sql.select("SELECT SUM(organizational_total_overall) AS total FROM form_b")
        FO_Total_Male = rapid_sql.select("SELECT SUM(organizational_total_male) AS total FROM form_b ")
        FO_Total_Female = rapid_sql.select("SELECT SUM(organizational_total_female) AS total FROM form_b ")

        FO_byRegion_8 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU8','RCU 8')")
        FO_byRegion_9 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU9','RCU 9')")
        FO_byRegion_10 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU10','RCU 10')")
        FO_byRegion_11 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU11','RCU 11')")
        FO_byRegion_12 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU12','RCU 12')")
        FO_byRegion_13 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU13','RCU 13')")
        FO_byRegion_barmm = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('BARMM')")
        
        FO_allRegion = [FO_byRegion_8[0]['percTotal'],FO_byRegion_9[0]['percTotal'],FO_byRegion_10[0]['percTotal'],FO_byRegion_11[0]['percTotal'],FO_byRegion_12[0]['percTotal'],FO_byRegion_13[0]['percTotal'],FO_byRegion_barmm[0]['percTotal']]
        FO_byOrgType = [FO_Total_Assoc[0]['total'],FO_Total_Coop[0]['total'],FO_Total_Others[0]['total']]
        
        # FO_PC_cacao = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` IN ('Cacao')")
        # FO_PC_coconut = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` IN ('Coconut','Copra')")
        # FO_PC_coffee = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` IN ('Coffee')")
        # FO_PC_pfn = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` IN ('Banana','Banana Cardava','BananaCardava','Cardava','Calamansi')")
        
        FO_PC_cacao = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Cacao%'")
        FO_PC_coconut = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Coconut%' OR `organizational_commodity` LIKE '%Copra%'")
        FO_PC_coffee = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Coffee%'")
        FO_PC_pfn = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Banana%' OR `organizational_commodity` LIKE '%Banana Cardava%' OR `organizational_commodity` LIKE '%BananaCardava%' OR `organizational_commodity` LIKE '%Cardava%' OR `organizational_commodity` LIKE '%Calamansi%'")
        FO_PC_untagged = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` NOT LIKE '%Cacao%' AND `organizational_commodity` NOT LIKE '%Coconut%' AND `organizational_commodity` NOT LIKE '%Copra%' AND `organizational_commodity` NOT LIKE '%Coffee%' AND `organizational_commodity` NOT LIKE '%Banana%' AND `organizational_commodity` NOT LIKE '%Banana Cardava%' AND `organizational_commodity` NOT LIKE '%BananaCardava%' AND `organizational_commodity` NOT LIKE '%Cardava%' AND `organizational_commodity` NOT LIKE '%Calamansi%'")


        FO_PC_data = [FO_PC_cacao[0]['total'],FO_PC_coconut[0]['total'],FO_PC_coffee[0]['total'],FO_PC_pfn[0]['total'],FO_PC_untagged[0]['total']]

        # Micro, Small, Medium Enterprises
        MSME_Total = rapid_sql.select("SELECT COUNT(*) AS total FROM form_c")

        MSME_byRegion_8 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU8','RCU 8')")
        MSME_byRegion_9 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU9','RCU 9')")
        MSME_byRegion_10 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU10','RCU 10')")
        MSME_byRegion_11 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU11','RCU 11')")
        MSME_byRegion_12 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU12','RCU 12')")
        MSME_byRegion_13 = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU13','RCU 13')")
        MSME_byRegion_barmm = rapid_sql.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('BARMM')")

        MSME_allRegion = [MSME_byRegion_8[0]['percTotal'],MSME_byRegion_9[0]['percTotal'],MSME_byRegion_10[0]['percTotal'],MSME_byRegion_11[0]['percTotal'],MSME_byRegion_12[0]['percTotal'],MSME_byRegion_13[0]['percTotal'],MSME_byRegion_barmm[0]['percTotal']]
        
        # MSME / PC ( BarChart )
        MSME_PC_micro = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Micro','Micro (3M below)')")
        MSME_PC_small = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Small','Small (3-15M)')")
        MSME_PC_medium = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Medium','Medium (15.1M-100M)')")
        MSME_PC_large = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Large','Large (Above 100M)')")
        
        MSME_PC_data = [MSME_PC_micro[0]['total'],MSME_PC_small[0]['total'],MSME_PC_medium[0]['total'],MSME_PC_large[0]['total']]
        
        # MSME / Commodity ( BarChart )
        # MSME_IC_cacao = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` IN ('Cacao')")
        # MSME_IC_coconut = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` IN ('Coconut','Copra')")
        # MSME_IC_coffee = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` IN ('Coffee')")
        # MSME_IC_pfn = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` IN ('Banana','Banana Cardava','BananaCardava','Cardava','Calamansi')")
        
        MSME_IC_cacao = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Cacao%'")
        MSME_IC_coconut = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Coconut%' OR `industry_cluster` LIKE '%Copra%'")
        MSME_IC_coffee = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Coffee%'")
        MSME_IC_pfn = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Banana%' OR `industry_cluster` LIKE '%Banana Cardava%' OR `industry_cluster` LIKE '%BananaCardava%' OR `industry_cluster` LIKE '%Cardava%' OR `industry_cluster` LIKE '%Calamansi%'")
        MSME_IC_untagged = rapid_sql.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` NOT LIKE '%Cacao%' AND `industry_cluster` NOT LIKE '%Coconut%' AND `industry_cluster` NOT LIKE '%Copra%' AND `industry_cluster` NOT LIKE '%Coffee%' AND `industry_cluster` NOT LIKE '%Banana%' AND `industry_cluster` NOT LIKE '%Banana Cardava%' AND `industry_cluster` NOT LIKE '%BananaCardava%' AND `industry_cluster` NOT LIKE '%Cardava%' AND `industry_cluster` NOT LIKE '%Calamansi%'")


        MSME_IC_data = [MSME_IC_cacao[0]['total'],MSME_IC_coconut[0]['total'],MSME_IC_coffee[0]['total'],MSME_IC_pfn[0]['total'],MSME_IC_untagged[0]['total']]

        # ====================================================================================
        # FMI
        # ====================================================================================
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

        FMI_data = {
            'FMR_totalkm_completed_ongoing' : (FMR_completed['total_km']+FMR_ongoing['total_km']),
            'FMR_total': FMR_total,
            'FMR_completed': FMR_completed,
            'FMR_ongoing': FMR_ongoing,
            'FMR_no1': FMR_no1,
            'FMR_no2': FMR_no2,
            'FMR_no3': FMR_no3,
            'FMR_pending': FMR_pending,
            'FMR_noa': FMR_noa,
            'FMR_Batch_data': {
                'FMR_Batch1_data' : FMR_Batch1_data,
                'FMR_Batch2_data' : FMR_Batch2_data,
                'FMR_Batch3_data' : FMR_Batch3_data,
                'FMR_Batch4_data' : FMR_Batch4_data
            }
        }
        # ====================================================================================
        # FMI - End
        # ====================================================================================

        background_colors = ['#629DDD','#A4BF7F','#A48BC1','#E2918F','#F4D470','#E8AA78','#A5D7D8','#7173A9','#77838E']
        background_colors_comm = ['#8D5630', '#D9BDAB', '#D36E4C', '#FFD60C']
        data = {
            'SHF' : {
                'SHF_Total' : SHF_Total[0]['total'],
                'SHF_Total_Male' : SHF_Total_Male[0]['total'],
                'SHF_Total_Female' : SHF_Total_Female[0]['total'],
                'SHF_Total_IP' : SHF_Total_IP[0]['total'],
                'SHF_Total_PWD' : SHF_Total_PWD[0]['total'],
                'SHF_Total_Youth' : SHF_Total_Youth[0]['total'],
                'SHF_Total_SC' : SHF_Total_SC[0]['total'],
                'SHF_byRegion' : {
                    'labels' : ['R-8','R-9','R-10','R-11','R-12','R-13','BARMM'],
                    'data' : SHF_allRegion,
                    'background_colors' : background_colors
                },
                'SHF_PC_data' : {
                    'labels' : ['Cacao','Coconut','Coffee','PFN'],
                    'data' : SHF_PC_data,
                    'background_colors' : background_colors_comm
                },
                'SHF_HH_Head_data' : {
                    'labels' : ['Male','Female','Untagged'],
                    'data' : SHF_total_HH_head_data,
                    'background_colors' : background_colors
                }
            },
            'FO' : {
                'FO_Total' : FO_Total[0]['total'],
                'FO_Total_Coop' : FO_Total_Coop[0]['total'],
                'FO_Total_Assoc' : FO_Total_Assoc[0]['total'],
                'FO_Total_Members' : FO_Total_Members[0]['total'],
                'FO_Total_Male' : FO_Total_Male[0]['total'],
                'FO_Total_Female' : FO_Total_Female[0]['total'],
                'FO_byRegion' : {
                    'labels' : ['R-8','R-9','R-10','R-11','R-12','R-13','BARMM'],
                    'data' : FO_allRegion,
                    'background_colors' : background_colors
                },
                'FO_byOrgType' : {
                    'labels' : ['Association','Cooperative','Others'],
                    'data' : FO_byOrgType,
                    'background_colors' : background_colors
                },
                'FO_PC_data' : {
                    'labels' : ['Cacao','Coconut','Coffee','PFN'],
                    'data' : FO_PC_data,
                    'background_colors' : background_colors_comm
                }
            },
            'MSME' : {
                'MSME_Total' : MSME_Total[0]['total'],
                'MSME_byRegion' : {
                    'labels' : ['R-8','R-9','R-10','R-11','R-12','R-13','BARMM'],
                    'data' : MSME_allRegion,
                    'background_colors' : background_colors
                },
                'MSME_PC_data' : {
                    'labels' : ['Micro','Small','Medium','Large'],
                    'data' : MSME_PC_data,
                    'background_colors' : background_colors
                },
                'MSME_IC_data' : {
                    'labels' : ['Cacao','Coconut','Coffee','PFN'],
                    'data' : MSME_IC_data,
                    'background_colors' : background_colors_comm
                }
            },
            'FMI' : FMI_data
        }

        return jsonify(data)