
from flask import Flask, redirect, url_for, render_template, request

email = 'admin@gmail.com'
password = '123'
def login():  
    email = request.form['email']
    password = request.form['password']
    if request.method == "POST" and email == email and password == password:
        return redirect(url_for("app_blueprint.index")) 
    return redirect(url_for('app_blueprint.base')) 