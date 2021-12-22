import telebot
from telebot import types
import random
from pasing import *
pin = 0
user = ''
log = ''
file_wipe('pins.txt')
verification = False

bot = telebot.TeleBot('')#Токен бота

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введи логин с сайта")
        bot.register_next_step_handler(message, get_user)#Приём сообщения пользователя
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_user(message):
    global user
    user = message.text
    bot.send_message(message.from_user.id, 'Введите пароль с сайта')
    bot.register_next_step_handler(message, get_log)

def get_log(message):
    global log
    log = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = 'Ваш логин ' + user + ' и ваш пароль ' + log + '. Верно?'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global verification
    if call.data == "yes":
        pin = random.randrange(100, 999)

        i = -2
        try:
            while i < len(users):
                i += 2
                if user == users[i] and log == users[i + 1]:
                    verification = True
                    break
            if verification == True:
                bot.send_message(call.message.chat.id, f'Ваш пин-код: {pin}')
                pin = str(pin)
                file_writer('pins.txt', pin)

        except IndexError:

            bot.send_message(call.message.chat.id, 'Неверный логин или пароль. Попробуй ещё раз /reg')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Попробуй ещё раз /reg')

bot.polling(none_stop=True, interval=0)
