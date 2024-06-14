from telebot import types

menu_kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3)
menu_kb.add(
    types.KeyboardButton('Работа'),
    types.KeyboardButton('Карта'),
    types.KeyboardButton('Магазин'),
)


job_kb = types.InlineKeyboardMarkup()
job_kb.add(
    types.InlineKeyboardButton('Шахта', callback_data='mine'),
    types.InlineKeyboardButton('?', callback_data='fishing'),
    types.InlineKeyboardButton('Механик', callback_data='mechanic'),
    types.InlineKeyboardButton('Назад', callback_data='back_menu')
)


city_for_penza = types.InlineKeyboardMarkup(row_width=2)
city_for_penza.add(
    types.InlineKeyboardButton('Владивосток', callback_data='vladivostok'),
    types.InlineKeyboardButton('Москва', callback_data='moscow'),
    types.InlineKeyboardButton('Самара', callback_data='samara'),
    types.InlineKeyboardButton('Питер', callback_data='piter'),
    types.InlineKeyboardButton('Сочи', callback_data='sochi'),
    types.InlineKeyboardButton('Омск', callback_data='omsc')
)

city_for_vladivostok = types.InlineKeyboardMarkup(row_width=2)
city_for_vladivostok.add(
    types.InlineKeyboardButton('Пенза', callback_data='penza'),
    types.InlineKeyboardButton('Москва', callback_data='moscow'),
    types.InlineKeyboardButton('Самара', callback_data='samara'),
    types.InlineKeyboardButton('Питер', callback_data='piter'),
    types.InlineKeyboardButton('Сочи', callback_data='sochi'),
    types.InlineKeyboardButton('Омск', callback_data='omsc')
)

city_for_moscow = types.InlineKeyboardMarkup(row_width=2)
city_for_moscow.add(
    types.InlineKeyboardButton('Пенза', callback_data='penza'),
    types.InlineKeyboardButton('Владивосток', callback_data='vladivostok'),
    types.InlineKeyboardButton('Самара', callback_data='samara'),
    types.InlineKeyboardButton('Питер', callback_data='piter'),
    types.InlineKeyboardButton('Сочи', callback_data='sochi'),
    types.InlineKeyboardButton('Омск', callback_data='omsc')
)

city_for_samara = types.InlineKeyboardMarkup(row_width=2)
city_for_samara.add(
    types.InlineKeyboardButton('Пенза', callback_data='penza'),
    types.InlineKeyboardButton('Владивосток', callback_data='vladivostok'),
    types.InlineKeyboardButton('Москва', callback_data='moscow'),
    types.InlineKeyboardButton('Питер', callback_data='piter'),
    types.InlineKeyboardButton('Сочи', callback_data='sochi'),
    types.InlineKeyboardButton('Омск', callback_data='omsc')
)

city_for_piter = types.InlineKeyboardMarkup(row_width=2)
city_for_piter.add(
    types.InlineKeyboardButton('Пенза', callback_data='penza'),
    types.InlineKeyboardButton('Владивосток', callback_data='vladivostok'),
    types.InlineKeyboardButton('Москва', callback_data='moscow'),
    types.InlineKeyboardButton('Самара', callback_data='samara'),
    types.InlineKeyboardButton('Сочи', callback_data='sochi'),
    types.InlineKeyboardButton('Омск', callback_data='omsc')
)

city_for_sochi = types.InlineKeyboardMarkup(row_width=2)
city_for_sochi.add(
    types.InlineKeyboardButton('Пенза', callback_data='penza'),
    types.InlineKeyboardButton('Владивосток', callback_data='vladivostok'),
    types.InlineKeyboardButton('Москва', callback_data='moscow'),
    types.InlineKeyboardButton('Самара', callback_data='samara'),
    types.InlineKeyboardButton('Питер', callback_data='piter'),
    types.InlineKeyboardButton('Омск', callback_data='omsc')
)

city_for_omsc = types.InlineKeyboardMarkup(row_width=2)
city_for_omsc.add(
    types.InlineKeyboardButton('Пенза', callback_data='penza'),
    types.InlineKeyboardButton('Владивосток', callback_data='vladivostok'),
    types.InlineKeyboardButton('Москва', callback_data='moscow'),
    types.InlineKeyboardButton('Самара', callback_data='samara'),
    types.InlineKeyboardButton('Питер', callback_data='piter'),
    types.InlineKeyboardButton('Сочи', callback_data='sochi')
)

# Back
back_upgrade_mine = types.InlineKeyboardMarkup()
back_upgrade_mine.add(
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)

upgrade_mine_kb = types.InlineKeyboardMarkup()
upgrade_mine_kb.add(
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_speed_mine')
)

back_sell_ore_kb = types.InlineKeyboardMarkup()
back_sell_ore_kb.add(
    types.InlineKeyboardButton('Назад', callback_data='back_sell_ore')
)

back_mine_kb = types.InlineKeyboardMarkup()
back_mine_kb.add(
    types.InlineKeyboardButton('Назад', callback_data='back_mine')
)
