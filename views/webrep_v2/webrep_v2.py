from multiprocessing import connection
from xmlrpc import server

from certifi.__main__ import args
from flask import Blueprint, abort, flash, render_template, render_template_string, request, session, redirect, jsonify, send_file, send_from_directory, Response, current_app, url_for
from flask_session import Session
from rsa import key
import modules
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
import uuid


from datetime import date, datetime
from modules.Req_Brorn_util import file_from_request
from v2_view.core._backend_sub import FILE_REQ
from views.dcfv2.dashboard.display_dataform import displayform


import smtplib
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        isAdmin = True
        user_data = ''
        
        if(c.IN_MAINTENANCE):return redirect("/we_will_be_back_later")
        # dashboard_data =  json.loads(dboard_main.system_page())
        # dashboard_data =  dboard_main.system_page()
        
        if 'USER_DATA' in session:
            user_data = session['USER_DATA'][0]
        
        if user_data != '':        
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                isAdmin = False
                
        return render_template(
            "home/home.html",
            sliders_data=_main.getLatestArticles(),
            is_session =_main.is_on_session(),
            g_site_key = g_site_key,
            active_bar = "home",
            isAdmin = isAdmin
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
        update_del = db.do("UPDATE `webrep_articles_v2` SET `status`='published' WHERE `id`='{}';".format(ids))
        return {"db_info":update_del}

    @app.route("/webrep_v2/articles/revise/<ids>",methods=["POST","GET"])
    def revise_article(ids):
        update_del = db.do("UPDATE `webrep_articles_v2` SET `status`='for_revision' WHERE `id`='{}';".format(ids))
        return {"db_info":update_del}
    
    @app.route("/webrep_v2/case_studies/delete/<ids>",methods=["POST","GET"])
    def delete_casestudy(ids):
        update_del = db.do("UPDATE `webrep_case_study_v2` SET `isDeleted`='1' WHERE `id`='{}';".format(ids))
        print("deleting.....")
        print(update_del)
        return {"db_info":update_del}

    @app.route("/webrep_v2/case_studies/confirm/<ids>",methods=["POST","GET"])
    def confirm_casestudy(ids):
        update_del = db.do("UPDATE `webrep_case_study_v2` SET `status`='published' WHERE `id`='{}';".format(ids))
        return {"db_info":update_del}

    @app.route("/webrep_v2/case_studies/revise/<ids>",methods=["POST","GET"])
    def revise_casestudy(ids):
        update_del = db.do("UPDATE `webrep_case_study_v2` SET `status`='for_revision' WHERE `id`='{}';".format(ids))
        return {"db_info":update_del}
    
    @app.route("/webrep/article/get_post_ind",methods=["POST","GET"])
    def get_post_ind():
        ids = request.form['article_id']
        return db.select("SELECT *, DATE_FORMAT(postDate, '%Y-%m-%d') AS postDate FROM webrep_articles_v2 WHERE id='{}' ORDER BY id DESC;".format(ids))
    @app.route("/webrep_v2/article/get_img/", defaults={"img": None}, methods=["GET", "POST"])
    @app.route("/webrep_v2/article/get_img/<img>",methods=["POST","GET"])
    def get_img(img):
        if img is None or img.strip() == "":
            return send_file( "static/img/no_img.png")
        
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
            # print(type(article), article)
            article['postheader'] = urllib.parse.unquote(article['postheader'])
            article['postContent'] = urllib.parse.unquote(article['postContent'])
            article['postdescription'] = urllib.parse.unquote(article['postdescription'])
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
        # Build absolute path from Flask's root
        base_path = os.path.join(current_app.root_path, 'static', 'pdf', 'tools')
        directory_path = os.path.join(base_path, directory)

        print(f"Checking directory: {directory_path}")  # Debug

        if not os.path.exists(directory_path):
            print("Directory does NOT exist!")
            return []

        print("Directory exists, walking files...")
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                relative_path = relative_path.replace("\\", "/")  # Normalize for URLs
                files_list.append(relative_path)

        # Sort ascending (alphabetical)
        files_list = sorted(files_list)
    
        print(f"Files found: {files_list}")
        return files_list

    def get_updates_files(directory=''):
        files_list = []
        # Build absolute path from Flask's root
        base_path = os.path.join(current_app.root_path, 'static', 'pdf', 'updates_and_reports')
        directory_path = os.path.join(base_path, directory)

        print(f"Checking directory: {directory_path}")  # Debug

        if not os.path.exists(directory_path):
            print("Directory does NOT exist!")
            return []

        print("Directory exists, walking files...")
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), base_path)
                relative_path = relative_path.replace("\\", "/")  # Normalize for URLs
                files_list.append(relative_path)
        
        # Sort ascending (alphabetical)
        files_list = sorted(files_list)
        
        print(f"Files found: {files_list}")
        return files_list

    @app.route("/webrep_v2/knowledge_and_data",methods=["POST","GET"])
    def knowledge_and_data():
        isAdmin = True
        user_data = ''  
        try:
            
            if 'USER_DATA' in session:
                user_data = session['USER_DATA'][0]
            
            if user_data != '':
                if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                    isAdmin = False
                
            region = request.args.get("region", "all")
            search = request.args.get("search", "").strip()
            
            str_query = ""
            if region != "all":
                str_query += f" AND webrep_case_study_v2.rcu='{region}'"
            if search:
                str_query += f" AND (basic_workingTitle LIKE '%{search}%' OR subject_mainSubject LIKE '%{search}%')"

            case_studies = db.select("SELECT webrep_case_study_v2.*,DATE_FORMAT(webrep_case_study_v2.basic_dateOfDocumentation, '%M %d, %Y') AS formatted_dateOfDocumentation,users.name AS created_by FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND (webrep_case_study_v2.status='published' OR webrep_case_study_v2.status='posted') {} ORDER BY id DESC ".format(str_query))
            # case_studies = db.select("SELECT webrep_case_study_v2.*,DATE_FORMAT(webrep_case_study_v2.basic_dateOfDocumentation, '%M %d, %Y') AS formatted_dateOfDocumentation,users.name AS created_by FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0  {} ORDER BY id DESC ".format(str_query))
            
            updates_files = _main.get_updates_files('')
            
            dip_files = _main.get_tools_files('Detailed Investment Plan Guide')
            diagnostictools_files = _main.get_tools_files('Enterprise Diagnostic Tools')
            mg_files = _main.get_tools_files('Matching Grant Guidelines')
            pim2025_files = _main.get_tools_files('Project Implementation Manual 2025')
            vcdt_files = _main.get_tools_files('Value Chain Development Tools')
            
            return render_template(
                "knowledge_and_data/knowledge_and_data.html",
                is_session =_main.is_on_session(),
                g_site_key = g_site_key,
                active_bar = "knowledge_and_data",
                dip_files = dip_files,
                diagnostictools_files = diagnostictools_files,
                mg_files = mg_files,
                pim2025_files = pim2025_files,
                updates_files = updates_files,
                vcdt_files = vcdt_files,
                case_studies = case_studies,
                isAdmin = isAdmin
            )
        except Exception as e:
            return render_template(
                "error/error.html",
                message = "An error occurred while loading the Knowledge and Data page.",
                error = str(e)
            )
    
    @app.route("/webrep_v2/stories",methods=["POST","GET"])
    def stories():
        isAdmin = True
        user_data = ''
        
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
        
        if 'USER_DATA' in session:
            user_data = session['USER_DATA'][0]
        
        if user_data != '':    
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                isAdmin = False
            
        per_page = 8
        offset = (page - 1) * per_page

        article_latest = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND status='posted' AND removed=0 ORDER BY id DESC LIMIT 3")
        latest_ids =  ",".join(f"{a['id']}" for a in article_latest)
        str_query += f" AND id NOT IN ({latest_ids})"

        articles = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND status='posted' AND removed=0 {} ORDER BY id DESC LIMIT {} OFFSET {}".format(str_query, per_page, offset))
        data_articles = []
        data_articles_latest = []

        # print(f"articles : {articles}")
        print(f"str_query = {str_query}")
        
        for latest in article_latest:
            latest['postheader'] = urllib.parse.unquote(latest['postheader'])
            latest['postdescription'] = urllib.parse.unquote(latest['postdescription'])
            latest['postContent'] = urllib.parse.unquote(latest['postContent'])
            latest['postAuthor'] = urllib.parse.unquote(latest['postAuthor'])
            latest['postRcu'] = urllib.parse.unquote(latest['postRcu'])
            data_articles_latest.append(latest)
        
        for article in articles:
            article['postheader'] = urllib.parse.unquote(article['postheader'])
            article['postdescription'] = urllib.parse.unquote(article['postdescription'])
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
            isAdmin = isAdmin
        )
        
    @app.route("/webrep_v2/news_and_updates",methods=["POST","GET"])
    def news_and_updates():
        isAdmin = True
        user_data = ''
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
        
        if 'USER_DATA' in session:
            user_data = session['USER_DATA'][0]
             
        if user_data != '':
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                isAdmin = False

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
            isAdmin = isAdmin
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
        isAdmin = True
        user_data = ''
        
        if 'USER_DATA' in session:
            user_data = session['USER_DATA'][0]
        
        if user_data != '':    
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                isAdmin = False
            
        fo = db.select("SELECT form_b.organization_registered_name,form_b.office_business_adrress, form_b.respondents_mobile, form_b.respondents_email, form_b.operational_crop_commodity, users.rcu, users.pcu FROM form_b LEFT JOIN users ON users.id = form_b.uploaded_by WHERE form_b.organization_registered_name <> '' ORDER BY form_b.organization_registered_name ASC")
        return render_template(
            "what_we_do/what_we_do.html",
            g_site_key = g_site_key,
            active_bar = "whatwedo",
            is_session =_main.is_on_session(),
            form_b = fo,
            isAdmin = isAdmin
        )
    
    @app.route("/webrep_v2/articles",methods=["POST","GET"])
    def articles():
        user_data = ''
        isAdmin = True
        
        try:

            if 'USER_DATA' in session:
                    user_data = session['USER_DATA'][0]
            else:
                # return "No User data! Please login first.", 400
                return redirect("/login?next=/webrep_v2/article/create")
            
            posttype = request.args.get("posttype", "all")
            commodities = request.args.get("commodity", "all")
            region = request.args.get("region", "all")
            status = request.args.get("status", "all")
            search = request.args.get("search", "").strip()
            
            str_query = ""
            rcu_filter = ""
            
            if posttype != "all":
                str_query += f" AND posttype='{posttype}'"
            if status != "all":
                if status == "draft" or status == "pending":
                    str_query += f" AND (status='draft' OR status='pending')"
                elif status == "for_revision" or status == "revise":
                    str_query += f" AND (status='for_revision' OR status='revise')"
                elif status == "published" or status == "posted":
                    str_query += f" AND (status='published' OR status='posted')"
                else:
                    str_query += f" AND status='{status}'"
            if commodities != "all":
                # quoted = ",".join(f"'{c}'" for c in commodities)
                # str_query += f" AND postCategory IN ({quoted})"
                str_query += f" AND postCategory = '{commodities}'"
            if region != "all":
                # quoted_rcu = ",".join(f"'{r}'" for r in region)
                # str_query += f" AND postRcu IN ({quoted_rcu})"
                str_query += f" AND postRcu='{region}'"
            if search:
                str_query += f" AND (postheader LIKE '%{search}%' OR postContent LIKE '%{search}%')"

            user_rcu = ""
            if user_data['rcu']=="RCU 8":
                user_rcu = "RCU VIII"
            elif user_data['rcu']=="RCU 9":
                user_rcu = "RCU IX"
            elif user_data['rcu']=="RCU 10":
                user_rcu = "RCU X"
            elif user_data['rcu']=="RCU 11":
                user_rcu = "RCU XI"
            elif user_data['rcu']=="RCU 12":
                user_rcu = "RCU XII"
            elif user_data['rcu']=="RCU 13":
                user_rcu = "RCU XIII"
            elif user_data['rcu']=="BARMM":
                user_rcu = "BARMM"
               
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                # str_query += f" AND USER_ID={user_data['id']}"
                str_query += f" AND postRcu='{user_rcu}'"
                rcu_filter += f" AND postRcu='{user_rcu}'"
                isAdmin = False
                
            # articles = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND removed=0 {} ORDER BY id DESC ".format(str_query))
            articles = db.select("SELECT * FROM webrep_articles_v2 WHERE removed=0 {} ORDER BY id DESC ".format(str_query))
            
            total = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE removed=0 {}".format(rcu_filter))[0]['total']
            draft = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE removed=0 AND (status='draft' OR status='pending') {}".format(rcu_filter))[0]['total']
            for_approval = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE removed=0 AND status='for_approval' {}".format(rcu_filter))[0]['total']
            for_revision = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE removed=0 AND (status='for_revision' OR status='revise') {}".format(rcu_filter))[0]['total']
            published = db.select("SELECT COUNT(*) AS total FROM webrep_articles_v2 WHERE removed=0 AND (status='published' OR status='posted') {}".format(rcu_filter))[0]['total']

            # total = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id  WHERE webrep_case_study_v2.isDeleted=0 {}".format(rcu_filter))[0]['total']
            # drafted = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='draft' {}".format(rcu_filter))[0]['total']
            # published = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='published' {}".format(rcu_filter))[0]['total']
            # for_approval = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='for_approval' {}".format(rcu_filter))[0]['total']
            # for_revision = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='for_revision' {}".format(rcu_filter))[0]['total']


            return render_template(
                "admin/articles.html",
                g_site_key = g_site_key,
                active_bar = "stories",
                articles = articles,
                posttype_selected = posttype,
                status_selected = status,
                commodity_selected = commodities,
                region_selected = region,
                search_query = search,
                is_session =_main.is_on_session(),
                user_data = user_data,
                isAdmin = isAdmin,
                total = total,
                draft = draft,
                for_approval = for_approval,
                for_revision = for_revision,
                published = published
            )
        except Exception as e:
            return render_template(
                "error/error.html",
                message="An unexpected error occurred while loading articles.",
                error=str(e)
            ), 500

    @app.route("/webrep_v2/case_studies",methods=["POST","GET"])
    def case_studies():
        user_data = ''
        isAdmin = True
        
        try:

            if 'USER_DATA' in session:
                    user_data = session['USER_DATA'][0]
            else:
                # return "No User data! Please login first.", 400
                return redirect("/login?next=/webrep_v2/case_studies/create")
            
            region = request.args.get("region", "all")
            status = request.args.get("status", "all")
            search = request.args.get("search", "").strip()
            
            str_query = ""
            rcu_filter = ""
            
            if status != "all":
                str_query += f" AND webrep_case_study_v2.status='{status}'"
            if region != "all":
                # quoted_rcu = ",".join(f"'{r}'" for r in region)
                # str_query += f" AND postRcu IN ({quoted_rcu})"
                str_query += f" AND webrep_case_study_v2.rcu='{region}'"
            if search:
                str_query += f" AND (basic_workingTitle LIKE '%{search}%' OR subject_mainSubject LIKE '%{search}%')"

            user_rcu = ""
            if user_data['rcu']=="RCU 8":
                user_rcu = "RCU VIII"
            elif user_data['rcu']=="RCU 9":
                user_rcu = "RCU IX"
            elif user_data['rcu']=="RCU 10":
                user_rcu = "RCU X"
            elif user_data['rcu']=="RCU 11":
                user_rcu = "RCU XI"
            elif user_data['rcu']=="RCU 12":
                user_rcu = "RCU XII"
            elif user_data['rcu']=="RCU 13":
                user_rcu = "RCU XIII"
            elif user_data['rcu']=="BARMM":
                user_rcu = "BARMM"
                
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                # str_query += f" AND USER_ID={user_data['id']}"
                str_query += f" AND webrep_case_study_v2.rcu='{user_rcu}'"
                rcu_filter += f" AND webrep_case_study_v2.rcu='{user_rcu}'"
                isAdmin = False

            
            print(f"str_query = {str_query}")
            
            # articles = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND removed=0 {} ORDER BY id DESC ".format(str_query))
            case_studies = db.select("SELECT webrep_case_study_v2.*,DATE_FORMAT(webrep_case_study_v2.basic_dateOfDocumentation, '%M %d, %Y') AS formatted_dateOfDocumentation,users.rcu,users.name AS created_by FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 {} ORDER BY id DESC ".format(str_query))
            
            total = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id  WHERE webrep_case_study_v2.isDeleted=0 {}".format(rcu_filter))[0]['total']
            drafted = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='draft' {}".format(rcu_filter))[0]['total']
            published = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='published' {}".format(rcu_filter))[0]['total']
            for_approval = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='for_approval' {}".format(rcu_filter))[0]['total']
            for_revision = db.select("SELECT COUNT(*) AS total FROM webrep_case_study_v2 LEFT JOIN users ON webrep_case_study_v2.USER_ID=users.id WHERE webrep_case_study_v2.isDeleted=0 AND webrep_case_study_v2.status='for_revision' {}".format(rcu_filter))[0]['total']

            # case_studies = []
            # total = 0
            # drafted = 0
            # published = 0
            # for_approval = 0        
            # for_revision = 0
            
            # print(f"case_studies : {case_studies}")
            return render_template(
                "admin/case_studies.html",
                g_site_key = g_site_key,
                active_bar = "knowledge_and_data",
                case_studies = case_studies,
                status_selected = status,
                region_selected = region,
                search_query = search,
                is_session =_main.is_on_session(),
                user_data = user_data,
                isAdmin = isAdmin,
                total = total,
                drafted = drafted,
                published = published,
                for_approval = for_approval,
                for_revision = for_revision,
            )
        except Exception as e:
            return render_template(
                "error/error.html",
                message="An unexpected error occurred while loading articles.",
                error=str(e)
            ), 500

    
    @app.route("/webrep_v2/newsletters/get",methods=["GET"])
    def get_newsletters():
        id = request.args.get("id")
        newsletters = db.select("SELECT webrep_newsletters.*,DATE_FORMAT(webrep_newsletters.createdDate, '%M %d, %Y %h:%i %p') AS formatted_createdDate,DATE_FORMAT(webrep_newsletters.publishedDate, '%M %d, %Y %h:%i %p') AS formatted_publishedDate,users.name AS created_by FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.id=users.id WHERE webrep_newsletters.isDeleted=0 AND webrep_newsletters.id={} ORDER BY id DESC".format(id))
        return jsonify({"newsletter": newsletters[0] if newsletters else None})

    @app.route("/webrep_v2/newsletters",methods=["POST","GET"])
    def newsletters():
        user_data = ''
        isAdmin = True
        
        try:

            if 'USER_DATA' in session:
                    user_data = session['USER_DATA'][0]
            else:
                # return "No User data! Please login first.", 400
                return redirect("/login?next=/webrep_v2/newsletters/create")
            
            subscribers = db.select("SELECT * FROM webrep_subscribers ORDER BY email ASC")
            
            # articles = db.select("SELECT * FROM webrep_articles_v2 WHERE posttype='story' AND removed=0 {} ORDER BY id DESC ".format(str_query))
            newsletters = db.select("SELECT webrep_newsletters.*,DATE_FORMAT(webrep_newsletters.createdDate, '%M %d, %Y %h:%i %p') AS formatted_createdDate,DATE_FORMAT(webrep_newsletters.publishedDate, '%M %d, %Y %h:%i %p') AS formatted_publishedDate,users.name AS created_by FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.id=users.id WHERE webrep_newsletters.isDeleted=0 {} ORDER BY id DESC ".format(''))
            
            total = db.select("SELECT COUNT(*) AS total FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.id=users.id  WHERE webrep_newsletters.isDeleted=0 {}".format(''))[0]['total']
            drafted = db.select("SELECT COUNT(*) AS total FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.id=users.id WHERE webrep_newsletters.isDeleted=0 AND webrep_newsletters.status='draft' {}".format(''))[0]['total']
            published = db.select("SELECT COUNT(*) AS total FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.id=users.id WHERE webrep_newsletters.isDeleted=0 AND webrep_newsletters.status='published' {}".format(''))[0]['total']
            total_subscribers = db.select("SELECT COUNT(*) AS total FROM webrep_subscribers")[0]['total']
            # for_approval = db.select("SELECT COUNT(*) AS total FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.USER_ID=users.id WHERE webrep_newsletters.isDeleted=0 AND webrep_newsletters.status='for_approval' {}".format(rcu_filter))[0]['total']
            # for_revision = db.select("SELECT COUNT(*) AS total FROM webrep_newsletters LEFT JOIN users ON webrep_newsletters.USER_ID=users.id WHERE webrep_newsletters.isDeleted=0 AND webrep_newsletters.status='for_revision' {}".format(rcu_filter))[0]['total']

            # newsletters = []
            # total = 0
            # drafted = 0
            # published = 0
            # for_approval = 0        
            # for_revision = 0
            
            # print(f"Subscribers : {subscribers}")
            return render_template(
                "admin/newsletter.html",
                g_site_key = g_site_key,
                active_bar = "knowledge_and_data",
                newsletters = newsletters,
                subscribers = subscribers,
                is_session =_main.is_on_session(),
                user_data = user_data,
                isAdmin = isAdmin,
                total = total,
                drafted = drafted,
                published = published,
                total_subscribers = total_subscribers
            )
        except Exception as e:
            return render_template(
                "error/error.html",
                message="An unexpected error occurred while loading articles.",
                error=str(e)
            ), 500
       
    @app.route("/webrep_v2/whoweare",methods=["POST","GET"])
    def about():
        isAdmin = True
        user_data = ''
        
        if 'USER_DATA' in session:
            user_data = session['USER_DATA'][0]
        
        if user_data != '':
            if user_data['job']!="Super Admin" and user_data['job']!="Communication and Knowledge Management Specialist":
                isAdmin = False
            
        return render_template(
            "about/about.html",
            active_bar = "whoweare",
            g_site_key = g_site_key,
            is_session =_main.is_on_session(),
            isAdmin = isAdmin
        )
    
    @app.route("/webrep_v2/article/create",methods=["POST","GET"])
    def create_story():
        
        if 'USER_DATA' in session:
                user_data = session['USER_DATA'][0]
        else:
            # return "No User data! Please login first.", 400
            return redirect("/login?next=/webrep_v2/article/create")

        id = request.args.get("ids")
        if id:
            article = db.select("SELECT * FROM webrep_articles_v2 WHERE id='{}'".format(id))
            if article:
                article = article[0]
                if int(article['USER_ID']) != int(user_data['id']) and user_data['job']!="Super Admin":
                    # return str(article['USER_ID'])+" | "+str(user_data['id'])+" | "+str(int(article['USER_ID']) != int(user_data['id'])) + " | "+ str(user_data['job']!="Super Admin")+" You don't have permission to edit this article.", 403
                    return "You don't have permission to edit this article.", 403
                article['postheader'] = urllib.parse.unquote(article['postheader'])
                article['postContent'] = urllib.parse.unquote(article['postContent'])
                article['postAuthor'] = urllib.parse.unquote(article['postAuthor'])
                article['postRcu'] = urllib.parse.unquote(article['postRcu'])
                return render_template(
                    "admin/create_article.html",
                    user_data = session['USER_DATA'][0],
                    active_bar = "stories",
                    g_site_key = g_site_key,
                    article = article
                )
            else:
                return "Article not found.", 404
            
        return render_template(
            "admin/create_article.html",
            user_data = session['USER_DATA'][0],
            active_bar = "stories",
            g_site_key = g_site_key,
            article = None
        )
    
    @app.route("/webrep_v2/newsletters/create",methods=["POST","GET"])
    def create_newsletter():
        
        if 'USER_DATA' in session:
                user_data = session['USER_DATA'][0]
        else:
            # return "No User data! Please login first.", 400
            return redirect("/login?next=/webrep_v2/newsletters/create")

        id = request.args.get("ids")
        if id:
            newsletter = db.select("SELECT * FROM webrep_newsletters WHERE id='{}'".format(id))
            if newsletter:
                newsletter = newsletter[0]
                # if int(newsletter['USER_ID']) != int(user_data['id']) and user_data['job']!="Super Admin":
                #     # return str(newsletter['USER_ID'])+" | "+str(user_data['id'])+" | "+str(int(newsletter['USER_ID']) != int(user_data['id'])) + " | "+ str(user_data['job']!="Super Admin")+" You don't have permission to edit this newsletter.", 403
                #     return "You don't have permission to edit this newsletter.", 403
                # newsletter['postheader'] = urllib.parse.unquote(newsletter['postheader'])
                # newsletter['postContent'] = urllib.parse.unquote(newsletter['postContent'])
                # newsletter['postAuthor'] = urllib.parse.unquote(newsletter['postAuthor'])
                # newsletter['postRcu'] = urllib.parse.unquote(newsletter['postRcu'])
                return render_template(
                    "admin/create_newsletter.html",
                    user_data = session['USER_DATA'][0],
                    active_bar = "stories",
                    g_site_key = g_site_key,
                    newsletter = newsletter
                )
            else:
                return "Newsletter not found.", 404
            
        return render_template(
            "admin/create_newsletter.html",
            user_data = session['USER_DATA'][0],
            active_bar = "stories",
            g_site_key = g_site_key,
            newsletter = None
        )
    
    @app.route("/webrep_v2/case_studies/<int:id>", methods=["POST","GET"])
    def view_case_study(id):
        casestudy = db.select("SELECT * FROM webrep_case_study_v2 WHERE id='{}'".format(id))
        if casestudy:
            casestudy = casestudy[0]
            return render_template(
                "case_studies/single.html",
                user_data = session['USER_DATA'][0],
                active_bar = "knowledge_and_data",
                g_site_key = g_site_key,
                case_study = casestudy
            )
        else:
            return "Case study not found.", 404

    @app.route("/webrep_v2/case_studies/create",methods=["POST","GET"])
    def create_case_study():
        
        if 'USER_DATA' in session:
                user_data = session['USER_DATA'][0]
        else:
            # return "No User data! Please login first.", 400
            return redirect("/login?next=/webrep_v2/case_studies/create")

        id = request.args.get("ids")
        if id:
            casestudy = db.select("SELECT * FROM webrep_case_study_v2 WHERE id='{}'".format(id))
            if casestudy:
                casestudy = casestudy[0]
                if int(casestudy['USER_ID']) != int(user_data['id']) and user_data['job']!="Super Admin":
                    # return str(casestudy['USER_ID'])+" | "+str(user_data['id'])+" | "+str(int(casestudy['USER_ID']) != int(user_data['id'])) + " | "+ str(user_data['job']!="Super Admin")+" You don't have permission to edit this case study.", 403
                    return "You don't have permission to edit this case study.", 403
                # casestudy['postheader'] = urllib.parse.unquote(casestudy['postheader'])
                # casestudy['postContent'] = urllib.parse.unquote(casestudy['postContent'])
                # casestudy['postAuthor'] = urllib.parse.unquote(casestudy['postAuthor'])
                # casestudy['postRcu'] = urllib.parse.unquote(casestudy['postRcu'])
                return render_template(
                    "admin/create_case_study_v2.html",
                    user_data = session['USER_DATA'][0],
                    active_bar = "knowledge_and_data",
                    g_site_key = g_site_key,
                    case_study = casestudy
                )
            else:
                return "Case study not found.", 404
            
        return render_template(
            "admin/create_case_study_v2.html",
            user_data = session['USER_DATA'][0],
            active_bar = "knowledge_and_data",
            g_site_key = g_site_key,
            case_study = None
        )
    
    @app.route("/webrep_v2/upload_case_study",methods=["POST","GET"])
    def upload_case_study():
        from datetime import date, datetime
        from modules.Req_Brorn_util import file_from_request
        data = dict(request.form)
        key = [];val = [];args=""
        data["USER_ID"] = session["USER_DATA"][0]['id']
        
        FILE_REQ = file_from_request(app)   
        __f = FILE_REQ.save_file_from_request(request,"photo",c.RECORDS+"/objects/webrep/",False,True)
        data["photo"] = __f["file_arr_str"]
        
        is_exist = len(db.select("SELECT * FROM `webrep_case_study_v2` WHERE `id` ='{}' ;".format(request.form['id'])))
        if(is_exist==0):
            print(" >> Adding Articles")
            # for datum in data:
			# 	# print(datum)
            #     value = urllib.parse.unquote(data[datum]) if isinstance(data[datum], str) else data[datum]
            #     key.append("`{}`".format(datum))
            #     val.append("'{}'".format(value))
            # sql = ('''INSERT INTO `webrep_case_study_v2` ({}) VALUES ({})'''.format(", ".join(key),", ".join(val)))
            # # sql = ('''INSERT INTO `webrep_case_study_v2` ({},`status`) VALUES ({},'Submitted')'''.format(", ".join(key),", ".join(val)))
            # last_row_id = db.do(sql)
            # Collect keys and values
            columns = []
            values = []
            for datum in data:
                value = urllib.parse.unquote(data[datum]) if isinstance(data[datum], str) else data[datum]
                columns.append(f"`{datum}`")
                values.append(value)

            # Add status column/value if needed
            # columns.append("`status`")
            # values.append("Submitted")

            # Build placeholders
            placeholders = ", ".join(["%s"] * len(values))

            # Construct SQL
            sql = f"INSERT INTO `webrep_case_study_v2` ({', '.join(columns)}) VALUES ({placeholders})"

            # Execute safely
            last_row_id = db.do(sql, values)
        else:
            print(" >> Editing Articles")
            # for datum in data:
            #     args += ",`{}`='{}'".format(datum,data[datum])
            # sql = "UPDATE `webrep_case_study_v2` SET  {} WHERE `id`='{}';".format(args[1:],request.form['id'])
            # pass
            
            if data.get("photo") == "":
                 del data["photo"]

            # Decode URL-encoded strings
            for key, value in list(data.items()):
                if isinstance(value, str):
                    data[key] = urllib.parse.unquote(value)

            # Build dynamic SET clause
            set_clause = ", ".join([f"`{key}`=%s" for key in data.keys()])

            # Construct SQL with placeholders
            sql = f"UPDATE `webrep_case_study_v2` SET {set_clause} WHERE `id`=%s"

            print(sql)
            
            # Values in the same order as keys, plus the id
            values = list(data.values()) + [request.form['id']]
            last_row_id = db.do(sql,values)
        
        return jsonify({"last_row_id":last_row_id})

 
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
    
    
    @app.route('/webrep_v2/upload-image', methods=['POST'])
    def upload_image():
        try:
            base_dir = os.path.join(current_app.root_path, 'static', 'webrepstatic_v2', 'img','embedded_images')
            # base_dir = c.RECORDS+"../static/webrepstatic_v2/img/embedded_images"
            os.makedirs(base_dir, exist_ok=True)
            
            if 'image' not in request.files:
                return jsonify({'error': 'No file'}), 400
            
            file = request.files['image']
            if file:
                filename = secure_filename(f"{uuid.uuid4().hex}_{file.filename}")
                file.save(os.path.join(base_dir, filename))
                
                # Return the public URL to the image
                img_url = url_for('static', filename=f'webrepstatic_v2/img/embedded_images/{filename}', _external=True)
                return jsonify({'url': img_url})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
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
            # columns.append("`status`")
            # values.append("pending")

            # Build placeholders for parameterization
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO `webrep_articles_v2` ({', '.join(columns)}) VALUES ({placeholders})"
            
        else:
            print(" >> Editing Articles")
            
            if data.get("file_name") == "":
             del data["file_name"]

            # Decode URL-encoded strings
            for key, value in list(data.items()):
                if isinstance(value, str):
                    data[key] = urllib.parse.unquote(value)

            # Build dynamic SET clause
            set_clause = ", ".join([f"`{key}`=%s" for key in data.keys()])

            # Construct SQL with placeholders
            # sql = f"UPDATE `webrep_articles_v2` SET {set_clause}, `status`='draft' WHERE `id`=%s"
            sql = f"UPDATE `webrep_articles_v2` SET {set_clause} WHERE `id`=%s"

            # Values in the same order as keys, plus the id
            values = list(data.values()) + [request.form['id']]

            # # Execute safely
            # cursor.execute(sql, values)
            # connection.commit()

        
        last_row_id = db.do(sql,values)
        return jsonify({"last_row_id":last_row_id,"FILES":__f})
    
    def send_newsletter_email(subject, content, recipients):
        # SMTP server configuration
        # SMTP_SERVER = "smtp.gmail.com"   # or your mail server
        # SMTP_PORT = 465                  # 465 for SSL, 587 for TLS
        # USERNAME = "dtirapid.noreply@gmail.com".strip()
        # PASSWORD = "anfg uzlh xlsp wess".replace("\xa0", "").strip()
        
        SMTP_SERVER = "email-smtp.ap-southeast-1.amazonaws.com"   # or your mail server
        SMTP_PORT = 587                  # 465 for SSL, 587 for TLS
        USERNAME = "AKIAQQ5WGXJBQADSVWUJ".strip()
        PASSWORD = "BOrNx6WPPZMmFBBjls63N58Whj5AEbKNSHvFce4VE9gU".replace("\xa0", "").strip()
        
        msg = MIMEMultipart("alternative")
        msg["From"] = "no-reply@dtirapid.ph"
        # msg["From"] = "dtirapid.noreply@gmail.com"
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(content, "html"))

        print("Sending email to:", recipients)

        try:
            # Use STARTTLS with port 587
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.set_debuglevel(1)  # logs SMTP conversation
                server.starttls()         # upgrade to secure connection
                server.login(USERNAME, PASSWORD)
                server.sendmail(msg["From"], recipients, msg.as_string())
            print("Email sent successfully")
        except Exception as e:
            print("Email sending failed:", e)
            
    @app.route("/webrep_v2/upload_file_webrep_newsletter",methods=["POST","GET"])
    def upload_file_webrep_newsletter():
        print("  * Article Module")
        from datetime import date, datetime
        from modules.Req_Brorn_util import file_from_request
        FILE_REQ = file_from_request(app)
        data = dict(request.form)
        key = [];val = [];args=""
        data["createdDate"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data["createdBy"] = session["USER_DATA"][0]['id']
        is_exist = len(db.select("SELECT * FROM `webrep_newsletters` WHERE `id` ='{}' ;".format(request.form['id'])))
        columns = []
        values = []
        if(is_exist==0):
            print(" >> Adding Newsletters")
            columns = []
            values = []

            if ( data.get("status") == "published" ):
                data["publishedDate"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data["publishedBy"] = session["USER_DATA"][0]['id']

                recipients = db.select("SELECT email FROM webrep_subscribers")
                recipient_emails = [recipient['email'] for recipient in recipients]
                
                data['recipients'] = ",".join(recipient_emails)
                data['totalRecipients'] = len(recipient_emails)
            
            
            for datum in data:
                columns.append(f"`{datum}`")
                value = data[datum]

                # Decode only if it's a string
                if isinstance(value, str):
                    value = urllib.parse.unquote(value)

                values.append(value)

            # Build placeholders for parameterization
            placeholders = ", ".join(["%s"] * len(values))
            sql = f"INSERT INTO `webrep_newsletters` ({', '.join(columns)}) VALUES ({placeholders})"
            
        else:
            print(" >> Editing Newsletters")

            if ( data.get("status") == "published" ):
                data["publishedDate"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                data["publishedBy"] = session["USER_DATA"][0]['id']
                
                recipients = db.select("SELECT email FROM webrep_subscribers")
                recipient_emails = [recipient['email'] for recipient in recipients]
                
                data['recipients'] = ",".join(recipient_emails)
                data['totalRecipients'] = len(recipient_emails)
                
            # Decode URL-encoded strings
            for key, value in list(data.items()):
                if isinstance(value, str):
                    data[key] = urllib.parse.unquote(value)

            # Build dynamic SET clause
            set_clause = ", ".join([f"`{key}`=%s" for key in data.keys()])

            # Construct SQL with placeholders
            # sql = f"UPDATE `webrep_articles_v2` SET {set_clause}, `status`='draft' WHERE `id`=%s"
            sql = f"UPDATE `webrep_newsletters` SET {set_clause} WHERE `id`=%s"

            # Values in the same order as keys, plus the id
            values = list(data.values()) + [request.form['id']]
        
        print(">> Newsletter Data:", data)  # Debugging line
        print(">> Newsletter Data Status:", data.get("status"))  # Debugging line
        
        if ( data.get("status") == "published" ):
            # Send the newsletter email to all subscribers
            subject = data.get('subject', 'No Subject')
            content = data.get('content', '')
            recipients = db.select("SELECT email FROM webrep_subscribers")
            recipient_emails = [recipient['email'] for recipient in recipients] 

            html = f"""
            <html>
            <style>
                .btn {{
                    display: inline-block;
                    padding: 5px 10px;
                    text-align: center;
                    text-decoration: none;
                    vertical-align: middle;
                    cursor: pointer;
                    -webkit-user-select: none;
                    -moz-user-select: none;
                    user-select: none;
                    transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
                }}
                .btn:hover {{
                    color: var(--bs-btn-hover-color);
                    background-color: var(--bs-btn-hover-bg);
                    border-color: var(--bs-btn-hover-border-color);
                }}
                .btn-primary {{
                    background-color: #0D6BF7;
                    color: #fff;
                    border-color: #0D6BF7;
                }}
                .btn-secondary {{
                    background-color: #6C757D;
                    color: #fff;
                    border-color: #6C757D;
                }}
                .btn-warning {{
                    background-color: #FFC107;
                    color: #000;
                    border-color: #FFC107;
                }}
                .btn-danger {{
                    background-color: #DC3545;
                    color: #fff;
                    border-color: #DC3545;
                }}
                .btn-success {{
                    background-color: #198754;
                    color: #fff;
                    border-color: #198754;
                }}
                .btn-info {{
                    background-color: #0DCAF0;
                    color: #000;
                    border-color: #0DCAF0;
                }}
                .btn-lime {{
                    background-color: #9AC156;
                    color: #000;
                    border-color: #9AC156;
                }}
                .btn-cyan {{
                    background-color: #004450;
                    color: #fff;
                    border-color: #004450;
                }}
            </style>
            <body>
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <div style="width: 500px; margin: 0 auto; background-color: #F6F6F6; padding: 20px; border-radius: 5px;">
                        {content}
                    </div>
                </div>
            </body>
            </html>
            """
            
            print(">> HTML Content:", html)  # Debugging line
            
            threading.Thread(target=_main.send_newsletter_email, args=(subject, html , recipient_emails)).start()

        last_row_id = db.do(sql,values)
        return jsonify({"last_row_id":last_row_id})