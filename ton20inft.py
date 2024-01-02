import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

TOKEN = '6692695290:AAFR1My0f132RkbwYxGzyceP8Tjt7ezEaQI'
bot = telebot.TeleBot(TOKEN)

# Проверка записи пользователя в txt документе
def is_user_logged(user_id):
    with open('user_log.txt', 'r') as log_file:
        for line in log_file:
            if f"ID: {user_id}" in line:
                return True
    return False

# Меню

@bot.message_handler(commands=['start'])
def handle_start(message):
    # Extract user information
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    username = message.from_user.username

    # Запись в txt данные пользователя, если его не было там ранее
    if not is_user_logged(user_id):
        with open('user_log.txt', 'a') as log_file:
            log_file.write(f"ID: {user_id}, Name: {user_name}, Username: {username}\n")

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('🌀 Что такое TON-20?', url="https://telegra.ph/TON-20-Prostoe-Opisanie-dlya-Dokumentacii-12-25")
    btn2 = types.InlineKeyboardButton('⚒ Минт токена «inft» TON-20', url="https://tonano.io/ton20/inft")
    btn3 = types.InlineKeyboardButton('💰 Продать токены «inft» TON-20', url='https://ton20.market/orders/inft')
    btn4 = types.InlineKeyboardButton('🏆 Конкурс', callback_data='contest')
    btn5 = types.InlineKeyboardButton('📣 Медиа-ресурсы', callback_data='media')

    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    keyboard.add(btn5)

    with open('ton20logo.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo,
                       caption=f"Привет, {message.from_user.first_name}! Выбери опцию ниже:",
                       reply_markup=keyboard)

# Обработчики кнопок

@bot.callback_query_handler(func=lambda call: True)
def handle_inline(call):
    if call.message:
        chat_id = call.message.chat.id

        if call.data == 'contest':
            send_contest_menu(chat_id, call.message.message_id)

        elif call.data == 'media':
            send_media_menu(chat_id, call.message.message_id)

        elif call.data == 'back':
            send_main_menu(chat_id, call.message.message_id)
        else:
            bot.answer_callback_query(call.id, text='🛠 В Разработке...')

# Конкурс
def send_contest_menu(chat_id, message_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    back_button = types.InlineKeyboardButton(text="◀️ Назад", callback_data='back')
    keyboard.add(back_button)

    bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                             caption='⭐️ Конкурс на токены $INFT! ⭐️\n\nРады объявить о запуске увлекательного конкурса, который призван порадовать вас. Чтобы принять участие в конкурсе вам нужно сминтить от 100 токенов "inft" TON-20. В конкурсе участвуют автоматически кошельки, держащие не менее 100 токенов "inft" TON-20. Среди держателей этих уникальных токенов будет роздано 2.5 $INFT, каждый из 20 победителей получит 0.125 $INFT (0.08 TON). Победители будут выбираться случайным образом. Итоги будут подведены 1 января! Это событие станет настоящим подарком для наших активных участников, поэтому не упустите свой шанс! Участвуйте, выигрывайте и наслаждайтесь приятными моментами в мире криптовалюты. Благодарим за ваш интерес и желаем удачи!',
                             reply_markup=keyboard)

# Главное меню
def send_main_menu(chat_id, message_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('🌀 Что такое TON-20?',
                                      url="https://telegra.ph/TON-20-Prostoe-Opisanie-dlya-Dokumentacii-12-25")
    btn2 = types.InlineKeyboardButton('⚒ Минт токена «inft» TON-20', url="https://tonano.io/ton20/inft")
    btn3 = types.InlineKeyboardButton('💰 Продать токены «inft» TON-20', url='https://ton20.market/orders/inft')
    btn4 = types.InlineKeyboardButton('🏆 Конкурс', callback_data='contest')
    btn5 = types.InlineKeyboardButton('📣 Медиа-ресурсы', callback_data='media')

    keyboard.add(btn1)
    keyboard.add(btn2)
    keyboard.add(btn3)
    keyboard.add(btn4)
    keyboard.add(btn5)

    with open('ton20logo.jpg', 'rb') as photo:
        bot.edit_message_media(media=types.InputMediaPhoto(media=photo),
                               chat_id=chat_id,
                               message_id=message_id,
                               reply_markup=keyboard)

# Медиа
def send_media_menu(chat_id, message_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    subscribe_button = types.InlineKeyboardButton(text="📢 Infinity | Community",
                                                  url="https://t.me/TokenInfinity")
    chat_button = types.InlineKeyboardButton(text="👥 Infinity | Chat", url="https://t.me/TokenInfinityChat")
    bote_button = types.InlineKeyboardButton(text="🤖 Infinity | Bot", url="https://t.me/InfinityTokenBot")
    staking_button = types.InlineKeyboardButton(text="💰 Infinity | Staking", callback_data='stake')
    airdrop_button = types.InlineKeyboardButton(text="🎁 Infinity | Airdrop",
                                                url="https://telegra.ph/Infinity--Airdrop-12-23")
    ton20_button = types.InlineKeyboardButton(text="🎯 Infinity | Clicker",
                                              url="https://t.me/InfinityClickerBot")
    buy_button = types.InlineKeyboardButton(text="🟡 $INFT | DeDust.io",
                                            url="https://dedust.io/swap/EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c/EQDzCNIjlBhSHAWuNwga2mCPuNMEObaedJWSL_GSfzeNzY1B")
    buy1_button = types.InlineKeyboardButton(text="⚫️ $INFT | EXTON",
                                             url="https://t.me/EXTON_SWAP_BOT")
    back_button = types.InlineKeyboardButton(text="◀️ Назад", callback_data='back')

    keyboard.add(subscribe_button, chat_button)
    keyboard.add(bote_button, airdrop_button)
    keyboard.add(ton20_button, staking_button)
    keyboard.add(buy_button, buy1_button)
    keyboard.add(back_button)

    with open('ton20logo.jpg', 'rb') as photo:
        bot.edit_message_caption(caption=f"🛎 Выберите медиа-ресурсы из нашего ассортимента:",
                                 chat_id=chat_id,
                                 message_id=message_id,
                                 reply_markup=keyboard)

if __name__ == "__main__":
    bot.polling(none_stop=True)

