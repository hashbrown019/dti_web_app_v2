from flask import Flask, Blueprint,request, flash, render_template, url_for,redirect, session,send_file
import Configurations as c

app = Blueprint("tests",__name__,template_folder="pages")

@app.route('/_test_',methods=["GET","POST"])
def _test_():
    return render_template("home.html")
