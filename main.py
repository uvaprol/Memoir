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
def get_calendar(day: int, todate: str = str(date.today()), y: list = []) -> list:
    md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    ty, tm, td = map(int, todate.split('-'))
    if (ty % 4 == 0 and ty % 100 != 0) or (ty % 400 == 0):
        md[2] += 1
    for m, d in md.items():
        week = 1
        for i in range(1, d+1):
            if day == 8:
                day = 1
                week += 1
            if m == tm and i >= td or m > tm:
                r = [("uvaprol", ty, m, i, week, day, "")]
                y += r
                print(*r)
            day += 1
    return y
def check_user_data(name: str, year: str = date.today().year) -> bool:
    connection = sqlite3.connect(DB_CONNECT[1])
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {TABLES[1][0]} WHERE {ROWS[1][0]} == "{name}" AND {ROWS[1][1]} == "{year}" LIMIT 1')
    data = cursor.fetchone()
    connection.close()
    if data == None:
        return False
    return True
def get_reg_data(name: str) -> tuple:
    connection = sqlite3.connect(DB_CONNECT[0])
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {TABLES[0][0]} WHERE {ROWS[0][0]} == "{name}" LIMIT 1')
    user = cursor.fetchone()
    connection.close()
    return user
def new_reg(login: str, passwor: str, mail: str) -> bool:
    if get_reg_data(login) == None:
        connection = sqlite3.connect(DB_CONNECT[0])
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO {TABLES[0][0]} ({ROWS[0][0]}, {ROWS[0][1]}, {ROWS[0][2]}) VALUES ("{login}", "{passwor}", "{mail}")')
        connection.commit()
        connection.close()
        return True
    return False

def data_rerender():
    return render_template('index.html', month=MONTHS, week_days=WEEK_DAYS, memoirs={1: {2: 'el'}})

DEV_MODE = False
app = Flask(__name__)

@app.route('/memoir', methods = ['POST', 'GET'])
def get_memoir():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        user = get_reg_data(login)
        if user != None and user[1] == password:
            return '', 200
    return render_template('index.html', month=MONTHS, memoirs={})
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