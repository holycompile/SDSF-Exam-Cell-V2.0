from flask import Flask
from flask import url_for, redirect, render_template
from flask import Blueprint
import os

app = Flask(__name__)


app.secret_key=os.getenv("SECRET_KEY")

from routes.admin import admin_bp
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route("/")
def home():
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True)
    