from flask import flash
import Configurations as c
from modules.Connections import mysql

db = mysql(*c.DB_CRED)
db.err_page = 0

def update(request):

    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        position_firm = request.form['position_firm']
        member_indegenous = request.form['member_indegenous']
        sex = request.form.get('sex')
        age = request.form['age']
        contact_details = request.form['contact_details']
        email_add = request.form['email_add']
        vc_stakeholders = request.form.get('vc_stakeholders')
        industry_cluster = request.form.get('industry_cluster')
        pfn_specify = request.form['pfn_specify']
        reg_businessname = request.form['reg_businessname']
        business_addr = request.form['business_addr']
        form_interprise = request.form.get('form_interprise')
        interprise_other = request.form.get('interprise_other')
        issued_by_business_reg = request.form.get('issued_by_business_reg')
        expired_date_business_reg = request.form.get('expired_date_business_reg')
        issued_by_product_reg = request.form.get('issued_by_product_reg')
        expired_date_product_reg = request.form.get('expired_date_product_reg')
        issued_by_cert_reg = request.form.get('issued_by_cert_reg')
        expired_date_cert_reg = request.form.get('expired_date_cert_reg')
        issued_by_lic_op = request.form.get('issued_by_lic_op')
        expired_date_lic_op = request.form.get('expired_date_lic_op')
        iso_cert_specific = request.form.get('iso_cert_specific')
        issued_by_iso_cert = request.form.get('issued_by_iso_cert')
        expired_date_iso_cert = request.form.get('expired_date_iso_cert')
        issued_by_gapgmp_cert = request.form.get('issued_by_gapgmp_cert')
        expired_date_gapgmp_cert = request.form.get('expired_date_gapgmp_cert')
        issued_by_organic = request.form.get('issued_by_organic')
        expired_date_organic = request.form.get('expired_date_organic')
        issued_by_halal = request.form.get('issued_by_halal')
        expired_date_halal = request.form.get('expired_date_halal')
        other_cert_specify = request.form.get('other_cert_specify')
        issued_by_other_cert = request.form.get('issued_by_other_cert')
        expired_date_other_cert = request.form.get('expired_date_other_cert')
        none_of_the_above = request.form.get('none_of_the_above')
        type_enterprise = request.form.get('type_enterprise')
        store_capacity_organic = request.form.get('store_capacity_organic')
        store_capacity_synthetic = request.form.get('store_capacity_synthetic')
        potential_organic = request.form.get('potential_organic')
        potential_synthetic = request.form.get('potential_synthetic')
        other_info_organic = request.form.get('other_info_organic')
        other_info_synthetic = request.form.get('other_info_synthetic')
        store_capacity_pesticides = request.form.get('store_capacity_pesticides')
        store_capacity_herbicides = request.form.get('store_capacity_herbicides')
        potential_pesticides = request.form.get('potential_pesticides')
        potential_herbicides = request.form.get('potential_herbicides')
        other_info_pesticides = request.form.get('other_info_pesticides')
        other_info_herbicides = request.form.get('other_info_herbicides')
        store_capacity_vermicast_compost = request.form.get('store_capacity_vermicast_compost')
        potential_vermicast_compost = request.form.get('potential_vermicast_compost')
        other_info_vermicast_compost = request.form.get('other_info_vermicast_compost')
        store_capacity_seedlings = request.form.get('store_capacity_seedlings')
        potential_seedlings = request.form.get('potential_seedlings')
        other_info_seedlings = request.form.get('other_info_seedlings')
        others_specific_products = request.form.get('others_specific_products')
        store_capacity_others_specific_products = request.form.get('store_capacity_others_specific_products')
        potential_others_specific_products = request.form.get('potential_others_specific_products')
        other_info_others_specific_products = request.form.get('other_info_others_specific_products')
        area_capacity_drying = request.form.get('area_capacity_drying')
        potential_exp_drying = request.form.get('potential_exp_drying')
        other_info_drying = request.form.get('other_info_drying')
        area_capacity_storage_hauling = request.form.get('area_capacity_storage_hauling')
        potential_exp_storage_hauling = request.form.get('potential_exp_storage_hauling')
        other_info_storage_hauling = request.form.get('other_info_storage_hauling')
        area_capacity_storage = request.form.get('area_capacity_storage')
        potential_exp_storage = request.form.get('potential_exp_storage')
        other_info_storage = request.form.get('other_info_storage')
        current_capacity_semi_processing = request.form.get('current_capacity_semi_processing')
        potential_exp_semi_processing = request.form.get('potential_exp_semi_processing')
        other_info_semi_processing = request.form.get('other_info_semi_processing')
        current_capacity_final_product = request.form.get('current_capacity_final_product')
        potential_exp_final_product = request.form.get('potential_exp_final_product')
        other_info_final_product = request.form.get('other_info_final_product')
        volume_consolidation = request.form.get('volume_consolidation')
        potential_consolidation = request.form.get('potential_consolidation')
        other_info_consolidation = request.form.get('other_info_consolidation')
        production_pack_label = request.form.get('production_pack_label')
        potential_pack_label = request.form.get('potential_pack_label')
        other_info_pack_label = request.form.get('other_info_pack_label')
        loan_portfo_micro_financing = request.form.get('loan_portfo_micro_financing')
        potential_micro_financing = request.form.get('potential_micro_financing')
        other_info_micro_financing = request.form.get('other_info_micro_financing')
        loan_portfo_insurance = request.form.get('loan_portfo_insurance')
        potential_insurance = request.form.get('potential_insurance')
        other_info_insurance = request.form.get('other_info_insurance')
        prodsales_product_service = request.form.get('prodsales_product_service')
        prodsales_sales_vol = request.form.get('prodsales_sales_vol')
        prodsales_unit_selling = request.form.get('prodsales_unit_selling')
        prodsales_unit_measurement = request.form.get('prodsales_unit_measurement')
        prodsales_payment_terms = request.form.get('prodsales_payment_terms')
        prodsales_product_service2 = request.form.get('prodsales_product_service2')
        prodsales_sales_vol2 = request.form.get('prodsales_sales_vol2')
        prodsales_unit_selling2 = request.form.get('prodsales_unit_selling2')
        prodsales_unit_measurement2 = request.form.get('prodsales_unit_measurement2')
        prodsales_payment_terms2 = request.form.get('prodsales_payment_terms2')
        prodsales_product_service3 = request.form.get('prodsales_product_service3')
        prodsales_sales_vol3 = request.form.get('prodsales_sales_vol3')
        prodsales_unit_selling3 = request.form.get('prodsales_unit_selling3')
        prodsales_unit_measurement3 = request.form.get('prodsales_unit_measurement3')
        prodsales_payment_terms3 = request.form.get('prodsales_payment_terms3')
        direct_farm = request.form.get('direct_farm')
        public_market = request.form.get('public_market')
        trader_conso = request.form.get('trader_conso')
        raw_materials = request.form.get('raw_materials')
        volume_supply = request.form.get('volume_supply')
        quality_requirement = request.form.get('quality_requirement')
        unit_measurement_raw = request.form.get('unit_measurement_raw')
        raw_materials2 = request.form.get('raw_materials2')
        volume_supply2 = request.form.get('volume_supply2')
        quality_requirement2 = request.form.get('quality_requirement2')
        unit_measurement_raw2 = request.form.get('unit_measurement_raw2')
        raw_materials3 = request.form.get('raw_materials3')
        volume_supply3 = request.form.get('volume_supply3')
        quality_requirement3 = request.form.get('quality_requirement3')
        unit_measurement_raw3 = request.form.get('unit_measurement_raw3')
        distrib_point_local_cust = request.form.get('distrib_point_local_cust')
        sales_vol_local_cust = request.form.get('sales_vol_local_cust')
        payment_terms_local_cust = request.form.get('payment_terms_local_cust')
        distrib_point_middleman = request.form.get('distrib_point_middleman')
        sales_vol_middleman = request.form.get('sales_vol_middleman')
        payment_terms_middleman = request.form.get('payment_terms_middleman')
        distrib_point_export = request.form.get('distrib_point_export')
        sales_vol_export = request.form.get('sales_vol_export')
        payment_terms_export = request.form.get('payment_terms_export')
        others_specify_marketing = request.form.get('others_specify_marketing')
        distrib_point_others_specify_marketing = request.form.get('distrib_point_others_specify_marketing')
        sales_vol_others_specify_marketing = request.form.get('sales_vol_others_specify_marketing')
        payment_terms_others_specify_marketing = request.form.get('payment_terms_others_specify_marketing')
        inhouse_num_workersmale = request.form.get('inhouse_num_workersmale')
        inhouse_num_workersfemale = request.form.get('inhouse_num_workersfemale')
        inhouse_memb_ip_group = request.form.get('inhouse_memb_ip_group')
        inhouse_ave_workdays = request.form.get('inhouse_ave_workdays')
        inhouse_ave_salary = request.form.get('inhouse_ave_salary')
        sub_cont_num_workersmale = request.form.get('sub_cont_num_workersmale')
        sub_cont_num_workersfemale = request.form.get('sub_cont_num_workersfemale')
        sub_cont_memb_ip_group = request.form.get('sub_cont_memb_ip_group')
        sub_cont_ave_workdays = request.form.get('sub_cont_ave_workdays')
        sub_cont_ave_salary = request.form.get('sub_cont_ave_salary')
        piece_rate_num_workersmale = request.form.get('piece_rate_num_workersmale')
        piece_rate_num_workersfemale = request.form.get('piece_rate_num_workersfemale')
        piece_rate_memb_ip_group = request.form.get('piece_rate_memb_ip_group')
        piece_rate_ave_workdays = request.form.get('piece_rate_ave_workdays')
        piece_rate_ave_salary = request.form.get('piece_rate_ave_salary')
        total_num_workersmale = request.form.get('total_num_workersmale')
        total_num_workersfemale = request.form.get('total_num_workersfemale')
        total_memb_ip_group = request.form.get('total_memb_ip_group')
        total_ave_workdays = request.form.get('total_ave_workdays')
        total_ave_salary = request.form.get('total_ave_salary')
        form_interprise2 = request.form.get('form_interprise2')
        ifyes_form_interprise = request.form.get('ifyes_form_interprise')
        pricing = request.form.get('pricing')
        ifyes_pricing = request.form.get('ifyes_pricing')
        quality_raw = request.form.get('quality_raw')
        ifyes_quality_raw = request.form.get('ifyes_quality_raw')
        quality_final_prod = request.form.get('quality_final_prod')
        ifyes_quality_final_prod = request.form.get('ifyes_quality_final_prod')
        other_specifyc3 = request.form.get('other_specifyc3')
        existing_comm = request.form.get('existing_comm')
        ifyes_existing_comm = request.form.get('ifyes_existing_comm')
        prov_supp_assis = request.form.get('prov_supp_assis')
        ifyes_prov_supp_assis = request.form.get('ifyes_prov_supp_assis')
        business_prodc3 = request.form.get('business_prodc3')
        ifyes_business_prodc3 = request.form.get('ifyes_business_prodc3')
        ifnoc3 = request.form.get('ifnoc3')
        capability = request.form.get('capability')
        tech_equip = request.form.get('tech_equip')
        access_market = request.form.get('access_market')
        commu_key_part = request.form.get('commu_key_part')
        political = request.form.get('political')
        chamber_commerce = request.form.get('chamber_commerce')
        trade_assoc = request.form.get('trade_assoc')
        coopera = request.form.get('coopera')
        commu_key_part2 = request.form.get('commu_key_part2')
        other_orgs_checkbox = request.form.get('other_orgs_checkbox')
        other_orgs_pls_spec = request.form.get('other_orgs_pls_spec')
        name_org = request.form.get('name_org')
        location_org = request.form.get('location_org')
        member_livelihood = request.form.get('member_livelihood')
        ifyes_member_livelihood = request.form.get('ifyes_member_livelihood')
        what_cluster_industry = request.form.get('what_cluster_industry')
        sql = """UPDATE form_c
               SET name='{}', position_firm='{}', member_indegenous='{}', sex='{}', age='{}', contact_details='{}', email_add='{}', vc_stakeholders='{}', industry_cluster='{}', pfn_specify='{}', reg_businessname='{}', business_addr='{}', form_interprise='{}', interprise_other='{}', issued_by_business_reg='{}', expired_date_business_reg='{}', issued_by_product_reg='{}', expired_date_product_reg='{}', issued_by_cert_reg='{}', expired_date_cert_reg='{}', issued_by_lic_op='{}', expired_date_lic_op='{}', iso_cert_specific='{}', issued_by_iso_cert='{}', expired_date_iso_cert='{}',
                issued_by_gapgmp_cert='{}', expired_date_gapgmp_cert='{}', issued_by_organic='{}', expired_date_organic='{}', issued_by_halal='{}', expired_date_halal='{}', other_cert_specify='{}',
                 issued_by_other_cert='{}', expired_date_other_cert='{}', none_of_the_above='{}', type_enterprise='{}', store_capacity_organic='{}', store_capacity_synthetic='{}', potential_organic='{}',
                  potential_synthetic='{}', other_info_organic='{}', other_info_synthetic='{}', store_capacity_pesticides='{}', store_capacity_herbicides='{}', potential_pesticides='{}', potential_herbicides='{}',
                   other_info_pesticides='{}', other_info_herbicides='{}', store_capacity_vermicast_compost='{}', potential_vermicast_compost='{}', other_info_vermicast_compost='{}', store_capacity_seedlings='{}',
                    potential_seedlings='{}', other_info_seedlings='{}', others_specific_products='{}', store_capacity_others_specific_products='{}', potential_others_specific_products='{}',
                     other_info_others_specific_products='{}', area_capacity_drying='{}', potential_exp_drying='{}', other_info_drying='{}', area_capacity_storage_hauling='{}', potential_exp_storage_hauling='{}',
                      other_info_storage_hauling='{}', area_capacity_storage='{}', potential_exp_storage='{}',other_info_storage='{}', current_capacity_semi_processing='{}', potential_exp_semi_processing='{}', other_info_semi_processing='{}', current_capacity_final_product='{}',
                       potential_exp_final_product='{}', other_info_final_product='{}', volume_consolidation='{}', potential_consolidation='{}', other_info_consolidation='{}', production_pack_label='{}',
                        potential_pack_label='{}', other_info_pack_label='{}', loan_portfo_micro_financing='{}', potential_micro_financing='{}', other_info_micro_financing='{}', loan_portfo_insurance='{}', 
                        potential_insurance='{}', other_info_insurance='{}', prodsales_product_service='{}', prodsales_sales_vol='{}', prodsales_unit_selling='{}', prodsales_unit_measurement='{}',prodsales_payment_terms='{}',
                         prodsales_product_service2='{}', prodsales_sales_vol2='{}', prodsales_unit_selling2='{}', prodsales_unit_measurement2='{}',prodsales_payment_terms2='{}', prodsales_product_service3='{}', prodsales_sales_vol3='{}', 
                         prodsales_unit_selling3='{}', prodsales_unit_measurement3='{}',prodsales_payment_terms3='{}', direct_farm='{}', public_market='{}', trader_conso='{}', raw_materials='{}', volume_supply='{}', quality_requirement='{}', 
                         unit_measurement_raw='{}', raw_materials2='{}', volume_supply2='{}', quality_requirement2='{}', unit_measurement_raw2='{}', raw_materials3='{}', volume_supply3='{}', quality_requirement3='{}', 
                         unit_measurement_raw3='{}', distrib_point_local_cust='{}', sales_vol_local_cust='{}', payment_terms_local_cust='{}', distrib_point_middleman='{}', sales_vol_middleman='{}', payment_terms_middleman='{}', 
                         distrib_point_export='{}', sales_vol_export='{}', payment_terms_export='{}', others_specify_marketing='{}', distrib_point_others_specify_marketing='{}', sales_vol_others_specify_marketing='{}', 
                         payment_terms_others_specify_marketing='{}', inhouse_num_workersmale='{}',inhouse_num_workersfemale='{}', inhouse_memb_ip_group='{}', inhouse_ave_workdays='{}', inhouse_ave_salary='{}', sub_cont_num_workersmale='{}',sub_cont_num_workersfemale='{}', sub_cont_memb_ip_group='{}', 
                         sub_cont_ave_workdays='{}', sub_cont_ave_salary='{}', piece_rate_num_workersmale='{}',piece_rate_num_workersfemale='{}', piece_rate_memb_ip_group='{}', piece_rate_ave_workdays='{}', piece_rate_ave_salary='{}', total_num_workersmale='{}', total_num_workersfemale='{}',
                         total_memb_ip_group='{}', total_ave_workdays='{}', total_ave_salary='{}', form_interprise2='{}', ifyes_form_interprise='{}', pricing='{}', ifyes_pricing='{}', quality_raw='{}', ifyes_quality_raw='{}', quality_final_prod='{}',
                         ifyes_quality_final_prod='{}', other_specifyc3='{}', existing_comm='{}', ifyes_existing_comm='{}', prov_supp_assis='{}', ifyes_prov_supp_assis='{}', business_prodc3='{}', ifyes_business_prodc3='{}', ifnoc3='{}', 
                         capability='{}', tech_equip='{}', access_market='{}', commu_key_part='{}', political='{}', chamber_commerce='{}', trade_assoc='{}', coopera='{}', commu_key_part2='{}', other_orgs_checkbox='{}', other_orgs_pls_spec='{}',
                          name_org='{}', location_org='{}', member_livelihood='{}', ifyes_member_livelihood='{}', what_cluster_industry='{}'
               WHERE id={}
            """.format(name ,position_firm ,member_indegenous ,sex ,age ,contact_details ,email_add ,vc_stakeholders , industry_cluster ,pfn_specify , reg_businessname ,business_addr ,form_interprise , interprise_other ,issued_by_business_reg ,expired_date_business_reg ,issued_by_product_reg ,expired_date_product_reg , issued_by_cert_reg ,expired_date_cert_reg ,issued_by_lic_op ,expired_date_lic_op ,  iso_cert_specific ,issued_by_iso_cert ,expired_date_iso_cert ,issued_by_gapgmp_cert ,expired_date_gapgmp_cert , issued_by_organic ,expired_date_organic , issued_by_halal , expired_date_halal ,other_cert_specify ,issued_by_other_cert , expired_date_other_cert ,  none_of_the_above ,type_enterprise , store_capacity_organic ,store_capacity_synthetic , potential_organic ,potential_synthetic ,  other_info_organic ,other_info_synthetic , store_capacity_pesticides ,store_capacity_herbicides ,potential_pesticides , potential_herbicides , other_info_pesticides ,other_info_herbicides ,store_capacity_vermicast_compost , potential_vermicast_compost ,  other_info_vermicast_compost , store_capacity_seedlings , potential_seedlings ,  other_info_seedlings , others_specific_products , store_capacity_others_specific_products ,  potential_others_specific_products ,other_info_others_specific_products ,  area_capacity_drying , potential_exp_drying , other_info_drying ,area_capacity_storage_hauling ,potential_exp_storage_hauling ,other_info_storage_hauling,area_capacity_storage ,potential_exp_storage ,other_info_storage ,current_capacity_semi_processing , potential_exp_semi_processing ,other_info_semi_processing ,current_capacity_final_product ,potential_exp_final_product ,  other_info_final_product , volume_consolidation , potential_consolidation ,  other_info_consolidation , production_pack_label ,potential_pack_label , other_info_pack_label ,loan_portfo_micro_financing ,  potential_micro_financing ,other_info_micro_financing ,loan_portfo_insurance ,potential_insurance ,  other_info_insurance , prodsales_product_service ,prodsales_sales_vol ,  prodsales_unit_selling ,prodsales_unit_measurement ,prodsales_payment_terms ,  prodsales_product_service2 ,prodsales_sales_vol2 , prodsales_unit_selling2 ,  prodsales_unit_measurement2 ,  prodsales_payment_terms2 , prodsales_product_service3 ,prodsales_sales_vol3 , prodsales_unit_selling3 ,  prodsales_unit_measurement3 ,  prodsales_payment_terms3 , direct_farm , public_market ,trader_conso ,raw_materials ,volume_supply ,quality_requirement ,  unit_measurement_raw , raw_materials2 ,  volume_supply2 ,  quality_requirement2 , unit_measurement_raw2 ,raw_materials3 ,  volume_supply3 ,  quality_requirement3 , unit_measurement_raw3 ,distrib_point_local_cust , sales_vol_local_cust , payment_terms_local_cust , distrib_point_middleman ,  sales_vol_middleman ,  payment_terms_middleman ,  distrib_point_export , sales_vol_export ,payment_terms_export , others_specify_marketing , distrib_point_others_specify_marketing ,sales_vol_others_specify_marketing ,payment_terms_others_specify_marketing ,inhouse_num_workersmale ,  inhouse_num_workersfemale ,inhouse_memb_ip_group ,inhouse_ave_workdays , inhouse_ave_salary ,sub_cont_num_workersmale , sub_cont_num_workersfemale ,sub_cont_memb_ip_group ,sub_cont_ave_workdays ,sub_cont_ave_salary ,  piece_rate_num_workersmale,piece_rate_num_workersfemale ,piece_rate_memb_ip_group , piece_rate_ave_workdays ,  piece_rate_ave_salary ,total_num_workersmale ,total_num_workersfemale ,  total_memb_ip_group ,  total_ave_workdays ,total_ave_salary ,form_interprise2 ,ifyes_form_interprise ,pricing , ifyes_pricing ,quality_raw , ifyes_quality_raw ,quality_final_prod ,ifyes_quality_final_prod , other_specifyc3 , existing_comm ,ifyes_existing_comm ,  prov_supp_assis , ifyes_prov_supp_assis ,business_prodc3 , ifyes_business_prodc3 ,ifnoc3 ,  capability ,  tech_equip ,  access_market ,commu_key_part ,  political ,chamber_commerce ,trade_assoc , coopera , commu_key_part2 , other_orgs_checkbox ,  other_orgs_pls_spec ,  name_org ,location_org ,member_livelihood ,ifyes_member_livelihood ,  what_cluster_industry, id)
        db.err_page = "asdasd"
        last_row_update_id = db.do(sql)
        if(last_row_update_id["response"]=="error"):
            flash(f"An error occured !", "error")
            print(str(last_row_update_id))
        else:
            flash(f"Data Updated! ", "success")
        # return redirect(url_for('formcdashboard'))
        return(last_row_update_id)