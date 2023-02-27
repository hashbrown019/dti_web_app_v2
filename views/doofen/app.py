from flask import Flask, render_template, redirect, flash, url_for


app = Flask(__name__)
	
@app.route("/")
def index():
	return redirect("dashboard")
	
@app.route("/dashboard")
def dashboard():
	return render_template('index.html')


@app.route("/respondents")
def b1():
	return render_template('B1-Respondents.html')


@app.route("/organizational")
def b2():
	return render_template('B2-Organizational.html')


@app.route("/operational")
def b3():
	return render_template('B3-Operational.html')


@app.route("/FoGCP")
def b4():
	return render_template('B4-FoGovernance.html')


@app.route("/admin")
def b5():
	return render_template('B5-Administrative.html')


@app.route("/capacity")
def b6():
	return render_template('B6-Capacity.html')



@app.route("/partnership")
def b7():
	return render_template('B7-Partnership.html')



if __name__ == "__main__":	
		app.run(debug=True)

