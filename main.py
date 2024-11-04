from flask import Flask, render_template, request, jsonify
import json
from seting import *
from datetime import date
import sqlite3
# def get_memoirs(name: str, year: str = date.today().year, month: str = date.today().month, memoirs: dict = {}) -> dict:
#     connection = sqlite3.connect(DB_CONNECT)
#     cursor = connection.cursor()
#     cursor.execute(f'SELECT {ROWS[1][3]}, {ROWS[1][4]}, {ROWS[1][5]} FROM {TABLES[1]} WHERE {ROWS[1][0]} == "{name}" AND {ROWS[1][1]} == "{year} AND {ROWS[1][2]} == "{month}" ORDER BY {ROWS[1][3]} ASC, {ROWS[1][4]} ASC;')
#     data = cursor.fetchall()
#     connection.close()
#     for d in data:
#         if memoirs.get(d[0]) == None:
#             memoirs[d[0]] = {}
#         else:
#             memoirs[d[0]].update({d[1]: d[2]})
#     return memoirs
def get_reg_data(name: str) -> tuple:
    connection = sqlite3.connect(DB_CONNECT[0])
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {TABLES[0]} WHERE {ROWS[0][0]} == "{name}" LIMIT 1')
    user = cursor.fetchone()
    connection.close()
    return user
def new_reg(login: str, passwor: str, mail: str) -> bool:
    if get_reg_data(login) == None:
        print(get_reg_data(login))
        connection = sqlite3.connect(DB_CONNECT[0])
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO {TABLES[0]} ({ROWS[0][0]}, {ROWS[0][1]}, {ROWS[0][2]}) VALUES ("{login}", "{passwor}", "{mail}")')
        connection.commit()
        connection.close()
        return True
    return False

DEV_MODE = False
app = Flask(__name__)

@app.route('/memoir', methods = ['POST', 'GET'])
def main_render():
    return '<script>alert( localStorage.getItem("login") );</script>' #render_template('index.html', months=MONTHS, week_days=WEEK_DAYS, user=name, memoirs=[])

@app.route('/', methods = ['POST', 'GET'])
def enter_render():
    if request.method == 'POST':
        mode = request.form.get('Mode')
        login = request.form.get('Login')
        password = request.form.get('Password')
        email = request.form.get('Email')
        if mode == 'true':
            if new_reg(login, password, email):
                return '', 200
            else:
                return 'Логин занят', 400
        else:
            user = get_reg_data(login)
            if user != None and user[1] == password:
                return '', 200
            return 'Неверный логин или пароль', 400
    return render_template('enterance.html')

app.run(host='0.0.0.0', port=80, debug=DEV_MODE)