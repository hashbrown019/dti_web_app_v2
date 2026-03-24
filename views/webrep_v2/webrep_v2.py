from flask import Blueprint, abort, flash, render_template, render_template_string, request, session, redirect, jsonify, send_file, send_from_directory, Response
from flask_session import Session
from modules.Connections import mysql
from modules.Req_Brorn_util import string_websafe as STRS
import Configurations as c
from werkzeug.utils import secure_filename
import os
from modules.Req_Brorn_util import file_from_request
import urllib.parse
import requests


# from PIL import Image
from io import BytesIO
import base64
import json

from datetime import date, datetime
from modules.Req_Brorn_util import file_from_request
from views.dcfv2.dashboard.display_dataform import displayform

# from v2_view.core._dashboard import _main as dboard_main

# from docx2pdf import convert
# pip install docx2pdf

db = mysql(*c.DB_CRED)
db.err_page = 0

app = Blueprint("webrep_v2",__name__,template_folder='pages',static_folder='static')
# app = Blueprint("webrep",__name__,url_prefix='/webrep',template_folder='pages')

# app.register_blueprint(_dashboard.app)

g_site_key = '6LfL2icsAAAAALUPS-KvCMKYZZ8wtaMdDoO_vyw9'
g_secret_key = '6LfL2icsAAAAAHu2Oqlfz-uUwuzL5FTPc5D9t5Pk'
g_verify_url = 'https://www.google.com/recaptcha/api/siteverify'

app.secret_key = "dtirapid2025"

class _main:
    def is_on_session(): return ('USER_DATA' in session)
    def __init__(self, arg):super(_main, self).__init__();self.arg = arg

    # app.errorhandler(404)
    # def is_on_session(): return ('USER_DATA' in session)
    # ======================================================================================================
    
    
    def urldecode_lines_filter(s):
        if not s:
            return s
        lines = s.splitlines()
        decoded_lines = [urllib.parse.unquote(line) for line in lines]
        return "<br>".join(decoded_lines)

    # Register the filter with the blueprint
    app.add_app_template_filter(urldecode_lines_filter, 'urldecode_lines')

    @app.route("/webrep",methods=["POST","GET"])
    def home():
        if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
        print("databse = "+c.DB_CRED[3])
        db = mysql(*c.DB_CRED)
        return redirect("/hi_there?ver=dti_rapidgrowth_"+c.DB_CRED[3])

    @app.route("/hi_there",methods=["POST","GET"])
    def hi_there():
        
        if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
        # dashboard_data =  json.loads(dboard_main.system_page())
        # dashboard_data =  dboard_main.system_page()
        
        return render_template(
            "home/home.html",
            sliders_data=_main.getLatestArticles(),
            is_session =_main.is_on_session(),
            g_site_key = g_site_key,
            active_bar = "home",
            # dashboard_data=_main.analyticUpdates()
        )

    @app.route("/webrep_v2/directory", methods=["GET"])
    def directory():
        return render_template("directory/directory.html",
            is_session =_main.is_on_session(),
            g_site_key = g_site_key,
            active_bar = "whoweare",)
    
    @app.route("/webrep_v2/getBlobContent/<sectionName>", methods=["GET"])
    def getBlobContent(sectionName):
        base_dir = c.RECORDS+"../views/webrep_v2/pages/blob_content"
        filename = f"{sectionName}.html"
        with open(os.path.join(base_dir, filename)) as f:
            content = f.read()
        return render_template_string(content)

        # return base_dir+"/"+filename
        # return send_from_directory(base_dir, filename)
    
    @app.route("/webrep_v2/article/<article_id>",methods=["POST","GET"])
    def article(article_id):
        # user_data = ''
        # if 'USER_DATA' in session:
        #     user_data = session['USER_DATA'][0]
        
        # filter_str = '';
        # if user_data == '':
        #     filter_str = " AND status='posted' ";
        # else:
        #     if (user_data['job']!="Super Admin" ):
        #         filter_str = " AND "
        
        article = db.select("SELECT * FROM webrep_articles_v2 WHERE id={} AND removed=0".format(article_id))
        if not article:
            return "Article not found", 404
        article = article[0]
        
        article_postype = article['posttype']
        related_result = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='{}' AND status='posted' AND removed=0 LIMIT 3".format(article_postype))
        related_articles = []
        for row in related_result:
            row['postheader'] = urllib.parse.unquote(row['postheader'])
            row['postAuthor'] = urllib.parse.unquote(row['postAuthor'])
            related_articles.append(row)
        # article['postheader'] = urllib.parse.unquote(article['postheader'])
        # article['postContent'] = urllib.parse.unquote(article['postContent'])
        # article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
        # article['postRcu'] = urllib.parse.unquote(article['postRcu'])
        # article['postRcu'] = urllib.parse.unquote(article['postRcu'])
        # article['postcaption'] = urllib.parse.unquote(article['postcaption'])
        # article['postdescription'] = urllib.parse.unquote(article['postdescription'])
        
        return render_template("articles/page.html", article=article, related_articles=related_articles)

    @app.route("/webrep_v2/articles/delete/<ids>",methods=["POST","GET"])
    def delete_article(ids):
        update_del = db.do("UPDATE `webrep_articles_v2` SET `removed`='1' WHERE `id`='{}';".format(ids))
        print("deleting.....")
        print(update_del)
        return {"db_info":update_del}

    @app.route("/webrep_v2/articles/confirm/<ids>",methods=["POST","GET"])
    def confirm_article(ids):
        update_del = db.do("UPDATE `webrep_articles_v2` SET `status`='posted' WHERE `id`='{}';".format(ids))
        return {"db_info":update_del}

    @app.route("/webrep_v2/articles/revise/<ids>",methods=["POST","GET"])
    def revise_article(ids):
        update_del = db.do("UPDATE `webrep_articles_v2` SET `status`='revise' WHERE `id`='{}';".format(ids))
        return {"db_info":update_del}
    
    @app.route("/webrep/article/get_post_ind",methods=["POST","GET"])
    def get_post_ind():
        ids = request.form['article_id']
        return db.select("SELECT *, DATE_FORMAT(postDate, '%Y-%m-%d') AS postDate FROM webrep_articles_v2 WHERE id='{}' ORDER BY id DESC;".format(ids))

    @app.route("/webrep_v2/article/get_img/<img>",methods=["POST","GET"])
    def get_img(img):
        
        img = img.replace('C:fakepath', '').replace(" ","_").replace(")","").replace("(","")
        file_path = os.path.join(c.RECORDS, "objects", "webrep", img)
       
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return send_file( "static/img/no_img.png")
            # return send_from_directory(os.path.join(app.static_folder, "img"), "no_img.png")
            # return send_from_directory(os.path.join(app.static_folder, "img", "no_img.png"))

    @app.route("/embed_forum_talks/<f_id>",methods=["POST","GET"])
    def embed_forum_talks(f_id):
        if(_main.is_on_session()):
            forum = db.select("SELECT `webrep_forum_topics`.*, `users`.`name` as 'uploader', `users`.`profilepic`, `users`.`job` FROM `webrep_forum_topics` INNER JOIN `users` ON `webrep_forum_topics`.`created_by`= `users`.`id` WHERE `webrep_forum_topics`.`id`='{}';".format(f_id))
            return render_template(
				'forum/embed_forum.html',
				USER_DATA = session['USER_DATA'][0],
				forum = forum[0]
			)
        else:
            return redirect("/login?force_url=1")

    @app.route("/forum/send_comment",methods=["POST","GET"])
    def send_comment():
        print("  * send_comment")
        FILE_REQ = file_from_request(app)
        data = dict(request.form)
        key = [];val = [];args=""

        is_exist = len(db.select("SELECT * FROM `webrep_forum_comments` WHERE `id` ='{}' ;".format(request.form['id'])))
        if(is_exist==0):
            print(" >> Adding Forum")
            for datum in data:
                key.append("`{}`".format(datum))
                val.append("'{}'".format(data[datum]))
            sql = ('''INSERT INTO `webrep_forum_comments` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
        else:
            print(" >> Editing Forum")
            for datum in data:
                args += ",`{}`='{}'".format(datum,data[datum])
            sql = "UPDATE `webrep_forum_comments` SET  {}, `edit`='1' WHERE `id`='{}';".format(args[1:],request.form['id'])
            pass
        last_row_id = db.do(sql)
        return jsonify({"last_row_id":last_row_id})
    
    @app.route("/forum/send_comment_like/<com_id>",methods=["POST","GET"])
    def send_comment_like(com_id):
        sql = "UPDATE `webrep_forum_comments` SET `likes` = `likes` + 1 WHERE `id`='{}';".format(com_id)
        last_row_id = db.do(sql)
        return jsonify({"last_row_id":last_row_id})

    @app.route("/forum/delete_comment/<com_id>",methods=["POST","GET"])
    def delete_comment(com_id):
        sql = "UPDATE `webrep_forum_comments` SET `removed`='1' WHERE `id`='{}';".format(com_id)
        last_row_id = db.do(sql)
        return jsonify({"last_row_id":last_row_id})

    @app.route("/forum/get_comment/<com_id>",methods=["POST","GET"])
    def get_comment(com_id):
        if(_main.is_on_session()):
            comments = db.select("SELECT `webrep_forum_comments`.*, `users`.`name` as 'commenter', `users`.`id` as 'commenter_id', `users`.`profilepic` as 'profilepic', `users`.`job` FROM `webrep_forum_comments` INNER JOIN `users` ON `webrep_forum_comments`.`comment_by`= `users`.`id` WHERE `webrep_forum_comments`.`topic_id`='{}' ORDER BY `id` DESC;".format(com_id))
            return [comments,_main.get_topic_people(com_id)]
        else:
            return redirect("/login?force_url=1")

    @app.route("/forum/get_topic_people/<com_id>",methods=["POST","GET"])
    def get_topic_people(com_id):
        if(_main.is_on_session()):
            comments = db.select("SELECT `webrep_forum_comments`.`id` as 'first_comment_id', `users`.`name` as 'commenter' FROM `webrep_forum_comments` INNER JOIN `users` ON `webrep_forum_comments`.`comment_by` = `users`.`id` WHERE `webrep_forum_comments`.`topic_id` = '{}' GROUP BY `users`.`name`;".format(com_id))
            return comments
        else:
            return redirect("/login?force_url=1")

    def getLatestArticles():
        articles = db.select("SELECT * FROM webrep_articles_v2 WHERE status='posted' AND removed=0 ORDER BY id DESC LIMIT 6")
        data = []
        for article in articles:
            article['postheader'] = urllib.parse.unquote(article['postheader'])
            article['postContent'] = urllib.parse.unquote(article['postContent'])
            article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
            article['postRcu'] = urllib.parse.unquote(article['postRcu'])
            data.append(article)
        return data

    def analyticUpdates():
        
        # ======================================================================================================
        # SMALL HOLDER FARMERS
        # ======================================================================================================
        
        SHF_Total = db.select("SELECT COUNT(*) AS total FROM excel_import_form_a")
        SHF_Total_Male = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_Sex`='Male'")
        SHF_Total_Female = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_Sex`='Female'")
        SHF_Total_IP = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='IP'")
        SHF_Total_Youth = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='Youth'")
        SHF_Total_PWD = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='PWD'")
        SHF_Total_SC = db.select("SELECT COUNT(*) AS total FROM excel_import_form_a WHERE `frmer_prof_@_basic_Info_@_sectoral_data`='SC'")

        SHF_byRegion_8 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('8','xiii','region8','region 8')")
        SHF_byRegion_9 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('9','ix','region9','region 9')")
        SHF_byRegion_10 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('10','x','region10','region 10')")
        SHF_byRegion_11 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('11','xi','region11','region 11')")
        SHF_byRegion_12 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('12','xii','region12','region 12')")
        SHF_byRegion_13 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('13','xiii','region13','region 13')")
        SHF_byRegion_barmm = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM excel_import_form_a)) * 100 AS percTotal FROM excel_import_form_a WHERE `frmer_prof_@_frmer_addr_@_region` IN('BARMM')")
        
        SHF_allRegion = [float(SHF_byRegion_8[0]['percTotal']),float(SHF_byRegion_9[0]['percTotal']),float(SHF_byRegion_10[0]['percTotal']),float(SHF_byRegion_11[0]['percTotal']),float(SHF_byRegion_12[0]['percTotal']),float(SHF_byRegion_13[0]['percTotal']),float(SHF_byRegion_barmm[0]['percTotal'])]

        SHF_byComm_cacao = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cacao%'")
        SHF_byComm_coconut = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coconut%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Copra%'")
        SHF_byComm_coffee = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Coffee%'")
        SHF_byComm_pfn = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Banana Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%BananaCardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Cardava%' OR `frmer_prof_@_Farming_Basic_Info_@_primary_crop` LIKE '%Calamansi%'")
        SHF_byComm_untagged = db.select("SELECT COUNT(*) AS total  FROM excel_import_form_a WHERE `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cacao%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coconut%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Copra%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Coffee%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Banana Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%BananaCardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Cardava%' AND `frmer_prof_@_Farming_Basic_Info_@_primary_crop` NOT LIKE '%Calamansi%'")

        SHF_byComm_data = [SHF_byComm_cacao[0]['total'],SHF_byComm_coconut[0]['total'],SHF_byComm_coffee[0]['total'],SHF_byComm_pfn[0]['total'],SHF_byComm_untagged[0]['total']]
        
        SHF_total_HH_head_male = db.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` = 'Male' WHERE dl.db_table='dcf_capacity_building'")
        SHF_total_HH_head_female = db.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` = 'Female' WHERE dl.db_table='dcf_capacity_building'")
        SHF_total_HH_head_untagged = db.select("SELECT COUNT(*) AS total FROM __data_link_1 dl INNER JOIN excel_import_form_a eia ON eia.id = dl.link_to_id AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` != 'Male' AND eia.`frmer_prof_@_hh_Head_Info_@_head_hh_sex` != 'Female' WHERE dl.db_table='dcf_capacity_building'")
        
        SHF_total_HH_head_data = [SHF_total_HH_head_male[0]['total'],SHF_total_HH_head_female[0]['total'],SHF_total_HH_head_untagged[0]['total']];


        # ======================================================================================================
        # FARMER ORGANIZATION
        # ======================================================================================================
        FO_Total = db.select("SELECT COUNT(*) AS total FROM form_b")
        FO_Total_Coop = db.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Cooperative'")
        FO_Total_Assoc = db.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Association'")
        FO_Total_Others = db.select("SELECT COUNT(*) AS total FROM form_b WHERE types_of_organization='Others'")
        FO_Total_Members = db.select("SELECT SUM(organizational_total_overall) AS total FROM form_b")
        FO_Total_Male = db.select("SELECT SUM(organizational_total_male) AS total FROM form_b ")
        FO_Total_Female = db.select("SELECT SUM(organizational_total_female) AS total FROM form_b ")

        FO_byRegion_8 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU8','RCU 8')")
        FO_byRegion_9 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU9','RCU 9')")
        FO_byRegion_10 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU10','RCU 10')")
        FO_byRegion_11 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU11','RCU 11')")
        FO_byRegion_12 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU12','RCU 12')")
        FO_byRegion_13 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('RCU13','RCU 13')")
        FO_byRegion_barmm = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_b)) * 100 AS percTotal FROM form_b fb INNER JOIN users u ON u.id=fb.uploaded_by AND u.rcu IN('BARMM')")
        
        FO_allRegion = [float(FO_byRegion_8[0]['percTotal']),float(FO_byRegion_9[0]['percTotal']),float(FO_byRegion_10[0]['percTotal']),float(FO_byRegion_11[0]['percTotal']),float(FO_byRegion_12[0]['percTotal']),float(FO_byRegion_13[0]['percTotal']),float(FO_byRegion_barmm[0]['percTotal'])]
        FO_byOrgType = [FO_Total_Assoc[0]['total'],FO_Total_Coop[0]['total'],FO_Total_Others[0]['total']]
        
        FO_byComm_cacao = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Cacao%'")
        FO_byComm_coconut = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Coconut%' OR `organizational_commodity` LIKE '%Copra%'")
        FO_byComm_coffee = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Coffee%'")
        FO_byComm_pfn = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` LIKE '%Banana%' OR `organizational_commodity` LIKE '%Banana Cardava%' OR `organizational_commodity` LIKE '%BananaCardava%' OR `organizational_commodity` LIKE '%Cardava%' OR `organizational_commodity` LIKE '%Calamansi%'")
        FO_byComm_untagged = db.select("SELECT COUNT(*) AS total  FROM form_b WHERE `organizational_commodity` NOT LIKE '%Cacao%' AND `organizational_commodity` NOT LIKE '%Coconut%' AND `organizational_commodity` NOT LIKE '%Copra%' AND `organizational_commodity` NOT LIKE '%Coffee%' AND `organizational_commodity` NOT LIKE '%Banana%' AND `organizational_commodity` NOT LIKE '%Banana Cardava%' AND `organizational_commodity` NOT LIKE '%BananaCardava%' AND `organizational_commodity` NOT LIKE '%Cardava%' AND `organizational_commodity` NOT LIKE '%Calamansi%'")

        FO_byComm_data = [FO_byComm_cacao[0]['total'],FO_byComm_coconut[0]['total'],FO_byComm_coffee[0]['total'],FO_byComm_pfn[0]['total'],FO_byComm_untagged[0]['total']]

        # ======================================================================================================
        # MICRO, SMALL, MEDIUM ENTERPRISES
        # ======================================================================================================
        MSME_Total = db.select("SELECT COUNT(*) AS total FROM form_c")[0]['total']

        MSME_byRegion_8 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU8','RCU 8')")
        MSME_byRegion_9 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU9','RCU 9')")
        MSME_byRegion_10 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU10','RCU 10')")
        MSME_byRegion_11 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU11','RCU 11')")
        MSME_byRegion_12 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU12','RCU 12')")
        MSME_byRegion_13 = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('RCU13','RCU 13')")
        MSME_byRegion_barmm = db.select("SELECT COUNT(*) AS regionCount, (COUNT(*) / (SELECT COUNT(*) FROM form_c)) * 100 AS percTotal FROM form_c fc INNER JOIN users u ON u.id=fc.upload_by AND u.rcu IN('BARMM')")

        MSME_allRegion = [float(MSME_byRegion_8[0]['percTotal']),float(MSME_byRegion_9[0]['percTotal']),float(MSME_byRegion_10[0]['percTotal']),float(MSME_byRegion_11[0]['percTotal']),float(MSME_byRegion_12[0]['percTotal']),float(MSME_byRegion_13[0]['percTotal']),float(MSME_byRegion_barmm[0]['percTotal'])]
        
        MSME_byComm_cacao = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Cacao%'")
        MSME_byComm_coconut = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Coconut%' OR `industry_cluster` LIKE '%Copra%'")
        MSME_byComm_coffee = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Coffee%'")
        MSME_byComm_pfn = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` LIKE '%Banana%' OR `industry_cluster` LIKE '%Banana Cardava%' OR `industry_cluster` LIKE '%BananaCardava%' OR `industry_cluster` LIKE '%Cardava%' OR `industry_cluster` LIKE '%Calamansi%'")
        MSME_byComm_untagged = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `industry_cluster` NOT LIKE '%Cacao%' AND `industry_cluster` NOT LIKE '%Coconut%' AND `industry_cluster` NOT LIKE '%Copra%' AND `industry_cluster` NOT LIKE '%Coffee%' AND `industry_cluster` NOT LIKE '%Banana%' AND `industry_cluster` NOT LIKE '%Banana Cardava%' AND `industry_cluster` NOT LIKE '%BananaCardava%' AND `industry_cluster` NOT LIKE '%Cardava%' AND `industry_cluster` NOT LIKE '%Calamansi%'")
        MSME_byComm_data = [MSME_byComm_cacao[0]['total'],MSME_byComm_coconut[0]['total'],MSME_byComm_coffee[0]['total'],MSME_byComm_pfn[0]['total'],MSME_byComm_untagged[0]['total']]

        MSME_byType_micro = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Micro','Micro (3M below)')")
        MSME_byType_small = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Small','Small (3-15M)')")
        MSME_byType_medium = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Medium','Medium (15.1M-100M)')")
        MSME_byType_large = db.select("SELECT COUNT(*) AS total  FROM form_c WHERE `type_enterprise` IN ('Large','Large (Above 100M)')")
        MSME_byType_data = [MSME_byType_micro[0]['total'],MSME_byType_small[0]['total'],MSME_byType_medium[0]['total'],MSME_byType_large[0]['total']]
    
        background_colors = ["#629DDD","#A4BF7F","#A48BC1","#E2918F","#F4D470","#E8AA78","#A5D7D8","#7173A9","#77838E"]
        
        data = {
                "SHF_Total" : SHF_Total[0]["total"],
                "SHF_Total_Male" : SHF_Total_Male[0]["total"],
                "SHF_Total_Female" : SHF_Total_Female[0]["total"],
                "SHF_Total_IP" : SHF_Total_IP[0]["total"],
                "SHF_Total_PWD" : SHF_Total_PWD[0]["total"],
                "SHF_Total_Youth" : SHF_Total_Youth[0]["total"],
                "SHF_Total_SC" : SHF_Total_SC[0]["total"],
                "SHF_byRegion" : SHF_allRegion,
                "SHF_byComm" : SHF_byComm_data,
                "SHF_byHHHead" : SHF_total_HH_head_data,
                "FO_Total" : FO_Total[0]["total"],
                "FO_Total_Coop" : FO_Total_Coop[0]["total"],
                "FO_Total_Assoc" : FO_Total_Assoc[0]["total"],
                "FO_Total_Members" : FO_Total_Members[0]["total"],
                "FO_Total_Male" : FO_Total_Male[0]["total"],
                "FO_Total_Female" : FO_Total_Female[0]["total"],
                "FO_byRegion" : FO_allRegion,
                "FO_byOrgType" : FO_byOrgType,
                "FO_byComm" : FO_byComm_data,
                "MSME_Total" : MSME_Total,
                "MSME_byRegion" : MSME_allRegion,
                "MSME_byComm" : MSME_byComm_data,
                "MSME_byType" : MSME_byType_data,
            }
        
        return data
    
    
    @app.route("/webrep_v2/dashboard", methods=["POST","GET"])
    def dashboard():
        region = request.args.get("region","").strip()
        data   = _main.analyticUpdates()
        # data_dcf = displayform()
        return render_template(
            "home/project_main_dashboard.html",
			dashboard_data=data,
            region=region,
            g_site_key = g_site_key,
            active_bar = "",
        )
    
    @app.route("/webrep_v2/subscribe", methods=["POST","GET"])
    def insertSubscriber():
        
        secret_response = request.form['g-recaptcha-response']
        verify_response =requests.post(url=f'{g_verify_url}?secret={g_secret_key}&response={secret_response}').json()
        
        if verify_response.get("success") != True or verify_response.get("score",0) < 0.5:
            abort(401)
            
        email = request.form.get("subcriber_email","").strip()
        if email=="":
            # resp = jsonify({"success": False ,"message":"Email is required."})
            session['show_sweetalert'] = {"title": "Error", "text": "Email is required!", "icon": "danger"}
            return redirect("/hi_there")

        # Check if email already exists
        existing = db.select("SELECT * FROM webrep_subscribers WHERE email='{}'".format(email))
        if existing:
            session['show_sweetalert'] = {"title": "Warning", "text": "Email is already subscribed!", "icon": "warning"}
            return redirect("/hi_there")
        
        result = db.do("INSERT INTO webrep_subscribers (email, subscribe_at) VALUES ('{}','{}')".format(email, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        if result['response'] == 'error':
            session['show_sweetalert'] = {"title": "Error", "text": "Failed to subscribe, Please try again later.", "icon": "danger"}
            return redirect("/hi_there")

        session['show_sweetalert'] = {"title": "Success", "text": "Successfully subscribed!", "icon": "success"}
        return redirect("/hi_there")
    
    @app.route("/webrep_v2/search", methods=["POST","GET"])
    def search():
        
        query = request.args.get("str","").strip()
        if query=="":
            return redirect("/hi_there")
        
        page = request.args.get("page", 1, type=int)
        per_page = 12
        offset = (page - 1) * per_page

        articles = db.select("SELECT * FROM webrep_articles WHERE status='posted' AND removed=0 AND (postheader LIKE '%{}%' OR postContent LIKE '%{}%') ORDER BY id DESC LIMIT {} OFFSET {}".format(query,query,per_page,offset))
        data = []
        for article in articles:
            article['postheader'] = urllib.parse.unquote(article['postheader'])
            article['postContent'] = urllib.parse.unquote(article['postContent'])
            article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
            article['postRcu'] = urllib.parse.unquote(article['postRcu'])
            data.append(article)
            

        total = db.select("SELECT COUNT(*) AS total FROM webrep_articles WHERE status='posted' AND removed=0 AND (postheader LIKE '%{}%' OR postContent LIKE '%{}%')".format(query,query))[0]['total']

        pages = (total + per_page - 1) // per_page
        start_page = max(1, page - 2)
        end_page = min(pages, page + 2)

        # return {
        #     "items": data,
        #     "page": page,
        #     "pages": pages
        # }

        return render_template(
            "home/search_results.html",
            query=query,
            results=data,
            results_count=total,
            page=page,
            pages=pages,    
            start_page=start_page,
            end_page=end_page,
            g_site_key = g_site_key,
            active_bar = "search",
            is_session =_main.is_on_session(),
        )
        
        
        # query = request.args.get("str","").strip()
        # if query=="":
        #     return redirect("/hi_there")
        
        # articles = db.select("SELECT * FROM webrep_articles WHERE status='posted' AND removed=0 AND (postheader LIKE '%{}%' OR postContent LIKE '%{}%') ORDER BY id DESC".format(query,query))
        # data = []
        # for article in articles:
        #     article['postheader'] = urllib.parse.unquote(article['postheader'])
        #     article['postContent'] = urllib.parse.unquote(article['postContent'])
        #     article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
        #     article['postRcu'] = urllib.parse.unquote(article['postRcu'])
        #     data.append(article)
        
        # return render_template(
        #     "home/search_results.html",
        #     query=query,
        #     results=data,
        #     results_count=len(data),
        #     is_session =_main.is_on_session(),
        #     g_site_key = g_site_key,
        # )
    
    def get_tools_files(directory=''):
        files_list = []
        directory_path = 'static/pdf/tools/'+directory
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Create a path relative to the static directory
                relative_path = os.path.relpath(os.path.join(root, file), directory_path)
                files_list.append(relative_path)
        return files_list

    @app.route("/webrep_v2/knowledge_and_data",methods=["POST","GET"])
    def knowledge_and_data():
        
        dip_files = _main.get_tools_files('Detailed Investment Plan Guide')
        diagnostictools_files = _main.get_tools_files('Enterprise Diagnostic Tools')
        mg_files = _main.get_tools_files('Matching Grant Guidelines')
        
        return render_template(
            "knowledge_and_data/knowledge_and_data.html",
            is_session =_main.is_on_session(),
            g_site_key = g_site_key,
            active_bar = "knowledge_and_data",
            dip_files = dip_files,
            diagnostictools_files = diagnostictools_files,
            mg_files = mg_files
        )
    
    @app.route("/webrep_v2/stories",methods=["POST","GET"])
    def stories():
        page = request.args.get("page", 1, type=int)
        category = request.args.get("category")
        commodities = request.args.get("commodity")
        region = request.args.get("region", "")
        year = request.args.get("year", "")
        search = request.args.get("search", "")
        
        # print(f"commodities : {commodities}")
        # commodities = ','.join(['%s'] * len(commodities))
        # print(f"commodities Join : {commodities}")
        
        print(f"category : {category} ")
        print(f"commodities : {commodities} ")
        print(f"region : {region} ")
        print(f"year : {year} ")
        print(f"search : {search} ")
        
        str_query = ""
        if category:
            str_query += f" AND posttags = '{category}'"
        if commodities:
            str_query += f" AND postCategory = '{commodities}'"
        if region:
            # quoted_rcu = ",".join(f"'{r}'" for r in region)
            str_query += f" AND postRcu='{region}'"
        if year:
            str_query += f" AND YEAR(datePosted)='{year}'"
        if search:
            str_query += f" AND (postheader LIKE '%{search}%' OR postContent LIKE '%{search}%')"    
            
        per_page = 6
        offset = (page - 1) * per_page

        article_latest = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND status='posted' AND removed=0 ORDER BY id DESC LIMIT 4")
        latest_ids =  ",".join(f"{a['id']}" for a in article_latest)
        str_query += f" AND id NOT IN ({latest_ids})"

        articles = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND status='posted' AND removed=0 {} ORDER BY id DESC LIMIT {} OFFSET {}".format(str_query, per_page, offset))
        data_articles = []
        data_articles_latest = []

        # print(f"articles : {articles}")
        print(f"str_query = {str_query}")
        
        for latest in article_latest:
            latest['postheader'] = urllib.parse.unquote(latest['postheader'])
            latest['postContent'] = urllib.parse.unquote(latest['postContent'])
            latest['postAuthor'] = urllib.parse.unquote(latest['postAuthor'])
            latest['postRcu'] = urllib.parse.unquote(latest['postRcu'])
            data_articles_latest.append(latest)
        
        for article in articles:
            article['postheader'] = urllib.parse.unquote(article['postheader'])
            article['postContent'] = urllib.parse.unquote(article['postContent'])
            article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
            article['postRcu'] = urllib.parse.unquote(article['postRcu'])
            data_articles.append(article)
            
        total = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE posttype='story' AND status='posted' AND removed=0 {}".format(str_query))[0]['total']
        # total_sql = f"""
        #             SELECT COUNT(*) AS total
        #             FROM webrep_articles
        #             WHERE status='posted' AND removed=0 {str_query}
        #         """
        # total = db.select(total_sql, latest_ids)[0]['total']

        pages = (total + per_page - 1) // per_page
        start_page = max(1, page - 2)
        end_page = min(pages, page + 2)

        return render_template(
            "articles/articles_v2.html",
            stories_latest = data_articles_latest,
            stories = data_articles,
            page = page,
            pages = pages,    
            start_page = start_page,
            end_page = end_page,
            g_site_key = g_site_key,
            active_bar = "newsAndstories",
            is_session =_main.is_on_session(),
            search_str = search,
            category_selected = category,
            commodity_selected = commodities,
            region_selected = region,
            year_selected = year,
        )
        
    @app.route("/webrep_v2/news_and_updates",methods=["POST","GET"])
    def news_and_updates():
        page = request.args.get("page", 1, type=int)
        region = request.args.get("region", "")
        year = request.args.get("year", "")
        search = request.args.get("search", "")
        
        # commodities = request.args.getlist("commodities")
        # region = request.args.getlist("region")
        
        # print(f"commodities : {commodities}")
        # commodities = ','.join(['%s'] * len(commodities))
        # print(f"commodities Join : {commodities}")
        
        str_query = ""
        # if region:
        #     quoted_rcu = ",".join(f"'{r}'" for r in region)
        #     str_query += f" AND postRcu IN ({quoted_rcu})"
        # if year:
        #     quoted = ",".join(f"'{c}'" for c in year)
        #     str_query += f" AND postCategory IN ({quoted})"
        
        if region:
            str_query += f" AND postRcu='{region}'"
        if year:
            str_query += f" AND YEAR(datePosted)='{year}'"
        if search:
            str_query += f" AND (postheader LIKE '%{search}%' OR postContent LIKE '%{search}%')"    
        
        per_page = 6
        offset = (page - 1) * per_page

        article_latest = db.select("SELECT * FROM webrep_articles_v2 WHERE ( posttype='news' OR posttype='event' ) AND status='posted' AND removed=0 ORDER BY id DESC LIMIT 4")
        latest_ids =  ",".join(f"{a['id']}" for a in article_latest)
        str_query += f" AND id NOT IN ({latest_ids})"

        articles = db.select("SELECT * FROM webrep_articles_v2 WHERE ( posttype='news' OR posttype='event' ) AND status='posted' AND removed=0 {} ORDER BY id DESC LIMIT {} OFFSET {}".format(str_query, per_page, offset))
        data_articles = []
        data_articles_latest = []

        print(f"articles : {articles}")
        
        for latest in article_latest:
            latest['postheader'] = urllib.parse.unquote(latest['postheader'])
            latest['postContent'] = urllib.parse.unquote(latest['postContent'])
            latest['postAuthor'] = urllib.parse.unquote(latest['postAuthor'])
            latest['postRcu'] = urllib.parse.unquote(latest['postRcu'])
            data_articles_latest.append(latest)
        
        for article in articles:
            article['postheader'] = urllib.parse.unquote(article['postheader'])
            article['postContent'] = urllib.parse.unquote(article['postContent'])
            article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
            article['postRcu'] = urllib.parse.unquote(article['postRcu'])
            data_articles.append(article)
            
        total = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE ( posttype='news' OR posttype='event' ) AND status='posted' AND removed=0 {}".format(str_query))[0]['total']
        # total_sql = f"""
        #             SELECT COUNT(*) AS total
        #             FROM webrep_articles
        #             WHERE status='posted' AND removed=0 {str_query}
        #         """
        # total = db.select(total_sql, latest_ids)[0]['total']

        pages = (total + per_page - 1) // per_page
        start_page = max(1, page - 2)
        end_page = min(pages, page + 2)

        return render_template(
            "articles/news_and_updates.html",
            stories_latest = data_articles_latest,
            stories = data_articles,
            page = page,
            pages = pages,    
            start_page = start_page,
            end_page = end_page,
            region_selected = region,
            year_selected = year,
            search_str = search,
            g_site_key = g_site_key,
            active_bar = "newsAndstories",
            is_session =_main.is_on_session(),
        )
    
    @app.route("/webrep_v2/what_we_do/network_beneficiaries", methods=["GET","POST"])
    def network_beneficiaries():
        fo = db.select("SELECT form_b.organization_registered_name,form_b.office_business_adrress, form_b.respondents_mobile, form_b.respondents_email, form_b.operational_crop_commodity, users.rcu, users.pcu FROM form_b LEFT JOIN users ON users.id = form_b.uploaded_by WHERE form_b.organization_registered_name <> '' ORDER BY form_b.organization_registered_name ASC")
        return render_template(
            "what_we_do/network_beneficiaries.html",
            g_site_key = g_site_key,
            active_bar = "whatwedo",
            form_b = fo,
        )
        
    @app.route("/webrep_v2/what_we_do/network/data",methods=["POST"])
    def what_we_do_network_data():
        
        stakeholder_type = request.json.get("stakeholder_type", "fo")
        if stakeholder_type == "fo":
            data = db.select("SELECT form_b.organization_registered_name as name ,form_b.office_business_adrress as address, form_b.respondents_mobile as contactno, form_b.respondents_email as email, form_b.operational_crop_commodity as commodity, users.rcu, users.pcu FROM form_b LEFT JOIN users ON users.id = form_b.uploaded_by WHERE form_b.organization_registered_name <> '' ORDER BY form_b.organization_registered_name ASC")
        elif stakeholder_type == "msme":
            data = db.select("SELECT form_c.reg_businessname as name, form_c.business_addr as address, form_c.contact_details as contactno, form_c.email_add as email, form_c.industry_cluster as commodity, users.rcu, users.pcu FROM form_c LEFT JOIN users ON users.id = form_c.upload_by WHERE form_c.reg_businessname <> '' ORDER BY form_c.reg_businessname ASC")
        return jsonify({"data": data})
    
    @app.route("/webrep_v2/what_we_do",methods=["POST","GET"])
    def what_we_do():
        fo = db.select("SELECT form_b.organization_registered_name,form_b.office_business_adrress, form_b.respondents_mobile, form_b.respondents_email, form_b.operational_crop_commodity, users.rcu, users.pcu FROM form_b LEFT JOIN users ON users.id = form_b.uploaded_by WHERE form_b.organization_registered_name <> '' ORDER BY form_b.organization_registered_name ASC")
        return render_template(
            "what_we_do/what_we_do.html",
            g_site_key = g_site_key,
            active_bar = "whatwedo",
            is_session =_main.is_on_session(),
            form_b = fo,
        )
    
    @app.route("/webrep_v2/articles",methods=["POST","GET"])
    def articles():
        user_data = ''
        if 'USER_DATA' in session:
                user_data = session['USER_DATA'][0]
        else:
            # return "No User data! Please login first.", 400
            return redirect("/login?next=/webrep_v2/article/create")
        
        posttype = request.args.get("posttype", "all")
        commodities = request.args.getlist("commodities", "all")
        region = request.args.getlist("region", "all")
        status = request.args.get("status", "all")
        search = request.args.get("search", "").strip()
        
        str_query = ""
        if posttype != "all":
            str_query += f" AND posttype='{posttype}'"
        if status != "all":
            str_query += f" AND status='{status}'"
        if commodities:
            quoted = ",".join(f"'{c}'" for c in commodities)
            str_query += f" AND postCategory IN ({quoted})"
        if region:
            quoted_rcu = ",".join(f"'{r}'" for r in region)
            str_query += f" AND postRcu IN ({quoted_rcu})"
        if search:
            str_query += f" AND (postheader LIKE '%{search}%' OR postContent LIKE '%{search}%')"

        if user_data['job']!="Super Admin":
                str_query += f" AND USER_ID={user_data['id']}"
        
        # articles = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND removed=0 {} ORDER BY id DESC ".format(str_query))
        articles = db.select("SELECT * FROM webrep_articles_v2 WHERE removed=0 {} ORDER BY id DESC ".format(str_query))
        
        return render_template(
            "admin/articles.html",
            g_site_key = g_site_key,
            active_bar = "stories",
            articles = articles,
            posttype_selected = posttype,
            status_selected = status,
            commodities_selected = commodities,
            region_selected = region,
            search_query = search,
            is_session =_main.is_on_session(),
        )
    
    @app.route("/webrep_v2/whoweare",methods=["POST","GET"])
    def about():
        return render_template(
            "about/about.html",
            active_bar = "whoweare",
            g_site_key = g_site_key,
            is_session =_main.is_on_session(),
        )
    
    @app.route("/webrep_v2/article/create",methods=["POST","GET"])
    def create_story():
        
        if 'USER_DATA' in session:
                user_data = session['USER_DATA'][0]
        else:
            # return "No User data! Please login first.", 400
            return redirect("/login?next=/webrep_v2/article/create")

        return render_template(
            "admin/create_article.html",
            user_data = session['USER_DATA'][0],
            active_bar = "stories",
            g_site_key = g_site_key,
        )
        
    # @app.route("/webrep_v2/upload_file_webrep",methods=["POST","GET"])
    # def upload_file_webrep():
    #     print("  * Article Module")
    #     from datetime import date, datetime
    #     from modules.Req_Brorn_util import file_from_request
    #     FILE_REQ = file_from_request(app)
    #     data = dict(request.form)
    #     key = [];val = [];args=""
    #     data["USER_ID"] = session["USER_DATA"][0]['id']

    #     __f = FILE_REQ.save_file_from_request(request,"file_name",c.RECORDS+"/objects/webrep/",False,True)
    #     data["file_name"] = __f["file_arr_str"]

    #     is_exist = len(db.select("SELECT * FROM `webrep_articles_v2` WHERE `id` ='{}' ;".format(request.form['id'])))
    #     if(is_exist==0):
    #         print(" >> Adding Articles")
    #         for datum in data:
    #             # print(datum)
    #             key.append("`{}`".format(datum))
    #             val.append("'{}'".format(data[datum]))
            
    #         # sql = ('''INSERT INTO `webrep_articles_v2` ({},`status`) VALUES ({},'pending')'''.format(", ".join(key),", ".join(val)))

    #     else:
    #         print(" >> Editing Articles")
    #         for datum in data:
    #             args += ",`{}`='{}'".format(datum,data[datum])
    #         sql = "UPDATE `webrep_articles_v2` SET  {}, `status`='pending' WHERE `id`='{}';".format(args[1:],request.form['id'])
    #         pass
        
    #     last_row_id = db.do(sql)
    #     return jsonify({"last_row_id":last_row_id,"FILES":__f})
    
    @app.route("/webrep_v2/upload_file_webrep",methods=["POST","GET"])
    def upload_file_webrep():
        print("  * Article Module")
        from datetime import date, datetime
        from modules.Req_Brorn_util import file_from_request
        FILE_REQ = file_from_request(app)
        data = dict(request.form)
        key = [];val = [];args=""
        data["USER_ID"] = session["USER_DATA"][0]['id']

        __f = FILE_REQ.save_file_from_request(request,"file_name",c.RECORDS+"/objects/webrep/",False,True)
        data["file_name"] = __f["file_arr_str"]

        is_exist = len(db.select("SELECT * FROM `webrep_articles_v2` WHERE `id` ='{}' ;".format(request.form['id'])))
        columns = []
        values = []
        if(is_exist==0):
            print(" >> Adding Articles")
            columns = []
            values = []

            for datum in data:
                columns.append(f"`{datum}`")
                value = data[datum]

                # Decode only if it's a string
                if isinstance(value, str):
                    value = urllib.parse.unquote(value)

                values.append(value)

            # Add status column/value
            columns.append("`status`")
            values.append("pending")

            # Build placeholders for parameterization
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO `webrep_articles_v2` ({', '.join(columns)}) VALUES ({placeholders})"
            
        else:
            print(" >> Editing Articles")
            for datum in data:
                args += ",`{}`='{}'".format(datum,data[datum])
            sql = "UPDATE `webrep_articles_v2` SET  {}, `status`='pending' WHERE `id`='{}';".format(args[1:],request.form['id'])
            pass
        
        last_row_id = db.do(sql,values)
        return jsonify({"last_row_id":last_row_id,"FILES":__f})