from flask import Flask, render_template, redirect, flash, url_for


app = Flask(__name__)
	
@app.route("/")
def index():
	return redirect("dashboard")
	

if __name__ == "__main__":	
		app.run(debug=True)

