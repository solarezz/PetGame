import telebot
from telebot import types
import database as db

API_TOKEN = '7006081046:AAFPbndJeFGBR4_tTQXHcItRZ0F4NJ4PsJw'

bot = telebot.TeleBot(API_TOKEN)



id = [0]
username = ['0']

@bot.message_handler(commands=['help', 'start'])
def welcome_message(message):
    message_ =  f'╭────────»»❀❀❀««────────╮\n'\
                f'      Привет, {message.from_user.first_name} \n'\
                f'      Бот был создан для: \n'\
                f'      @solarezzov и @solarezzova\n'\
                f'\n'\
                f'      Разработчик: @solarezzov \n'\
                f'╰────────»»❀❀❀««────────╯'
    markup = types.InlineKeyboardMarkup()
    button_profile = types.InlineKeyboardButton('📋 Профиль', callback_data='profile')
    button_partner = types.InlineKeyboardButton('👩🏻‍❤️‍👨🏻 Партнёр', callback_data='partner')
    button_pet = types.InlineKeyboardButton('🐾 Питомец', callback_data='pet')
    markup.row(button_profile, button_pet, button_partner)
    bot.reply_to(message, message_, reply_markup=markup)
    try:
        db.table_input(user_id=message.chat.id, username=message.from_user.username)
    except:
        pass

    
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == 'profile':
        profile_function(call.message)
    elif call.data == 'partner':
        if db.info(call.message.chat.id)[3] != None:
            bot.send_message(call.message.chat.id, f"Информация по партнёру:\nВаш партнёр: {db.info(call.message.chat.id)[3]} ")
        else:
            bot.send_message(call.message.chat.id, "⌨️ Введите [ID] пользователя(его можно узнать в профиле): ")
    elif call.data == 'yes_partner':
        profile_partner(call.message)
    elif call.data == 'no_partner':
        bot.send_message(call.message.chat.id, '🚫 Вам отказали в партнерстве')
        db.request_partner_id(0, call.message.chat.id)
     
@bot.message_handler(func=lambda message: db.info(message.chat.id)[4] == 0)
def handle_id_input(message):
    markup = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton('✔️ Да', callback_data='yes_partner')
    button_no = types.InlineKeyboardButton('❌ Нет', callback_data='no_partner')
    markup.row(button_yes, button_no)
    part = message.text
    id[0] = message.chat.id
    username[0] = message.from_user.username
    db.request_partner_id(part, message.chat.id)
    try:
        if part != db.info(message.chat.id)[0]:
            bot.send_message(part, "📨 Вам отправили запрос на партнерство", reply_markup=markup)
        else:
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="❌ Вы не можете отправлять запрос себе!")
    except:
        bot.reply_to(message, "⚠️ id не найден")

def profile_partner(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text= "🤝🏻 Вы теперь партнеры")
    bot.send_message(id[0], "🤝🏻 Вы теперь партнеры")
                     #user_id,   partner_name, partner_id
    db.partner_update(message.chat.id, username[0], id[0])
    db.partner_update(id[0], db.info(message.chat.id)[1], db.info(message.chat.id)[0])
    db.request_partner_id(0, id[0])

def profile_function(message):
    try:
        health_status = "Отлично себя чувствует" if {db.info_pet(message.from_user.username)[4]} > 70 else "Плохо" if db.info_pet(message.from_user.username)[4] <= 30 else "Нормально"
        eat_status = "Не голоден" if db.info_pet(message.from_user.username)[5] == 100 else "Голоден" if db.info_pet(message.from_user.username)[5] <= 30 else "Нормально"
        water_status = "Не хочет пить" if db.info_pet(message.from_user.username)[6] == 100 else "Хочет пить" if db.info_pet(message.from_user.username)[6] <= 30 else "Нормально"
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=
'╭────»»❀❀❀»»\n'\
f'| 📋 Ваш профиль:\n'\
f'| 👤 Имя - {db.info(message.chat.id)[1]}\n'\
f'| 👩🏻‍❤️‍👨🏻 Партнер - {db.info(message.chat.id)[2]}\n'\
'|───────────────\n'\
'| 📌 Информация по питомцу:\n'\
f'| 🐾 Имя питомца - {db.info_pet(message.from_user.username)[3]}\n'\
f'| 🌍 Месторасположение - {db.info_pet(message.from_user.username)[1]}\n'\
f'| 🩺 Здоровье -  {health_status}\n'\
f'| 🍽️ Еда - {eat_status}\n'\
f'| 💦 Вода - {water_status}\n'\
'╰────»»❀❀❀»»')
    except:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=
'╭────»»❀❀❀»»\n'\
f'| 📋 Ваш профиль:\n'\
f'| 👤 Имя - {db.info(message.chat.id)[1]}\n'\
f'| 👩🏻‍❤️‍👨🏻 Партнер - {db.info(message.chat.id)[2]}\n'\
'╰────»»❀❀❀»»')
        
bot.infinity_polling()
print("bot started")
