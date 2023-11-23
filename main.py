import telebot
from telebot import types

from User import User
from Users import Users

print('Type bot token: ')
bot = telebot.TeleBot(input())

users = Users([])
current_user = User(0)


@bot.message_handler(commands=['start'])
def start(message):
    user = User(message.chat.id)
    if len(user.recognized_photos) > 0:
        send_button('Press "Select photos" to start', ['Add photos', 'Send new photos', 'Choose language'], message.chat.id)
    else:
        send_buttons('Press "Select photos" to start', ['Select photos', 'Choose language'], message.chat.id)

    if users.get_user(user.chat_id) is not None:
        return None

    users.add_user(user)


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global current_user
    current_user = users.get_user(message.chat.id)

    if current_user.is_sending is True:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        if downloaded_file not in current_user.photos:
            current_user.photos.append(downloaded_file)


@bot.message_handler()
def get_message(message):
    global current_user
    current_user = users.get_user(message.chat.id)
    if current_user is None:
        return None

    if current_user.setting_language is True:
        current_user.model_init(message.text)
        current_user.setting_language = False
        send_message('Language set', chat_id=message.chat.id)
        start(message)

    if message.text == 'Choose language':
        send_message('Input needed language. \nFormatting: ru, en, ua.. etc.', chat_id=message.chat.id)
        current_user.setting_language = True

    if message.text == 'Select photos':
        send_button('Send photos to this chat', 'Stop sending', message.chat.id)
        current_user.is_sending = True
        return None

    if message.text == 'Stop sending':
        current_user.is_sending = False

        send_message('Starting preparations', message.chat.id)
        if current_user.reader is None:
            current_user.model_init()

        current_user.recognize()
        send_message('Recognizing completed', message.chat.id)
        send_buttons('Type text for searching...', ['Send new photos', 'Add photos'], message.chat.id)
        return None

    if message.text == 'Send new photos':
        current_user.photos.clear()
        send_button('Send photos to this chat', 'Stop sending', message.chat.id)
        current_user.is_sending = True
        return None

    if message.text == 'Add photos':
        send_button('Send photos to this chat', 'Stop sending', message.chat.id)
        current_user.is_sending = True
        return None

    if len(current_user.recognized_photos) > 0:
        photos = current_user.get_photos(message.text)
        media = []
        for photo in photos:
            media.append(telebot.types.InputMediaPhoto(photo))

        if len(media) > 0:
            bot.send_media_group(message.chat.id, media)
        else:
            send_message("Photos not found", message.chat.id)


def send_message(text, chat_id):
    bot.send_message(chat_id, text=text)


def send_buttons(text, buttons, chat_id):
    buttons_list = []
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in buttons:
        buttons_list.append(types.KeyboardButton(i))
        markup.add(buttons_list[-1])

    bot.send_message(chat_id, text=text, reply_markup=markup)


def send_button(text, button, chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    parse = types.KeyboardButton(button)
    markup.add(parse)

    bot.send_message(chat_id, text=text, reply_markup=markup)


bot.polling(none_stop=True)
