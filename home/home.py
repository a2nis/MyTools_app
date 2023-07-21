from flask import Blueprint, render_template

home = Blueprint("home", __name__, static_folder="static", template_folder="templates")

@home.route("/")
def home_page():
  return render_template('index.html')