from flask import Flask, jsonify, render_template, request, redirect, url_for, Blueprint

import time, os, PyPDF2
from app.authentication.login import login
from app.authentication.profiles import Profiles
# from app.authentication.extr import ResumeParser

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
app_blueprint = Blueprint('app_blueprint', __name__, static_folder='app/static', template_folder='app/templates')

@app_blueprint.route('/')
def base():
    return render_template('/layouts/base.html')

@app_blueprint.route('/index')
def index():
    return render_template('/home/index.html')

@app_blueprint.route("/login", methods=["POST", "GET"]) 
def login_page():
    return login()

@app_blueprint.route('/index', methods=['POST'])
def select():
    username = 'ashleykhanaasmara61@gmail.com'
    password = 'aasmara@61'
    choice = request.form.get('choice_select')
    target = request.form.get('target')
    location = request.form.get('location')
    options = None
    scraper = Profiles(username, password, choice, target, location, options)
    scraper.login()
    scraper.collect_links()
    response_data = {'message': 'Scraping completed successfully'}
    return jsonify(response_data)

app.register_blueprint(app_blueprint)
if __name__ == '__main__':
    app.run(debug=True)
