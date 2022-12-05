import telebot
from parsing import get_report
from token_tg import token_bot
from telebot import types
import os
# from test_file import filling_file


def valid_id(id):
    print(id)
    with open('users_id.txt') as file:
        for i in file:
            print(i[:-1]+':')
            if id == i[:-1]:
                print('122')
                return 1
    return 0


bot = telebot.TeleBot(token_bot)


@bot.message_handler(commands=['start'])
def start(message):
    file = open('Пустой отчет.xlsx', 'rb')
    standart_mess = 'Это пустой отчет, заполни в нем даты работы,' \
                    'регистранционный номер и талон,' \
                    'и прикрепи этот файл сюда для того чтобы я его заполнил!)'
    mess = f'Hello, {message.from_user.first_name}'
    bot.send_message(message.chat.id, f'{mess} \n{standart_mess}')
    bot.send_document(message.chat.id, file)


@bot.message_handler(commands=['emptyReport'])
def empty_report(message):
    file = open('Пустой отчет.xlsx', 'rb')
    bot.send_document(message.chat.id, file)


@bot.message_handler(commands=['help'])
def menu(massage):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    start = types.KeyboardButton('/start')
    empty_report = types.KeyboardButton('/emptyReport')
    markup.add(start, empty_report)
    bot.send_message(massage.chat.id, 'Выбери команду!',reply_markup=markup)


@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    print(message)
    if valid_id(str(message.from_user.id)):
        os.listdir('C:\Bot_wialon\wialon\Report/')
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            src = 'C:\Bot_wialon\wialon\Report/' + message.document.file_name;
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, "Это может занять какое-то время...")
        except Exception as e:
            bot.reply_to(message, e)
        try:
            rezult = 'No company'
            if message.caption != None:
                rezult = get_report(message.caption, message.document.file_name)
                if rezult != 'bad company':
                    file = open('C:\Bot_wialon\wialon\Report/' + message.document.file_name, 'rb')
                    bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, str(rezult))
        except:
            print("TYT")
    else:
        bot.send_message(message.chat.id, 'Вас нет в системе.')
    # os.remove('C:\Bot_wialon\wialon\Report/' + message.document.file_name)
    # filling_file_name = filling_file(f'C:\_wialon\wialo/{message.document.file_name}')
    # file = open(filling_file_name, 'rb')
    # bot.send_document(message.chat.id, file)


bot.polling(none_stop=True)
