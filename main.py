from flask import Flask, render_template, request, jsonify
import json
from seting import *

def load_DB():
    with open('DATABASE/DB.json', 'r') as json_file:
        data = json.load(json_file)
    return data


def get_users():
    with open('DATABASE/USERS.json', 'r') as json_file:
        data = json.load(json_file)
    return data


DEV_MODE = False
app = Flask(__name__)

@app.route('/memoir')
def main_render():
    return render_template('index.html', months=MONTHS)

@app.route('/')
def enter_render():
    return render_template('enterance.html')

@app.route('/enter', methods = ['POST'])
def user_check():
    login = request.form.get('login')
    password = request.form.get('password')
    user = get_reg_data(login)[0]
    if user[2] == password:
        return 'true', 200
    return 'false', 400

# @app.route('/send_data_users', methods = ['POST'])
# def send_data():
#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#     if data.get('password') == API_PASSWORD:
#         response = {
#             'message': 'Data received successfully',
#             'L_data': get_logins(),
#             'U_data': get_users(),
#         }
#         return jsonify(response), 200
#     return 'Data received successfully', 400
#
# @app.route('/save_data_users', methods = ['POST'])
# def save_DATABASE():
#     data = request.json
#     U_data = data.get('U_data')
#     L_data = data.get('L_data')
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400
#     if data.get('password') == API_PASSWORD:
#         with open('DATABASE/USERS.json', 'w') as json_file:
#             json.dump(U_data, json_file)
#         with open('DATABASE/LOGINS.json', 'w') as json_file:
#             json.dump(L_data, json_file)
#     return 'Data received successfully', 200

app.run(host='0.0.0.0', port=80, debug=DEV_MODE)