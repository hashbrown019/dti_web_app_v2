import socket

# =================================
IN_MAINTENANCE = False
# IN_MAINTENANCE = False
# =================================

print(" ++ Configuration Setting ++")
host_name = socket.gethostname()
IP_address = socket.gethostbyname(host_name)
# --- SYSTEM CONFIG --- #
SECRET_KEY = "@002342562988603673976#131452@HHPLHKHHH"
# HOST = host_name;

VIBER_TOKEN = "524fe3a9d127e6da-5e8765b3e533f3fc-c7abfcf58c51424"

LOCAL_IP ="127.0.0.1"
HOST = "0.0.0.0";
CUSTOM_HOST = "192.168.0.1";
PORT = 5000;
_PORT = 5000;
IS_DEBUG = True;

SQLITE_DB_LOCAL = "assets/sqlite_db/dti_rapidxi.db";
SQLITE_DB_SERVER = "/var/www/html/dti_web_app_v2/assets/sqlite_db/dti_rapidxi.db";
SQLITE_DB = "none";

RECORDS_LINUX_LOCAL= "/mnt/c/Users/USER/Desktop/Systems/dti_web_app_v2/assets/";
RECORDS_SERVER = "/var/www/html/dti_web_app_v2/assets/";
RECORDS_LOCAL = "assets/";
RECORDS = "none";

M_APPVER_LOCAL = "";
M_APPVER_SERVER = "/home/dtirapid/dti_web_app_v2/";
M_APPVER = "none";
# --- DATABASE---- #

LOCAL_PORT=3306
LOCAL_HOST = "127.0.0.1";
LOCAL_HOST_LINUX = "localhost";
LOCAL_USER = "root";
LOCAL_PASSWORD = "";
LOCAL_DATABASE = "mis_2023";

SERVER_PORT=3306;
# SERVER_HOST = "database-1.cpnzndp4qz0e.ap-southeast-1.rds.amazonaws.com"; # OLD ENDPOINTT
SERVER_HOST = "dti-rapid-database.cpnzndp4qz0e.ap-southeast-1.rds.amazonaws.com";
SERVER_USER = "admin";
SERVER_PASSWORD = "NRGlBUhehOvi0Yt4fDE5";
SERVER_DATABASE = "mis_2023";
# SERVER_PASSWORD = "password123"; # OLD PASSWORD

MOCK_DATABASE_TEST = "mis_2023_test";

# LOCAL_DATABASE = "dti_rapidxi";
IS_ON_SERVER = False;

# SERVER_PORT=3306;
# SERVER_HOST = "dtirapid.mysql.pythonanywhere-services.com";
# SERVER_USER = "dtirapid";
# SERVER_PASSWORD = "ruralagro";
# SERVER_DATABASE = "dtirapid$dti_rapidxi";

DB_CRED = [];

_SERVER_PORT=3306;
_HOST = "not initialized";
_USER = "not initialized";
_PASSWORD = "not initialized";
_DATABASE = "not initialized";


# =======for login auth===================================
login_auth_web = None
jinja_func = None
FLASK_APP = None


# =====Data CLEANING===========================================================
DATA_CLEAN_FORM_A_REF = {
	"frmer_prof_@_Farming_Basic_Info_@_DIP_name":{
		"table":"dcf_prep_review_aprv_status",
		"col":"form_1_anchor_firm"
	},
	"frmer_prof_@_Farming_Basic_Info_@_Name_coop":{
		"table":"form_b",
		"col":"organization_registered_name"
	},
	"farmer_dip_ref":{
		"table":"dcf_prep_review_aprv_status",
		"col":"form_1_anchor_firm"
	},
	"farmer_fo_name_rapid":{
		"table":"form_b",
		"col":"organization_registered_name"
	},
}

# ================================
global __STORE ;
__STORE = {} ;
# ================================

# _PORT
# _HOST
# _USER
# _PASSWORD
# _DATABASE

# SAMPLE 
# {
# 	"font_size": 8,
# 	"ignored_packages":
# 	[
# 		"Vintage",
# 	],
# 	"theme": "Adaptive.sublime-theme",
# 	"color_scheme": "Monokai.sublime-color-scheme",
# 	"spell_check": true,
# 	"drag_text": false,
# 	"show_tab_close_buttons": false,
# 	"hide_new_tab_button": true,
# 	"show_encoding": true,
# 	"show_line_endings": true,
# 	// "show_full_path": false,
# 	"show_rel_path": true,
# 	"show_project_first": true,
# }


# sudo rsync -a --info=progress2 --ignore-existing "dtirapid@ssh.pythonanywhere.com:dti_web_app_v2/assets/*" "/var/www/html/dti_web_app_v2/assets/"
