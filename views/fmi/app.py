from flask import Flask, render_template, url_for,flash
import bp_app as bp
app = Flask(__name__)
app.register_blueprint(bp.app)
app.secret_key = 'fmi'
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")