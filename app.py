from flask import Flask
from flask import url_for, redirect, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "In home"

if __name__=="__main__":
    app.run(debug=True)
    