import telebot
from seting import *
import json

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



with open('USERS.json', 'r') as json_file:
    USERS = json.load(json_file)

def user_del(u):
    return



bot = telebot.TeleBot(API_KEY)
@bot.message_handler(content_types=['text'])
def user_greeting(message):
    global REG_SRC, USERS
    text = message.text
    user = message.from_user.id
    print(user)
    if text == '/start':
        bot.send_message(message.from_user.id, WELCOME_MSG)
        USERS[user] = {'action': ''}
    elif text == '/del':
        bot.send_message(message.from_user.id, 'Вы точно хотите удалить свою учетную запись\n/y\n/n')
        USERS[user].update({'action': 'del'})
    elif text == '/set_login':
        USERS[user].update({'action': 'set_login'})
        bot.send_message(message.from_user.id, 'Введите логин')
    elif text == '/set_password':
        USERS[user].update({'action': 'set_password'})
        bot.send_message(message.from_user.id, 'Введите пароль')
    elif text == '/regestration':
        if USERS[user].get('login') != None and USERS[user].get('password') != None:
            USERS[user].update({'action': ''})
            REG_SRC = REG_SRC.replace('{login}', USERS[user]['login'])
            REG_SRC = REG_SRC.replace('{password}', USERS[user]['password'])
            bot.send_message(message.from_user.id, REG_SRC)
        elif USERS[user].get('login') != None:
            bot.send_message(message.from_user.id, 'Создайте логин\n/set_login')
        else:
            bot.send_message(message.from_user.id, 'Создайте пароль\n/set_password')
    elif text == '/help':
        USERS[user].update({'action': 'help'})
        bot.send_message(message.from_user.id, 'Введите сообщение')
    elif text == '/exit':
        USERS[user].update({'action': 'help'})
        bot.send_message(message.from_user.id, 'Чтобы прочесть инструкцию введите\n/start')
    elif USERS[user]['action'] == 'del' and text.find('y') != -1:
        user_del(user)
    elif USERS[user]['action'] == 'del' and text.find('n') != -1:
        USERS[user].update({'action': ''})
    elif USERS[user]['action'] == 'help':
        for i in ADMINS_ID:
            bot.send_message(i, f'/{user}\n{text}')
        bot.send_message(message.from_user.id, 'Ваше сообщение отправлено оператор свяжется с вами'
                                               '\nдля выхода из режима диалога с оператором введите'
                                               '\n/exit')
    elif USERS[user]['action'] == 'set_login':
        if USERS[user].get('login') != None:
            bot.send_message(message.from_user.id, 'Этот логин уже занят')
        else:
            USERS[user].update({'login': text})
            if USERS[user].get('login') != None and USERS[user].get('password') != None:
                bot.send_message(message.from_user.id, 'Теперь зарегистрируйте пользователя\n/regestration')
            else:
                bot.send_message(message.from_user.id, 'Создайте пароль\n/set_password')
                USERS[user].update({'action': ''})
    elif USERS[user]['action'] == 'set_password':
        USERS[user].update({'password': text})
        if USERS[user].get('login') != None and USERS[user].get('password') != None:
            bot.send_message(message.from_user.id, 'Теперь зарегистрируйте пользователя\n/regestration')
        else:
            bot.send_message(message.from_user.id, 'Создайте логин\n/set_login')
            USERS[user].update({'action': ''})



bot.polling(none_stop=True, interval=0)
