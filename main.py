import telebot
from parsing import get_report
from token_tg import token_bot
from telebot import types
import os
import json
from token_wialon import info
# from test_file import filling_file


bot = telebot.TeleBot(token_bot)
markup_user = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
markup_admin = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
empty_report = types.KeyboardButton('/Пустой отчет')
download_report = types.KeyboardButton('/Загрзуить отчет')
add_user = types.KeyboardButton('/Добавить пользователя')
delete_user = types.KeyboardButton('/Удалить пользователя')
all_user = types.KeyboardButton('/Все пользователи')
request_user = types.KeyboardButton('/Запросы')
add_admin = types.KeyboardButton('/Новый админ')
add_password = types.KeyboardButton('/Изменить токен')
# all_password = types.KeyboardButton('/Сайты и пароли')
markup_user.add(empty_report, download_report)
markup_admin.add(add_user, delete_user, all_user, add_admin, add_password, request_user, empty_report, download_report)
users_request = {

}
admin_all = {

}
password_all = {

}
password = ''

def valid_user(file_name, user_id):
    with open(file_name, "r", encoding='utf-8') as file:
        data = file.read()
        if data:
            result = json.loads(data)
            for el in result:
                if result[el] == user_id:
                    return 1
    return 0


@bot.message_handler(commands=['start'])
def start(message):
    try:
        if valid_user('all_users.json', message.from_user.id):
            bot.send_message(message.chat.id, 'Выбери команду!', reply_markup=markup_user)
        elif valid_user('admin.json', message.from_user.id):
            bot.send_message(message.chat.id, 'Выбери команду!', reply_markup=markup_admin)
        else:
            bot.send_message(message.chat.id, 'Вас нет в системе.')
            user_name = message.from_user.username
            user_id = message.from_user.id
            users_request[user_name] = user_id
            with open("request.json", "w", encoding='utf-8') as file:
                json.dump(users_request, file, indent=4, ensure_ascii=False)
    except:
            bot.send_message(message.chat.id, 'Вас нет в системе.')
            user_name = message.from_user.username
            user_id = message.from_user.id
            users_request[user_name] = user_id
            with open("request.json", "w", encoding='utf-8') as file:
                json.dump(users_request, file, indent=4, ensure_ascii=False)

@bot.message_handler(commands=['menu'])
def start(message):
    try:
        if valid_user('admin.json', message.from_user.id):
            bot.send_message(message.chat.id, 'Выбери команду!', reply_markup=markup_admin)
        elif valid_user('all_users.json', message.from_user.id):
            bot.send_message(message.chat.id, 'Выбери команду!', reply_markup=markup_user)
        else:
            bot.send_message(message.chat.id, 'Вас нет в системе.')
    except:
            bot.send_message(message.chat.id, 'Вас нет в системе.')

@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    # print(message)
    if valid_user('all_users.json', message.from_user.id):
        for file in os.listdir('C:\Bot_wialon\wialon\Report\\'):
            os.remove(os.path.join('C:\Bot_wialon\wialon\Report\\', file))
        try:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = 'C:\Bot_wialon\wialon\Report/' + message.document.file_name;
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Это может занять какое-то время...")
        except Exception as e:
            bot.reply_to(message, e)
        # try:
        rezult = 'No company'
        if message.caption != None:
            rezult = get_report(message.caption, message.document.file_name)
            if rezult != 'bad company':
                file = open('C:\Bot_wialon\wialon\Report/' + message.document.file_name, 'rb')
                bot.send_document(message.chat.id, file)
        bot.send_message(message.chat.id, str(rezult))
        # except Exception as e:
        #     print(e)
        #     print("TYT")
    else:
        bot.send_message(message.chat.id, 'Вас нет в системе.')
    # os.remove('C:\Bot_wialon\wialon\Report/' + message.document.file_name)
    # filling_file_name = filling_file(f'C:\_wialon\wialo/{message.document.file_name}')
    # file = open(filling_file_name, 'rb')
    # bot.send_document(message.chat.id, file)

@bot.message_handler(commands=['Добавить'])
def empty_report(message):
    if valid_user('admin.json', message.from_user.id):
        bot.send_message(message.chat.id, 'Ведите ник пользователя')
        bot.register_next_step_handler(message, add_user)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')

def add_user(message):
    users_all = {}
    with open("request.json", "r", encoding='utf-8') as file:
        result = json.load(file)
        for el in result:
            if el == message.text:
                users_all[message.text] = result[message.text]
    if users_all != {}:
        with open("request.json", "w", encoding='utf-8') as file:
            result.pop(message.text)
            json.dump(result, file, indent=4, ensure_ascii=False)
        with open("all_users.json", "r", encoding='utf-8') as file:
            data = file.read()
            if data:
                result = json.loads(data)
                for user in result:
                    users_all[user] = result[user]
        with open("all_users.json", "w", encoding='utf-8') as file:
            json.dump(users_all, file, indent=4, ensure_ascii=False)
        bot.send_message(message.chat.id, 'Пользователь успешно добавлен!')
    else:
        bot.send_message(message.chat.id, f'Пользователь {message.text} не был добавлен!')


@bot.message_handler(commands=['Удалить'])
def empty_report(message):
    if valid_user('admin.json', message.from_user.id):
        bot.send_message(message.chat.id, 'Ведите ник пользователя')
        bot.register_next_step_handler(message, delete_user)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')

def delete_user(message):
    with open("all_users.json", "r", encoding='utf-8') as file:
        data = file.read()
        if data:
            result = json.loads(data)
    if result:
        for el in result:
            if el == message.text:
                result.pop(message.text)
                break
        with open("all_users.json", "w", encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)
            bot.send_message(message.chat.id, 'Пользователь был успешно удален!')
    else:
        bot.send_message(message.chat.id, f'Пользователь {message.text} не найден!')


@bot.message_handler(commands=['Все'])
def empty_report(message):
    all_users = ''
    result = ''
    if valid_user('admin.json', message.from_user.id):
        with open("all_users.json", "r", encoding='utf-8') as file:
            data = file.read()
            if data:
                print(data)
                result = json.loads(data)
        if result != '':
            for key in result.keys():
                all_users += f'\n{key}'
            bot.send_message(message.chat.id, all_users)
        else:
            bot.send_message(message.chat.id, 'Нет пользователей')
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')
@bot.message_handler(commands=['Новый'])
def empty_report(message):
    if valid_user('admin.json', message.from_user.id):
        bot.send_message(message.chat.id, 'Введите ник админа')
        bot.register_next_step_handler(message, add_admin)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')
def add_admin(message):
    users_all = {}
    with open("all_users.json", "r", encoding='utf-8') as file:
        result = json.load(file)
        for el in result:
            if el == message.text:
                users_all[message.text] = result[message.text]
    if users_all != {}:
        with open("admin.json", "r", encoding='utf-8') as file:
            data = file.read()
            if data:
                result = json.loads(data)
                for user in result:
                    users_all[user] = result[user]
        with open("admin.json", "w", encoding='utf-8') as file:
            json.dump(users_all, file, indent=4, ensure_ascii=False)
            bot.send_message(message.chat.id, 'Админ был успешно добавлен!')
    else:
        bot.send_message(message.chat.id, 'Админ не был добавлен!')

# @bot.message_handler(commands=['Сайты'])
# def empty_report(message):
#     password = ''
#     with open("password.json", "r", encoding='utf-8') as file:
#         result = json.load(file)
#     for key in result.keys():
#         password += f'{key}: {result[key]}\n'
#     bot.send_message(message.chat.id, password)

@bot.message_handler(commands=['Изменить'])
def name_company(message):
    if valid_user('admin.json', message.from_user.id):
        bot.send_message(message.chat.id, 'Введите название сайта для которого хотите поменять токен!')
        bot.register_next_step_handler(message, password_company)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')

def password_company(message):
    name = message.text.lower()
    bot.send_message(message.chat.id, f'Введите токен для {name}!')
    bot.register_next_step_handler(message, changing_password, name)

def changing_password(message, name):
    result = ''
    with open('token_wialon.py', 'r', encoding='utf-8') as file:
        f = 0
        for line in file:
            if f == 0:
                result += line
            elif f == 1:
                result += f"     'token': '{message.text}',\n"
                bot.send_message(message.chat.id, f'Токен для {name} успешно обновлен!')
                f = 0
                line = ''
            if line.find(name) != -1:
                f = 1
    if result.find(message.text) == -1:
        bot.send_message(message.chat.id, 'Токен не был добавлен т.к. данная комания была не найдена!')
    if result != '':
        with open('token_wialon.py', 'w', encoding='utf-8') as file:
            file.write(result)
    # for el in info:
    #     if el['name'] == name.lower():
    #         el['token'] = message.text
    #         bot.send_message(message.chat.id, f'Токен для {name} успешно обновлен!')
    #         print(info)
    #         return 0
    # bot.send_message(message.chat.id, 'Токен не был добавлен т.к. данная комания была не найдена!')
    # with open("token_wialon.py", "r", encoding='utf-8') as file:
    #     result = json.load(file)
    # for company in result.keys():
    #     if company == name:
    #         result[name] = message.text
    #         with open("password.json", "w", encoding='utf-8') as file:
    #             json.dump(result, file, indent=4, ensure_ascii=False)
            # return 0



@bot.message_handler(commands=['Запросы'])
def empty_report(message):
    if valid_user('admin.json', message.from_user.id):
        request_users = {}
        with open("request.json", "r", encoding='utf-8') as file:
            data = file.read()
            if data:
                result = json.loads(data)
                if result != {}:
                    for key in result.keys():
                        request_users += f'\n{key}'
                    bot.send_message(message.chat.id, request_users)
            if not data or result == {}:
                bot.send_message(message.chat.id, 'Список запросов пуст!')
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')

@bot.message_handler(commands=['Пустой'])
def empty_report(message):
    if valid_user('all_users.json', message.from_user.id):
        file = open('Пустой отчет.xlsx', 'rb')
        bot.send_document(message.chat.id, file)
    else:
        bot.send_message(message.chat.id, 'У вас нет доступа к данной команде!')



bot.polling(none_stop=True, timeout=1000)
