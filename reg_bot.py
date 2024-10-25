import telebot

bot = telebot.TeleBot('')
@bot.message_handler(content_types=['text'])
def user_greeting(message):
    print(message.text)
    bot.send_message(message.from_user.id, message.text)
bot.polling(none_stop=True, interval=0)