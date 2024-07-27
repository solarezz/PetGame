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

@bot.message_handler(func=lambda message: db.info(message.chat.id)[3] != "None")
def handle_petname_input(message):
    try:
        if db.info_pet(db.info(message.chat.id)[1])[3] != "Питомец не выбран" and db.info_pet(db.info(message.chat.id)[1])[4] == "Имя питомцу не назначено":
            db.update_petname(message.from_user.username, message.text)
            bot.send_message(message.chat.id, f'❤️ Вы присвоили питомцу имя - "{db.info_pet(message.from_user.username)[4]}"')
            bot.send_message(db.info(message.chat.id)[3], f'❤️ Партнёр присвоил имя питомцу - "{db.info_pet(message.from_user.username)[4]}"')
    except TypeError:
        bot.send_message(message.chat.id, "✔️ Имя должен писать Ваш партнёр: ")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    bot.answer_callback_query(call.id)
    if call.data == 'profile':
        profile_function(call.message)
    elif call.data == 'partner':
        if db.info(call.message.chat.id)[3] != "None":
            markup = types.InlineKeyboardMarkup()
            button_partner = types.InlineKeyboardButton('💔 Расстаться', callback_data='breake')
            button_pet = types.InlineKeyboardButton('🐾 Наш питомец', callback_data='pet')
            markup.row(button_partner, button_pet)
            bot.send_message(call.message.chat.id, f"📌 Информация по партнёру:\n❤️ Ваш партнёр: @{db.info(call.message.chat.id)[2]}", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id, "⌨️ Введите [ID] пользователя(его можно узнать в профиле): ")
    elif call.data == 'breake':
        bot.send_message(call.message.chat.id, "💔 Вы расстались с партнёром.")
        bot.send_message(db.info(call.message.chat.id)[3], "💔 Ваш партнёр решил расстаться.")
        #user_id: int, partner_name: str, partner_id: int
        db.partner_update(db.info(call.message.chat.id)[3], "Партнёра нет", "None")
        db.partner_update(call.message.chat.id, "Партнёра нет", "None")
        db.delete_pet(db.info(call.message.chat.id)[1])
    elif call.data == 'pet':
        try:
            if db.info(call.message.chat.id)[3] == "None":
                bot.send_message(call.message.chat.id, "❌ У вас нет партнёра!")
            elif db.info_pet(db.info(call.message.chat.id)[1])[3] != "Питомец не выбран":
                health_status = "Отлично себя чувствует" if db.info_pet(db.info(call.message.chat.id)[1])[5] > 70 else "Плохо" if \
                db.info_pet(db.info(call.message.chat.id)[1])[5] <= 30 else "Нормально"
                eat_status = "Не голоден" if db.info_pet(db.info(call.message.chat.id)[1])[6] == 100 else "Голоден" if \
                db.info_pet(db.info(call.message.chat.id)[1])[6] <= 30 else "Нормально"
                water_status = "Не хочет пить" if db.info_pet(db.info(call.message.chat.id)[1])[7] == 100 else "Хочет пить" if \
                db.info_pet(db.info(call.message.chat.id)[1])[7] <= 30 else "Нормально"
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=
                '╭────»»❀❀❀»»\n'\
                '| 📌 Информация по питомцу:\n' \
                f'| 🐾 Питомец - {db.info_pet(db.info(call.message.chat.id)[1])[3]}\n' \
                f'| 📸 Имя питомца - {db.info_pet(db.info(call.message.chat.id)[1])[4]}\n' \
                f'| 🌍 Месторасположение - {db.info_pet(db.info(call.message.chat.id)[1])[2]}\n' \
                f'| 🩺 Здоровье -  {health_status}\n' \
                f'| 🍽️ Еда - {eat_status}\n' \
                f'| 💦 Вода - {water_status}\n' \
                '╰────»»❀❀❀»»')
            else:
                choice_pet(call.message)
        except TypeError:
            choice_pet(call.message)
    elif call.data == 'yes_partner':
        profile_partner(call.message)
    elif call.data == 'no_partner':
        bot.send_message(call.message.chat.id, '🚫 Вам отказали в партнерстве')
        db.request_partner_id(0, call.message.chat.id)
    elif call.data == 'dog':
        markup = types.InlineKeyboardMarkup()
        button_yesdog = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesdog')
        button_nodog = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesdog, button_nodog)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(db.info(call.message.chat.id)[3], '⚠️ Ваш партнёр выбрал питомца "🐶 Собака". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'cat':
        markup = types.InlineKeyboardMarkup()
        button_yescat = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yescat')
        button_nocat = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yescat, button_nocat)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(db.info(call.message.chat.id)[3], '⚠️ Ваш партнёр выбрал питомца "🐱 Кот". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'squirrel':
        markup = types.InlineKeyboardMarkup()
        button_yesbelka = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesbelka')
        button_nobelka = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesbelka, button_nobelka)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(db.info(call.message.chat.id)[3], '⚠️ Ваш партнёр выбрал питомца "🐿️ Белка". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'hamster':
        markup = types.InlineKeyboardMarkup()
        button_yeshamster = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yeshamster')
        button_nohamster = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yeshamster, button_nohamster)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(db.info(call.message.chat.id)[3], '⚠️ Ваш партнёр выбрал питомца "🐹 Хомяк". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'turtle':
        markup = types.InlineKeyboardMarkup()
        button_yesturtle = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesturtle')
        button_noturtle = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesturtle, button_noturtle)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(db.info(call.message.chat.id)[3], '⚠️ Ваш партнёр выбрал питомца "🐢 Черепаха". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'parrot':
        markup = types.InlineKeyboardMarkup()
        button_yesparrot = types.InlineKeyboardButton('✔️ Одобряю', callback_data='yesparrot')
        button_noparrot = types.InlineKeyboardButton('❌ Не одобряю', callback_data='notapprove')
        markup.row(button_yesparrot, button_noparrot)
        bot.send_message(call.message.chat.id, '⚠️ Ваш партнёр должен одобрить Ваш выбор. Ожидаем одобрения...')
        bot.send_message(db.info(call.message.chat.id)[3], '⚠️ Ваш партнёр выбрал питомца "🦜 Попугай". Нажмите на кнопку в связи с вашим решением.', reply_markup=markup)
    elif call.data == 'yesdog':
        db.pet_update(owner1=db.info(call.message.chat.id)[1], owner2=db.info(call.message.chat.id)[2], pet="🐶 Собака")
        bot.send_message(db.info(call.message.chat.id)[3], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.\n\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
    elif call.data == 'yescat':
        db.pet_update(owner1=db.info(call.message.chat.id)[1], owner2=db.info(call.message.chat.id)[2], pet="🐱 Кот")
        bot.send_message(db.info(call.message.chat.id)[3], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.\n\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
    elif call.data == 'yesbelka':
        db.pet_update(owner1=db.info(call.message.chat.id)[1], owner2=db.info(call.message.chat.id)[2], pet="🐿️ Белка")
        bot.send_message(db.info(call.message.chat.id)[3], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.\n\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
    elif call.data == 'yeshamster':
        db.pet_update(owner1=db.info(call.message.chat.id)[1], owner2=db.info(call.message.chat.id)[2], pet="🐹 Хомяк")
        bot.send_message(db.info(call.message.chat.id)[3], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.\n\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
    elif call.data == 'yesturtle':
        db.pet_update(owner1=db.info(call.message.chat.id)[1], owner2=db.info(call.message.chat.id)[2], pet="🐢 Черепаха")
        bot.send_message(db.info(call.message.chat.id)[3], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.\n\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
    elif call.data == 'yesparrot':
        db.pet_update(owner1=db.info(call.message.chat.id)[1], owner2=db.info(call.message.chat.id)[2], pet="🦜 Попугай")
        bot.send_message(db.info(call.message.chat.id)[3], f'👩🏻‍❤️‍👨🏻 Партнёр одобрил Ваш выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.')
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text=f'👩🏻‍❤️‍👨🏻 Вы одобрили выбор. Теперь у вас есть питомец {db.info_pet(db.info(call.message.chat.id)[1])[3]}.\n\nТеперь напишите имя питомца, перед тем как написать обязательно хорошо посоветуйтесь с партнёром! Имя:')
    elif call.data == 'notapprove':
        bot.send_message(db.info(call.message.chat.id)[3], "❌ Ваш партнёр не одобрил Ваш выбор.")
    
def choice_pet(message):
    markup = types.InlineKeyboardMarkup()
    button_dog = types.InlineKeyboardButton('🐶 Собака', callback_data='dog')
    button_cat = types.InlineKeyboardButton('🐱 Кот', callback_data='cat')
    button_squirrel = types.InlineKeyboardButton('🐿️ Белка', callback_data='squirrel')
    button_hamster = types.InlineKeyboardButton('🐹 Хомяк', callback_data='hamster')
    button_turtle = types.InlineKeyboardButton('🐢 Черепаха', callback_data='turtle')
    button_parrot = types.InlineKeyboardButton('🦜 Попугай', callback_data='parrot')
    markup.add(button_dog, button_cat, button_squirrel)
    markup.add(button_hamster, button_turtle, button_parrot)
    bot.send_message(message.chat.id, "Выберите питомца: ", reply_markup=markup)

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
        db.request_partner_id(0, id[0])

def profile_partner(message):
    bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text= "🤝🏻 Вы теперь партнеры")
    bot.send_message(id[0], "🤝🏻 Вы теперь партнеры")
                     #user_id,   partner_name, partner_id
    db.partner_update(message.chat.id, username[0], id[0])
    db.partner_update(id[0], db.info(message.chat.id)[1], db.info(message.chat.id)[0])
    db.request_partner_id(0, id[0])

def profile_function(message):
    try:
        health_status = "Отлично себя чувствует" if db.info_pet(db.info(message.chat.id)[1])[5] > 70 else "Плохо" if db.info_pet(db.info(message.chat.id)[1])[5] <= 30 else "Нормально"
        eat_status = "Не голоден" if db.info_pet(db.info(message.chat.id)[1])[6] == 100 else "Голоден" if db.info_pet(db.info(message.chat.id)[1])[6] <= 30 else "Нормально"
        water_status = "Не хочет пить" if db.info_pet(db.info(message.chat.id)[1])[7] == 100 else "Хочет пить" if db.info_pet(db.info(message.chat.id)[1])[7] <= 30 else "Нормально"
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=
'╭────»»❀❀❀»»\n'\
f'| 📋 Ваш профиль:\n'\
f'| 👤 Имя - @{db.info(message.chat.id)[1]}\n'\
f'| 🆔 Айди - {db.info(message.chat.id)[0]} \n'\
f'| 👩🏻‍❤️‍👨🏻 Партнер - @{db.info(message.chat.id)[2]}\n'\
'|───────────────\n'\
'| 📌 Информация по питомцу:\n'\
f'| 🐾 Питомец - {db.info_pet(db.info(message.chat.id)[1])[3]}\n'\
f'| 📸 Имя питомца - {db.info_pet(db.info(message.chat.id)[1])[4]}\n'\
f'| 🌍 Месторасположение - {db.info_pet(db.info(message.chat.id)[1])[2]}\n'\
f'| 🩺 Здоровье -  {health_status}\n'\
f'| 🍽️ Еда - {eat_status}\n'\
f'| 💦 Вода - {water_status}\n'\
'╰────»»❀❀❀»»')
    except:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=
'╭────»»❀❀❀»»\n'\
f'| 📋 Ваш профиль:\n'\
f'| 👤 Имя - @{db.info(message.chat.id)[1]}\n'\
f'| 🆔 Айди - {db.info(message.chat.id)[0]} \n'\
f'| 👩🏻‍❤️‍👨🏻 Партнер - {db.info(message.chat.id)[2]}\n'\
'╰────»»❀❀❀»»')

print("bot started")
bot.infinity_polling()
