https://036352473667.signin.aws.amazon.com/console

036352473667
user: dti-christian
password: P@ssword!


Database Credentials
username : admin
password : password! - RDS




============pythonanywhere to AWS======================================

scp -r "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/*" "/var/www/html/DTI-Web-App/assets/"

sudo rsync -a --progress --ignore-existing "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/*" "/var/www/html/DTI-Web-App/assets/"






===============pythonanywhere to local WLS===================================

scp -r "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/*" "C:\_SYSTEMS\DTI-Web-App\assets"

sudo rsync -a --progress --ignore-existing "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/*" "C:\_SYSTEMS\DTI-Web-App\assets"
=====================================================


===============local WLS to AWS===================================

scp -r "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/*" "C:\_SYSTEMS\DTI-Web-App\assets"

sudo rsync -a --progress --ignore-existing "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/*" "C:\_SYSTEMS\DTI-Web-App\assets"

=====================================================




NEW==NEW==NEW==NEW==NEW== SYSTEM NEW==NEW==NEW==NEW==NEW==

============pythonanywhere to AWS======================================
!!!WORKING - MOBILE
sudo rsync -a --progress --ignore-existing "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/records/profiles/__temp__/" "/var/www/html/dti_web_app_v2/assets/objects/profiling_forms/queued/pf_a/"

!!!WORKING - EXCEL
sudo rsync -a --progress --ignore-existing "dtirapid@ssh.pythonanywhere.com:DTI-Web-App/assets/records/spreadsheets/" "/var/www/html/dti_web_app_v2/assets/objects/spreadsheets/queued/"

=====================================================
=== to access assets older publicly 
sudo chmod -R 777 directory/









sudo service apache2 restart

sudo tail -f /var/log/apache2/error.log


13.214.147.151 === TEST IP

==============


HOW TO !! LEGIT!!!
https://jqn.medium.com/deploy-a-flask-app-on-aws-ec2-1850ae4b0d41