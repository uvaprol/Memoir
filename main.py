from flask import Flask, render_template, request
import json
from seting import *

def load_DB():
    with open('DATABASE/DB.json', 'r') as json_file:
        data = json.load(json_file)
    return data
def get_users():
    with open('DATABASE/LOGINS.json', 'r') as json_file:
        users = json.load(json_file)
    return users

DEV_MODE = False
app = Flask(__name__)

@app.route('/')
def main_render():
    return render_template('index.html')

@app.route('/enterance')
def enter_render():
    return render_template('enterance.html')

@app.route('/enter')
def user_check():
    login = request.args['login']
    password = request.args['password']
    users = get_users()
    if users.get(login) == password:
        return 'true'
    return 'false'

@app.route('/send_data_users')
def send_data():
    if request.args['password'] == API_PASSWORD:
        with open('DATABASE/USERS.json', 'r') as json_file:
            USERS = json.load(json_file)
        with open('DATABASE/LOGINS.json', 'r') as json_file:
            LOGINS = json.load(json_file)
        return [USERS, LOGINS]
    return ''

@app.route('/save_data_users')
def save_DATABASE():
    if request.args['password'] == API_PASSWORD:
        U_data = eval(request.args['U_data'])
        L_data = eval(request.args['L_data'])
        with open('DATABASE/USERS.json', 'w') as json_file:
            json.dump(U_data, json_file)
        with open('DATABASE/LOGINS.json', 'w') as json_file:
            json.dump(L_data, json_file)
    return 'True'
app.run(host='0.0.0.0', port=80, debug=DEV_MODE)