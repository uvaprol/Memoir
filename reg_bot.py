import telebot
from seting import *
import json
import re
import requests

WELCOME_MSG = 'Привет, я твой бот асистент!\n' \
              'Я буду следить за твоей учетной записью.\n' \
              'И помогать тебе с доступом к ней.\n' \
              'Для начала давай зарегистрируемся.\n' \
              'Для этого воспользуйся командами:\n' \
              '/set_login\n' \
              '/set_password\n' \
              'чтобы создать логин и пароль для своей учетной записи.\n' \
              'Также эти команды позволят тебе изменить их в будущем\n' \
              '\n' \
              'После создания учетной записи не забудьте ее зарегистроровать\n' \
              '/regestration\n' \
              '\n' \
              'Для удаление записи воспользуйтесь командой\n' \
              '/del\n' \
              '\n' \
              'Для связи с поддержкой введите\n' \
              '/help'


def save_DATABASE(U_data, L_data):
    response = requests.get(f'{API_URL}/save_data_users?U_data={U_data}&L_data={L_data}&password={API_PASSWORD}')
    if response.status_code != 200:
        print(False)


response = requests.get(f'{API_URL}/send_data_users?password={API_PASSWORD}')
USERS, LOGINS = eval(response.text)
save_DATABASE(USERS, LOGINS)

def user_del(u):
    return



bot = telebot.TeleBot(API_KEY)
try:
    @bot.message_handler(content_types=['text'])
    def bot_comand(message):
        global REG_SRC, USERS, LOGINS
        text = message.text
        user = message.from_user.id
        user = str(user)

        # ---------------------ADMIN----------------------------
        if int(user) in ADMINS_ID:
            if text == ADMINS_COMMAND[0]:
                raise Exception('Finish')
            elif text == ADMINS_COMMAND[1]:
                USERS, LOGINS = {}, {}
                save_DATABASE(USERS, LOGINS)
            elif re.match(r'/\d', text) != None:
                pass

        # ---------------------WELCOME--------------------------
        if USERS.get(user) == None:
            USERS[user] = {'action': ''}
        elif text == '/start':
            bot.send_message(message.from_user.id, WELCOME_MSG)
            USERS[user]['action'] = ''

        # ---------------------COMANDS---------------------------
        elif text == '/set_login':
            if USERS[user].get('login') != None:
                bot.send_message(message.from_user.id, 'Вы можете изменять только пароль\n'
                                                       '/set_password\n'
                                                       'Если хотите удалить свою запись воспользуйтесь\n'
                                                       '/del')
            else:
                USERS[user]['action'] = 'set_login'
                bot.send_message(message.from_user.id, 'Введите логин')
        elif text == '/del':
            bot.send_message(message.from_user.id, 'Вы точно хотите удалить свою учетную запись\n/y\n/n')
            USERS[user]['action'] = 'del'
        elif text == '/set_password':
            USERS[user]['action'] = 'set_password'
            bot.send_message(message.from_user.id, 'Введите пароль')
        elif text == '/regestration':
            if USERS[user].get('login') != None and USERS[user].get('password') != None:
                USERS[user]['action'] = ''
                REG_SRC = REG_SRC.replace('{login}', USERS[user]['login'])
                REG_SRC = REG_SRC.replace('{password}', USERS[user]['password'])
                bot.send_message(message.from_user.id, REG_SRC)
                print(LOGINS)
                save_DATABASE(USERS, LOGINS)
            elif USERS[user].get('login') == None:
                bot.send_message(message.from_user.id, 'Создайте логин\n/set_login')
            else:
                bot.send_message(message.from_user.id, 'Создайте пароль\n/set_password')
        elif text == '/help':
            USERS[user]['action'] = 'help'
            bot.send_message(message.from_user.id, 'Введите сообщение')
        elif text == '/exit':
            USERS[user]['action'] = ''
            bot.send_message(message.from_user.id, 'Чтобы прочесть инструкцию введите\n/start')

        # -----------------------ACTIONS------------------------
        elif USERS[user]['action'] == 'help':
            for i in ADMINS_ID:
                bot.send_message(i, f'/{user}\n{text}')
            bot.send_message(message.from_user.id, 'Ваше сообщение отправлено оператор свяжется с вами'
                                                   '\nдля выхода из режима диалога с оператором введите'
                                                   '\n/exit'
                                                   '\nили любую другую команду')
        elif USERS[user]['action'] == 'del' and text.find('y') != -1:
            user_del(user)
        elif USERS[user]['action'] == 'del' and text.find('n') != -1:
            USERS[user]['action'] = ''
        elif USERS[user]['action'] == 'set_login':
            if text in LOGINS:
                bot.send_message(message.from_user.id, 'Этот логин уже занят')
            else:
                USERS[user]['login'] = text
                LOGINS.update({text: USERS[user].get('password')})
                if USERS[user].get('password') != None:
                    bot.send_message(message.from_user.id, 'Теперь зарегистрируйте пользователя\n/regestration')
                else:
                    bot.send_message(message.from_user.id, 'Создайте пароль\n/set_password')
                    USERS[user]['action'] = ''
        elif USERS[user]['action'] == 'set_password':
            USERS[user]['password'] = text
            if USERS[user].get('login') != None:
                LOGINS.update({USERS[user].get('login'): USERS[user].get('password')})
                bot.send_message(message.from_user.id, 'Теперь зарегистрируйте пользователя\n/regestration')
            else:
                bot.send_message(message.from_user.id, 'Создайте логин\n/set_login')
                USERS[user]['action'] = ''

    bot.polling(none_stop=True, interval=0)

except:
    save_DATABASE(USERS, LOGINS)