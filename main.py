from flask import Flask, render_template, request, jsonify
from seting import *
from datetime import date, datetime
import sqlite3
def get_memoirs(name: str, year: int = date.today().year, month: int = date.today().month, key: bool = True) -> dict:
    memoirs: dict = {}
    connection = sqlite3.connect(DB_CONNECT[1])
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT '
        f'{ROWS[1][4]}, '
        f'{ROWS[1][3]}, '
        f'{ROWS[1][5]}, '
        f'{ROWS[1][6]}, '
        f'{ROWS[1][7]}, '
        f'{ROWS[1][8]} '
        f'FROM {TABLES[1]} '
        f'WHERE '
        f'{ROWS[1][0]} = "{name}" '
        f'AND {ROWS[1][1]} = {year} '
        f'AND {ROWS[1][2]} = {month} '
        f'ORDER BY '
        f'{ROWS[1][4]} ASC, '
        f'{ROWS[1][5]} ASC;'
    )
    data = cursor.fetchall()
    connection.close()
    print(data)
    if data:
        for d in data:
            if memoirs.get(d[0]) == None:
                memoirs[d[0]] = {d[1]: (d[2], d[3])}
            else:
                memoirs[d[0]].update({d[1]: (d[2], d[3], d[4], d[5])})
    elif month != date.today().month:
        return {'STATE': 400, 'MESSAGE': 'Запись отсутсвует'}
    elif key:
        get_calendar(user=name)
        get_memoirs(name=name, key=False)
    else:
        return {'STATE': 400, 'MESSAGE': 'Ошибка загрузки\nСвяжитесь с тех.поддержкой'}
    return {'STATE': 200,'MESSAGE': memoirs}

def get_calendar(user: str, day: int = datetime.today().weekday(), todate: str = str(date.today())) -> bool:
    connection = sqlite3.connect(DB_CONNECT[1])
    cursor = connection.cursor()
    md = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    ty, tm, td = map(int, todate.split('-'))
    if (ty % 4 == 0 and ty % 100 != 0) or (ty % 400 == 0):
        md[2] += 1
    week = 1
    for i in range(td, md[tm] + 1):
        if day == 7:
            day = 0
            week += 1
        cursor.execute(
            f'INSERT INTO {TABLES[1]} '
            f'({ROWS[1][0]}, '
            f'{ROWS[1][1]}, '
            f'{ROWS[1][2]}, '
            f'{ROWS[1][3]}, '
            f'{ROWS[1][4]}, '
            f'{ROWS[1][5]}, '
            f'{ROWS[1][6]}) '
            f'VALUES '
            f'("{user}", '
            f'{ty}, '
            f'{tm}, '
            f'{i}, '
            f'{week}, '
            f'{day}, '
            f'"")'
        )
        day += 1
    connection.commit()
    connection.close()
    return True
def check_user_data(name: str, year: int = date.today().year) -> bool:
    connection = sqlite3.connect(DB_CONNECT[1])
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * '
        f'FROM {TABLES[1]} '
        f'WHERE '
        f'{ROWS[1][0]} = "{name}" '
        f'AND {ROWS[1][1]} = "{year}" '
        f'LIMIT 1'
    )
    data = cursor.fetchone()
    connection.close()
    if data == None:
        return False
    return True
def get_reg_data(name: str) -> tuple:
    connection = sqlite3.connect(DB_CONNECT[0])
    cursor = connection.cursor()
    cursor.execute(
        f'SELECT * '
        f'FROM {TABLES[0]} '
        f'WHERE '
        f'{ROWS[0][0]} = "{name}" '
        f'LIMIT 1'
    )
    user = cursor.fetchone()
    connection.close()
    return user
def new_reg(login: str, passwor: str, mail: str) -> bool:
    if get_reg_data(login) == None:
        connection = sqlite3.connect(DB_CONNECT[0])
        cursor = connection.cursor()
        cursor.execute(
            f'INSERT INTO {TABLES[0]} '
            f'({ROWS[0][0]}, '
            f'{ROWS[0][1]}, '
            f'{ROWS[0][2]}) '
            f'VALUES '
            f'("{login}", '
            f'"{passwor}", '
            f'"{mail}")'
        )
        connection.commit()
        connection.close()
        return True
    return False
def update_memory(login: str, day: tuple, text: str) -> bool:
    try:
        connection = sqlite3.connect(DB_CONNECT[1])
        cursor = connection.cursor()
        cursor.execute(
            f'UPDATE {TABLES[1]} '
            f'SET {ROWS[1][6]} = "{text}"'
            f'WHERE {ROWS[1][0]} = "{login}" '
            f'AND {ROWS[1][1]} = {day[0]} '
            f'AND {ROWS[1][2]} = {day[1]} '
            f'AND {ROWS[1][3]} = {day[2]} '
        )
        connection.commit()
        connection.close()
        return True
    except:
        return False
def update_value(login: str, day: tuple, val: str) -> bool:
    try:
        connection = sqlite3.connect(DB_CONNECT[1])
        cursor = connection.cursor()
        cursor.execute(
            f'UPDATE {TABLES[1]} '
            f'SET {ROWS[1][7]} = "{val}"'
            f'WHERE {ROWS[1][0]} = "{login}" '
            f'AND {ROWS[1][1]} = {day[0]} '
            f'AND {ROWS[1][2]} = {day[1]} '
            f'AND {ROWS[1][3]} = {day[2]} '
        )
        connection.commit()
        connection.close()
        return True
    except:
        return False
def update_point(login: str, day: tuple, val: bool) -> bool:
    try:
        connection = sqlite3.connect(DB_CONNECT[1])
        cursor = connection.cursor()
        cursor.execute(
            f'UPDATE {TABLES[1]} '
            f'SET {ROWS[1][8]} = {not val} '
            f'WHERE {ROWS[1][0]} = "{login}" '
            f'AND {ROWS[1][8]} = {val} '
            f'AND {ROWS[1][1]} = {day[0]} '
            f'AND {ROWS[1][2]} = {day[1]} '
            f'AND {ROWS[1][4]} = {day[3]} '
        )
        cursor.execute(
            f'UPDATE {TABLES[1]} '
            f'SET {ROWS[1][8]} = {val} '
            f'WHERE {ROWS[1][0]} = "{login}" '
            f'AND {ROWS[1][1]} = {day[0]} '
            f'AND {ROWS[1][2]} = {day[1]} '
            f'AND {ROWS[1][3]} = {day[2]} '
        )
        connection.commit()
        connection.close()
        return True
    except:
        return False
# def return_memory(login: str, day: tuple) -> str:
#     connection = sqlite3.connect(DB_CONNECT[1])
#     cursor = connection.cursor()
#     cursor.execute(
#         f'SELECT {ROWS[1][6]}, {ROWS[1][7]} FROM {TABLES[1]} '
#         f'WHERE {ROWS[1][0]} == "{login}" '
#         f'AND {ROWS[1][1]} == "{day[0]}" '
#         f'AND {ROWS[1][2]} == "{day[1]}" '
#         f'AND {ROWS[1][3]} == "{day[2]}" '
#         f'LIMIT 1'
#     )
#     memoir = cursor.fetchone()
#     connection.close()
#     return memoir




DEV_MODE = False
app = Flask(__name__)

@app.route('/memoir_save', methods=['POST'])
def save_memoir():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        memoir = request.form.get('Memoir')
        day = request.form.get('Date')
        user = get_reg_data(login)
        if user != None and user[1] == password and memoir != '':
            day = day.split('_')
            # print(update_memory(login, day, memoir))
            if update_memory(login, day, memoir):
                return '', 200
            else:
                # memoir = return_memory(login, day)
                return '', 400
@app.route('/value_save', methods=['POST'])
def save_val():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        val = request.form.get('Value')
        day = request.form.get('Date')
        user = get_reg_data(login)
        if user != None and user[1] == password and val != '':
            day = day.split('_')
            # print(update_value(login, day, val))
            if update_value(login, day, val):
                return '', 200
            else:
                # memoir = return_memory(login, day)
                return '', 400
@app.route('/point_save', methods=['POST'])
def save_point():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        val = True if request.form.get('Value') == 'on' else False
        day = request.form.get('Date')
        user = get_reg_data(login)
        if user != None and user[1] == password:
            day = day.split('_')
            # print(update_value(login, day, val))
            if update_point(login, day, val):
                return '', 200
            else:
                # memoir = return_memory(login, day)
                return '', 400
@app.route('/memoir', methods=['POST', 'GET'])
def get_memoir():
    if request.method == 'POST':
        login = request.form.get('Login')
        password = request.form.get('Password')
        year = int(request.form.get('Year'))
        month = int(request.form.get('Month'))
        user = get_reg_data(login)
        if user and user[1] == password:
            memoirs = get_memoirs(name=login, year=year, month=month)
            return jsonify(memoirs['MESSAGE']), memoirs['STATE']
    return render_template('index.html', months=MONTHS)
@app.route('/', methods=['POST', 'GET'])
def enter_render():
    if request.method == 'POST':
        mode = request.form.get('Mode')
        login = request.form.get('Login')
        password = request.form.get('Password')
        email = request.form.get('Email')
        if mode == 'true':
            if new_reg(login, password, email):
                if get_calendar(login):
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