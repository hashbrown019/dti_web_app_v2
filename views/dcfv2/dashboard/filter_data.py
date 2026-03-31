from flask import flash,render_template,redirect,session
import Configurations as c
from modules.Connections import mysql
from flask_session import Session
from werkzeug.utils import secure_filename


db = mysql(*c.DB_CRED)
db.err_page = 0
def is_on_session(): return ('USER_DATA' in session)

def data_filter(request):
    # Extract filter parameters
    if request.method == 'POST':
        filter1 = request.form.get('filter1')
        filter2 = request.form.get('filter2')
        filter3 = request.form.get('filter3')
        filter4 = request.form.get('filter4')
    else:
        filter1 = filter2 = filter3 = filter4 = None
    
    raw_data = db.select("""
        SELECT 
            industry_cluster,
            form_interprise,
            sex,
            business_addr,
            interprise_other,
            pfn_specify
        FROM form_c
        WHERE industry_cluster IS NOT NULL 
           OR sex IS NOT NULL 
           OR business_addr IS NOT NULL
    """)
    
    # Get full datatable for backward compatibility
    datatable = db.select("SELECT * FROM form_c")
    
    # Build lookup results in Python (O(1) access instead of DB queries)
    # Industry + Enterprise type
    coffee_singlesole = [r for r in raw_data if r.get('industry_cluster') == 'coffee' and r.get('form_interprise') == 'Single/Sole']
    cacao_singlesole = [r for r in raw_data if r.get('industry_cluster') == 'cacao' and r.get('form_interprise') == 'Single/Sole']
    coconut_singlesole = [r for r in raw_data if r.get('industry_cluster') == 'coconut' and r.get('form_interprise') == 'Single/Sole']
    pfn_singlesole = [r for r in raw_data if r.get('industry_cluster') not in [None, 'cacao', 'coconut', 'coffee', '', ' '] and r.get('form_interprise') == 'Single/Sole']
    
    coffee_partnership = [r for r in raw_data if r.get('industry_cluster') == 'coffee' and r.get('form_interprise') == 'partnership']
    cacao_partnership = [r for r in raw_data if r.get('industry_cluster') == 'cacao' and r.get('form_interprise') == 'partnership']
    coconut_partnership = [r for r in raw_data if r.get('industry_cluster') == 'coconut' and r.get('form_interprise') == 'partnership']
    pfn_partnership = [r for r in raw_data if r.get('industry_cluster') not in [None, 'cacao', 'coconut', 'coffee', '', ' '] and r.get('form_interprise') == 'partnership']
    
    coffee_corporation = [r for r in raw_data if r.get('industry_cluster') == 'coffee' and r.get('form_interprise') == 'corporation']
    cacao_corporation = [r for r in raw_data if r.get('industry_cluster') == 'cacao' and r.get('form_interprise') == 'corporation']
    coconut_corporation = [r for r in raw_data if r.get('industry_cluster') == 'coconut' and r.get('form_interprise') == 'corporation']
    pfn_corporation = [r for r in raw_data if r.get('industry_cluster') not in [None, 'cacao', 'coconut', 'coffee', '', ' '] and r.get('form_interprise') == 'corporation']
    
    # Calculate totals
    totalsinglesole = len(coffee_singlesole) + len(cacao_singlesole) + len(coconut_singlesole) + len(pfn_singlesole)
    totalpartnership = len(coffee_partnership) + len(cacao_partnership) + len(coconut_partnership) + len(pfn_partnership)
    totalcorporation = len(coffee_corporation) + len(cacao_corporation) + len(coconut_corporation) + len(pfn_corporation)
    
    # Industry counts
    count_coffee_single = len(coffee_singlesole)
    count_cacao_single = len(cacao_singlesole)
    count_coconut_single = len(coconut_singlesole)
    count_pfn_single = len(pfn_singlesole)
    total_industrysingle = count_coffee_single + count_cacao_single + count_coconut_single + count_pfn_single
    
    count_coffeepart = len(coffee_partnership)
    count_cacaopart = len(cacao_partnership)
    count_coconutpart = len(coconut_partnership)
    count_pfnpart = len(pfn_partnership)
    total_industrypart = count_coffeepart + count_cacaopart + count_coconutpart + count_pfnpart
    
    count_coffeecorp = len(coffee_corporation)
    count_cacaocorp = len(cacao_corporation)
    count_coconutcorp = len(coconut_corporation)
    count_pfncorp = len(pfn_corporation)
    total_industrycorp = count_coffeecorp + count_cacaocorp + count_coconutcorp + count_pfncorp
    
    # Gender filters
    male_singlesole = [r for r in raw_data if r.get('sex') == 'male' and r.get('form_interprise') == 'Single/Sole']
    female_singlesole = [r for r in raw_data if r.get('sex') == 'female' and r.get('form_interprise') == 'Single/Sole']
    male_partnership = [r for r in raw_data if r.get('sex') == 'male' and r.get('form_interprise') == 'partnership']
    female_partnership = [r for r in raw_data if r.get('sex') == 'female' and r.get('form_interprise') == 'partnership']
    male_corporation = [r for r in raw_data if r.get('sex') == 'male' and r.get('form_interprise') == 'corporation']
    female_corporation = [r for r in raw_data if r.get('sex') == 'female' and r.get('form_interprise') == 'corporation']
    
    count_male_singlesole = len(male_singlesole)
    count_female_singlesole = len(female_singlesole)
    count_malepartnership = len(male_partnership)
    count_femalepartnership = len(female_partnership)
    count_male_corporation = len(male_corporation)
    count_female_corporation = len(female_corporation)
    
    # Gender + Other enterprise type
    male_other = [r for r in raw_data if r.get('sex') == 'male' and r.get('interprise_other') and r.get('interprise_other') != '']
    female_other = [r for r in raw_data if r.get('sex') == 'female' and r.get('interprise_other') and r.get('interprise_other') != '']
    count_male_other = len(male_other)
    count_female_other = len(female_other)
    totalother = count_male_other + count_female_other
    
    # Industry + Other
    coffee_othersql = [r for r in raw_data if r.get('industry_cluster') == 'coffee' and r.get('interprise_other') and r.get('interprise_other') != '']
    cacao_othersql = [r for r in raw_data if r.get('industry_cluster') == 'cacao' and r.get('interprise_other') and r.get('interprise_other') != '']
    coconut_othersql = [r for r in raw_data if r.get('industry_cluster') == 'coconut' and r.get('interprise_other') and r.get('interprise_other') != '']
    pfn_othersql = [r for r in raw_data if r.get('pfn_specify') and r.get('pfn_specify') != '' and r.get('interprise_other') and r.get('interprise_other') != '']
    
    count_coffeeoth = len(coffee_othersql)
    count_cacaooth = len(cacao_othersql)
    count_coconutoth = len(coconut_othersql)
    count_pfnoth = len(pfn_othersql)
    total_industryoth = count_coffeeoth + count_cacaooth + count_coconutoth + count_pfnoth
    
    # Industry + Gender
    coffee_malesql = [r for r in raw_data if r.get('industry_cluster') == 'coffee' and r.get('sex') == 'male']
    cacao_malesql = [r for r in raw_data if r.get('industry_cluster') == 'cacao' and r.get('sex') == 'male']
    coconut_malesql = [r for r in raw_data if r.get('industry_cluster') == 'coconut' and r.get('sex') == 'male']
    pfn_malesql = [r for r in raw_data if r.get('industry_cluster') not in [None, 'cacao', 'coconut', 'coffee', '', ' '] and r.get('sex') == 'male']
    
    coffee_femalesql = [r for r in raw_data if r.get('industry_cluster') == 'coffee' and r.get('sex') == 'female']
    cacao_femalesql = [r for r in raw_data if r.get('industry_cluster') == 'cacao' and r.get('sex') == 'female']
    coconut_femalesql = [r for r in raw_data if r.get('industry_cluster') == 'coconut' and r.get('sex') == 'female']
    pfn_femalesql = [r for r in raw_data if r.get('industry_cluster') not in [None, 'cacao', 'coconut', 'coffee', '', ' '] and r.get('sex') == 'female']
    
    # Build region filters dynamically
    REGIONS = {
        'adn': 'agusan del norte', 
        'ads': 'agusan del sur', 
        'sds': 'surigao del sur', 
        'magui': 'maguindanao',
        'ns': 'northern samar', 
        'leyte': 'leyte', 
        'sleyte': 'southern leyte', 
        'mo': 'misamis oriental',
        'bukd': 'bukidnon', 
        'ldn': 'lanao del norte', 
        'nc': 'north cotabato', 
        'sk': 'sultan kudarat',
        'srng': 'sarangani', 
        'zdn': 'zamboanga del norte', 
        'zs': 'zamboanga sibugay', 
        'zds': 'zamboanga del sur',
        'ddo': 'davao de oro', 
        'do': 'davao oriental', 
        'ddn': 'davao del norte', 
        'dds': 'davao del sur', 
        'doc': 'davao occidental'
    }
    
    region_filters = {}
    for reg_code, reg_name in REGIONS.items():
        # Single/Sole
        region_filters[f"{reg_code}_singlesql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('form_interprise') == 'Single/Sole']
        # Partnership
        region_filters[f"{reg_code}_partsql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('form_interprise') == 'partnership']
        # Corporation
        region_filters[f"{reg_code}_corpsql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('form_interprise') == 'corporation']
        # Other
        region_filters[f"{reg_code}_othersql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('interprise_other') and r.get('interprise_other') != '']
        # Male
        region_filters[f"{reg_code}_malesql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('sex') == 'male']
        # Female
        region_filters[f"{reg_code}_femalesql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('sex') == 'female']
        # Coffee
        region_filters[f"{reg_code}_coffeesql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('industry_cluster') == 'coffee']
        # Cacao
        region_filters[f"{reg_code}_cacaosql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('industry_cluster') == 'cacao']
        # Coconut
        region_filters[f"{reg_code}_coconutsql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('industry_cluster') == 'coconut']
        # PFN (other industries)
        region_filters[f"{reg_code}_pfnsql"] = [r for r in raw_data 
            if reg_name.lower() in (r.get('business_addr', '') or '').lower() 
            and r.get('industry_cluster') not in [None, 'cacao', 'coconut', 'coffee', '', ' ']]
    
    # Region totals
    total_adn_addr = len(region_filters.get('adn_singlesql', [])) + len(region_filters.get('adn_partsql', [])) + len(region_filters.get('adn_corpsql', [])) + len(region_filters.get('adn_othersql', []))
    total_ads_addr = len(region_filters.get('ads_singlesql', [])) + len(region_filters.get('ads_partsql', [])) + len(region_filters.get('ads_corpsql', [])) + len(region_filters.get('ads_othersql', []))
    total_sds_addr = len(region_filters.get('sds_singlesql', [])) + len(region_filters.get('sds_partsql', [])) + len(region_filters.get('sds_corpsql', [])) + len(region_filters.get('sds_othersql', []))
    
    total_coffeeaddr = sum(len(region_filters.get(f"{r}_coffeesql", [])) for r in REGIONS.keys())
    total_cacaoaddr = sum(len(region_filters.get(f"{r}_cacaosql", [])) for r in REGIONS.keys())
    total_coconutaddr = sum(len(region_filters.get(f"{r}_coconutsql", [])) for r in REGIONS.keys())
    total_pfnaddr = sum(len(region_filters.get(f"{r}_pfnsql", [])) for r in REGIONS.keys())
    
    maless = male_singlesole
    femaless = female_singlesole
    
    # Build and return complete result dictionary
    return {
        'count_male_singlesole': count_male_singlesole,
        'count_female_singlesole': count_female_singlesole,
        'count_malepartnership': count_malepartnership,
        'count_femalepartnership': count_femalepartnership,
        'count_male_corporation': count_male_corporation,
        'count_female_corporation': count_female_corporation,
        'totalsinglesole': totalsinglesole,
        'totalpartnership': totalpartnership,
        'totalcorporation': totalcorporation,
        'count_male_other': count_male_other,
        'count_female_other': count_female_other,
        'totalother': totalother,
        'filter1': filter1,
        'filter2': filter2,
        'filter3': filter3,
        'filter4': filter4,
        'count_coffee_single': count_coffee_single,
        'count_cacao_single': count_cacao_single,
        'count_coconut_single': count_coconut_single,
        'count_pfn_single': count_pfn_single,
        'total_industrysingle': total_industrysingle,
        'count_coffeepart': count_coffeepart,
        'count_cacaopart': count_cacaopart,
        'count_coconutpart': count_coconutpart,
        'count_pfnpart': count_pfnpart,
        'total_industrypart': total_industrypart,
        'count_coffeecorp': count_coffeecorp,
        'count_cacaocorp': count_cacaocorp,
        'count_coconutcorp': count_coconutcorp,
        'count_pfncorp': count_pfncorp,
        'total_industrycorp': total_industrycorp,
        'count_coffeeoth': count_coffeeoth,
        'count_cacaooth': count_cacaooth,
        'count_coconutoth': count_coconutoth,
        'count_pfnoth': count_pfnoth,
        'total_industryoth': total_industryoth,
        'coffee_malesql': coffee_malesql,
        'cacao_malesql': cacao_malesql,
        'coconut_malesql': coconut_malesql,
        'pfn_malesql': pfn_malesql,
        'coffee_femalesql': coffee_femalesql,
        'cacao_femalesql': cacao_femalesql,
        'coconut_femalesql': coconut_femalesql,
        'pfn_femalesql': pfn_femalesql,
        'coffee_othersql': coffee_othersql,
        'cacao_othersql': cacao_othersql,
        'coconut_othersql': coconut_othersql,
        'pfn_othersql': pfn_othersql,
        'datatable': datatable,
        'maless': maless,
        'femaless': femaless,
        'total_adn_addr': total_adn_addr,
        'total_ads_addr': total_ads_addr,
        'total_sds_addr': total_sds_addr,
        'total_coffeeaddr': total_coffeeaddr,
        'total_cacaoaddr': total_cacaoaddr,
        'total_coconutaddr': total_coconutaddr,
        'total_pfnaddr': total_pfnaddr,
        **region_filters,  # Unpack all region filter results
    }
