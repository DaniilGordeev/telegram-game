import telebot
from telebot import types
from config import token, admins
from database import Database
import keyboard_mine as kb_mine
import keyboard as kb
import function as func
import time
import schedule
import threading


bot = telebot.TeleBot(token)

def payday():
    text = f'PayDay\n'\
            f'+1 XP\n'\
            f'+5000$'
    db = Database(admins[0], bot)
    users = db.check_payday()
    for user in users:
        bot.send_message(user.get('id'), text)
        db.update_data_payday(user.get('id'))

schedule.every().hour.at(':00').do(payday)

@bot.message_handler(regexp='Тест')
def test(message):
    payday()

@bot.message_handler(regexp='start')
def start(message):
    user_id = message.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if db.check_users(user_id) == True:
        text = f'Привет, давай познакомимся с тобой?\n'\
                f'Как тебя звать?'
        name = bot.send_message(user_id, text)
        bot.register_next_step_handler(name, get_name)
    else:
        text = f'Привет, {user['name']}\n\n'\
                f'Твоя статистика:\n'\
                f'{user['money']} Рублей\n'\
                f'{user['lvl']} уровень'
        bot.send_message(user_id, text, reply_markup=kb.menu_kb)

def get_name(message):
    user_id = message.from_user.id
    db = Database(user_id, bot)
    while(True):
        name = message.text
        if db.check_name_users(name) == None:
            text = f'Приятно познакомится, {name} !\n'\
                    f'Советую посмотреть тебе раздел работы.'
            bot.send_message(user_id, text, reply_markup=kb.menu_kb)
            db.get_user(user_id, name)
            return
        else:
            bot.send_message(user_id, 'Данное имя уже занято!')
            start(message)
            return

@bot.message_handler(regexp='Работа')
def job(message):
    user_id = message.from_user.id
    text = f'Выбери на какую работу ты пойдешь?'
    bot.send_message(user_id, text, reply_markup=kb.job_kb)


# Шахта 
@bot.callback_query_handler(lambda call: call.data == 'mine')
def mine(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    if db.check_mine(user_id) == True:
        db.init_mine(user_id)
    user_mine = db.get_me_mine(user_id)
    text = f'Ты на шахте!\n\n'\
            f'У тебя есть: \n'\
            f'Камень: {user_mine['stone']} \n'\
            f'Металл: {user_mine['metall']} \n'\
            f'Серебро: {user_mine['silver']} \n'\
            f'Золото: {user_mine['gold']}'
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.mine_kb)

@bot.callback_query_handler(lambda call: call.data == 'mine_start')
def mine_start(call, text='Давай'):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    if user['mining_hour'] != user['max_amount_ore']:
        mining_kb = types.InlineKeyboardMarkup(row_width=3)
        for i in range(3):
            mining_kb.add(
                types.InlineKeyboardButton('?', callback_data=func.random_ore()),
                types.InlineKeyboardButton('?', callback_data=func.random_ore()),
                types.InlineKeyboardButton('?', callback_data=func.random_ore())
            )
        mining_kb.add(types.InlineKeyboardButton('Назад', callback_data='back_mine'))
        bot.send_message(user_id, text, reply_markup=mining_kb)
    else:
        bot.send_message(user_id, 'У тебя кончился объём на этот час!', reply_markup=kb.back_mine_kb)

@bot.callback_query_handler(lambda call: call.data == 'add_stone')
def add_stone(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.add_stone(user_id)
    bot.delete_message(user_id, call.message.message_id)
    mine_start(call, 'Ты добыл камень')

@bot.callback_query_handler(lambda call: call.data == 'add_metall')
def add_metall(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.add_metall(user_id)
    bot.delete_message(user_id, call.message.message_id)
    mine_start(call, 'Ты добыл металл')

@bot.callback_query_handler(lambda call: call.data == 'add_silver')
def add_silver(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.add_silver(user_id)
    bot.delete_message(user_id, call.message.message_id)
    mine_start(call, 'Ты добыл серебро')

@bot.callback_query_handler(lambda call: call.data == 'add_gold')
def add_gold(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.add_gold(user_id)
    bot.delete_message(user_id, call.message.message_id)
    mine_start(call, 'Ты добыл золото')

@bot.callback_query_handler(lambda call: call.data == 'mine_upgrade')
def mine_shop(call):
    user_id = call.from_user.id
    text = f'Ты в улучшениях шахтера: \n'
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.mine_upgrade_kb)


# Улучшение скоррости 
@bot.callback_query_handler(lambda call: call.data == 'speed_mining')
def speed_mining(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    text = f'Твоя скорость копания: {user['speed_mining']}\n'\
            f'Чтобы улучшить кирку, необходимо: \n'\

    if user['speed_mining'] == 1:
        text += f'10000 денег'
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.speed_mining_kb_1)
    elif user['speed_mining'] == 2:
        text += f'50000 денег'
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.speed_mining_kb_2)
    elif user['speed_mining'] == 3:
        text += f'100000 денег'
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.speed_mining_kb_3)
    elif user['speed_mining'] == 4:
        text += f'250000 денег'
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.speed_mining_kb_4)
    elif user['speed_mining'] == 5:
        text += f'500000 денег'
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.speed_mining_kb_5)
    else:
        text = f'Твоя скорость копания: {user['speed_mining']}\n'\
                f'У тебя максимальный уровень скорости '
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.speed_mining_kb_end)


@bot.callback_query_handler(lambda call: call.data == 'upgrade_speed_mining_1')
def upgrade_speed_mining_1(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] < 10000:
        text = 'Тебе не хватает на данное улучшение.'
    else:
        text = 'Ты успешно улучшил свою кирку!'
        db.upgrade_speed(user_id, 10000)
    
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.upgrade_mine_kb)

@bot.callback_query_handler(lambda call: call.data == 'upgrade_speed_mining_2')
def upgrade_speed_mining_2(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] < 50000:
        text = 'Тебе не хватает на данное улучшение.'
    else:
        text = 'Ты успешно улучшил свою кирку!'
        db.upgrade_speed(user_id, 50000)
    
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb.upgrade_mine_kb)

@bot.callback_query_handler(lambda call: call.data == 'upgrade_speed_mining_3')
def upgrade_speed_mining_3(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] < 100000:
        text = 'Тебе не хватает на данное улучшение.'
    else:
        text = 'Ты успешно улучшил свою кирку!'
        db.upgrade_speed(user_id, 100000)
    
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb.upgrade_mine_kb)

@bot.callback_query_handler(lambda call: call.data == 'upgrade_speed_mining_4')
def upgrade_speed_mining_4(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] < 250000:
        text = 'Тебе не хватает на данное улучшение.'
    else:
        text = 'Ты успешно улучшил свою кирку!'
        db.upgrade_speed(user_id, 250000)
    
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb.upgrade_mine_kb)

@bot.callback_query_handler(lambda call: call.data == 'upgrade_speed_mining_5')
def upgrade_speed_mining_5(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] < 500000:
        text = 'Тебе не хватает на данное улучшение.'
    else:
        text = 'Ты успешно улучшил свою кирку!'
        db.upgrade_speed(user_id, 500000)
    
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb.upgrade_mine_kb)

# Улучшение макс кол-ва добычи
@bot.callback_query_handler(lambda call: call.data == 'max_amount_ore_upgrade')
def max_amount_ore_upgrade(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    text = f'Максимально ты можешь добыть {user['max_amount_ore']} руд/час.\n'\
            f'Желаешь увеличить объём?'
    if user['max_amount_ore'] == 30:
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.max_amount_ore_upgrade_kb_1)
    elif user['max_amount_ore'] == 60:
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.max_amount_ore_upgrade_kb_2)
    elif user['max_amount_ore'] == 90:
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb_mine.max_amount_ore_upgrade_kb_3)
    elif user['max_amount_ore'] == 120:
        text = f'У тебя максимальный объём 120 руд/час!'
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb.back_upgrade_mine)


@bot.callback_query_handler(lambda call: call.data == 'max_amount_ore_1')
def max_amount_ore_1(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] >= 50000:
        text = f'Ты успешно увеличил объём!'
        db.max_amount_ore(user_id, 50000, 60)
    else:
        text = f'У тебя не хватает денег!'
    bot.send_message(user_id, text, reply_markup=kb.back_upgrade_mine)

@bot.callback_query_handler(lambda call: call.data == 'max_amount_ore_2')
def max_amount_ore_2(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] >= 100000:
        text = f'Ты успешно увеличил объём!'
        db.max_amount_ore(user_id, 100000, 90)
    else:
        text = f'У тебя не хватает денег!'
    bot.send_message(user_id, text, reply_markup=kb.back_upgrade_mine)
    
@bot.callback_query_handler(lambda call: call.data == 'max_amount_ore_3')
def max_amount_ore_3(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    if user['money'] >= 250000:
        text = f'Ты успешно увеличил объём!'
        db.max_amount_ore(user_id, 250000, 120)
    else:
        text = f'У тебя не хватает денег!'
    bot.send_message(user_id, text, reply_markup=kb.back_upgrade_mine)

    

# Продажа руды
@bot.callback_query_handler(lambda call: call.data == 'sell_ore')
def sell_ore(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    text = 'Выбери какую руду ты хочешь продать.'
    select_ore_kb = types.InlineKeyboardMarkup(row_width=2)
    select_ore_kb.add(
        types.InlineKeyboardButton(f'Камень {user['stone']}', callback_data='sell_stone'),
        types.InlineKeyboardButton(f'Металл {user['metall']}', callback_data='sell_metall'),
        types.InlineKeyboardButton(f'Серебро {user['silver']}', callback_data='sell_silver'),
        types.InlineKeyboardButton(f'Золото {user['gold']}', callback_data='sell_gold'),
        types.InlineKeyboardButton('Назад', callback_data='back_mine')
    )
    bot.send_message(user_id, text, reply_markup=select_ore_kb)

@bot.callback_query_handler(lambda call: call.data == 'sell_stone')
def sell_stone_select_count(call):
    user_id = call.from_user.id
    text = f'Введи количество которое хочешь продать.'
    count = bot.send_message(user_id, text, reply_markup=kb.back_sell_ore_kb)
    bot.register_next_step_handler(count, sell_stone)

def sell_stone(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    while(True):
        count = call.text
        if int(count) <= user['stone']:
            text = f'Ты успешно продал камень в количестве {count}.'
            bot.send_message(user_id, text)
            db.sell_ore(user_id, 100, count, 'stone')
            sell_ore(call)
            return
        else:
            text = f'У тебя нет столько камня!'
            bot.delete_message(user_id, call.message_id - 1)
            bot.delete_message(user_id, call.message_id - 2)
            bot.send_message(user_id, text)
            sell_stone_select_count(call)
            return
        
@bot.callback_query_handler(lambda call: call.data == 'sell_metall')
def sell_metal_select_count(call):
    user_id = call.from_user.id
    text = f'Введи количество которое хочешь продать.'
    count = bot.send_message(user_id, text, reply_markup=kb.back_sell_ore_kb)
    bot.delete_message(user_id, call.message.message_id)
    bot.register_next_step_handler(count, sell_metal)

def sell_metal(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    while(True):
        count = call.text
        if int(count) <= user['metall']:
            text = f'Ты успешно продал металл в количестве {count}.'
            bot.send_message(user_id, text)
            db.sell_ore(user_id, 250, count, 'metall')
            sell_ore(call)
            return
        else:
            text = f'У тебя нет столько металла!'
            bot.delete_message(user_id, call.message_id - 1)
            bot.delete_message(user_id, call.message_id - 2)
            bot.send_message(user_id, text)
            sell_metal_select_count(call)
            return

@bot.callback_query_handler(lambda call: call.data == 'sell_silver')
def sell_silver_select_count(call):
    user_id = call.from_user.id
    text = f'Введи количество которое хочешь продать.'
    count = bot.send_message(user_id, text, reply_markup=kb.back_sell_ore_kb)
    bot.delete_message(user_id, call.message.message_id)
    bot.register_next_step_handler(count, sell_silver)

def sell_silver(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    while(True):
        count = call.text
        if int(count) <= user['silver']:
            text = f'Ты успешно продал металл в количестве {count}.'
            bot.send_message(user_id, text)
            db.sell_ore(user_id, 500, count, 'silver')
            sell_ore(call)
            return
        else:
            text = f'У тебя нет столько металла!'
            bot.delete_message(user_id, call.message_id - 1)
            bot.delete_message(user_id, call.message_id - 2)
            bot.send_message(user_id, text)
            sell_silver_select_count(call)
            return
        
@bot.callback_query_handler(lambda call: call.data == 'sell_gold')
def sell_gold_select_count(call):
    user_id = call.from_user.id
    text = f'Введи количество которое хочешь продать.'
    count = bot.send_message(user_id, text, reply_markup=kb.back_sell_ore_kb)
    bot.delete_message(user_id, call.message.message_id)
    bot.register_next_step_handler(count, sell_gold)

def sell_gold(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    user = db.get_me_mine(user_id)
    while(True):
        count = call.text
        if int(count) <= user['gold']:
            text = f'Ты успешно продал металл в количестве {count}.'
            bot.send_message(user_id, text)
            db.sell_ore(user_id, 1000, count, 'gold')
            sell_ore(call)
            return
        else:
            text = f'У тебя нет столько металла!'
            bot.delete_message(user_id, call.message_id - 1)
            bot.delete_message(user_id, call.message_id - 2)
            bot.send_message(user_id, text)
            sell_gold_select_count(call)
            return
        
# Карта 
@bot.message_handler(regexp='Карта')
def map(message):
    user_id = message.from_user.id
    db = Database(user_id, bot)
    user = db.get_me(user_id)
    text = f'Ты в городе {user['city']}.\n'\
            f'Куда поедем?'
    if user['city'] == 'Пенза':
        bot.send_message(user_id, text, reply_markup=kb.city_for_penza)
    elif user['city'] == 'Владивосток':
        bot.send_message(user_id, text, reply_markup=kb.city_for_vladivostok)
    elif user['city'] == 'Москва':
        bot.send_message(user_id, text, reply_markup=kb.city_for_moscow)
    elif user['city'] == 'Самара':
        bot.send_message(user_id, text, reply_markup=kb.city_for_samara)
    elif user['city'] == 'Питер':
        bot.send_message(user_id, text, reply_markup=kb.city_for_piter)
    elif user['city'] == 'Сочи':
        bot.send_message(user_id, text, reply_markup=kb.city_for_sochi)
    else:
        bot.send_message(user_id, text, reply_markup=kb.city_for_omsc)

@bot.callback_query_handler(lambda call: call.data == 'penza')
def penza(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Пенза')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Пенза".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'vladivostok')
def vladivostok(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Владивосток')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Владивосток".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'moscow')
def moscow(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Москва')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Москва".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'samara')
def samara(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Самара')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Самара".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'piter')
def piter(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Питер')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Питер".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'sochi')
def sochi(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Сочи')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Сочи".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)

@bot.callback_query_handler(lambda call: call.data == 'omsc')
def omsc(call):
    user_id = call.from_user.id
    db = Database(user_id, bot)
    db.send_to_city(user_id, 'Омск')
    text1 = f'Отлично!\n'\
            f'Теперь ты в городе "Омск".'
    text2 = f'Чем будешь заниматься в этом прекрасном городе?'
    bot.edit_message_text(text1, user_id, call.message.message_id)
    bot.send_message(user_id, text2, reply_markup=kb.menu_kb)


# Возвраты в меню
@bot.callback_query_handler(lambda call: call.data == 'back_upgrade_speed_mine')
def back_upgrade_speed_mine(call):
    speed_mining(call)

@bot.callback_query_handler(lambda call: call.data == 'back_upgrade_mine')
def back_upgrade_mine(call):
    mine_shop(call)

@bot.callback_query_handler(lambda call: call.data == 'back_mine')
def back_mine(call):
    mine(call)

@bot.callback_query_handler(lambda call: call.data == 'back_job')
def back_job(call):
    user_id = call.from_user.id
    text = f'Выбери на какую работу ты пойдешь?'
    bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=kb.job_kb)

@bot.callback_query_handler(lambda call: call.data == 'back_menu')
def back_menu(call):
    start(call)
    bot.delete_message(call.from_user.id, call.message.message_id)

def scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
    
scheduler_thread = threading.Thread(target=scheduler).start()

bot.polling(non_stop=True, interval=0)

        