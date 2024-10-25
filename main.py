from flask import Flask, render_template, request
import pandas as pd
import json


DEV_MODE = False
app = Flask(__name__)
def load_DB():
    with open('DATABASE/DB.json', 'r') as json_file:
        data = json.load(json_file)
    return data
def get_users():
    with open('DATABASE/LOGINS.json', 'r') as json_file:
        users = json.load(json_file)
    return users
# print(load_DB()['uvaprol']['Password'])
@app.route('/')
def main_render():
    return render_template('index.html')

@app.route('/enterance')
def Enter_or_Registration():
    return render_template('enterance.html')

@app.route('/enter')
def user_check():

    login = request.args['login']
    password = request.args['password']
    users = get_users()
    try:
        if users[login] == password:
            return 'true'
        return 'false'
    except:
        return 'false'

app.run(host='0.0.0.0', port=80, debug=DEV_MODE)