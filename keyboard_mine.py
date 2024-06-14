from telebot import types

mine_kb = types.InlineKeyboardMarkup()
mine_kb.add(
    types.InlineKeyboardButton('Копать', callback_data='mine_start'),
    types.InlineKeyboardButton('Улучшения', callback_data='mine_upgrade'),
    types.InlineKeyboardButton('Продать руду', callback_data='sell_ore'),
    types.InlineKeyboardButton('Назад', callback_data='back_job')
)

mine_upgrade_kb = types.InlineKeyboardMarkup()
mine_upgrade_kb.add(
    types.InlineKeyboardButton('Скорость', callback_data='speed_mining'),
    types.InlineKeyboardButton('Макс. кол-во ресурсов', callback_data='max_amount_ore_upgrade'),
    types.InlineKeyboardButton('Назад', callback_data='back_mine')
)

speed_mining_kb_1 = types.InlineKeyboardMarkup()
speed_mining_kb_1.add(
    types.InlineKeyboardButton('Улучшить', callback_data='upgrade_speed_mining_1'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)
speed_mining_kb_2 = types.InlineKeyboardMarkup()
speed_mining_kb_2.add(
    types.InlineKeyboardButton('Улучшить', callback_data='upgrade_speed_mining_2'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)
speed_mining_kb_3 = types.InlineKeyboardMarkup()
speed_mining_kb_3.add(
    types.InlineKeyboardButton('Улучшить', callback_data='upgrade_speed_mining_3'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)
speed_mining_kb_4 = types.InlineKeyboardMarkup()
speed_mining_kb_4.add(
    types.InlineKeyboardButton('Улучшить', callback_data='upgrade_speed_mining_4'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)
speed_mining_kb_5 = types.InlineKeyboardMarkup()
speed_mining_kb_5.add(
    types.InlineKeyboardButton('Улучшить', callback_data='upgrade_speed_mining_5'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)
speed_mining_kb_end = types.InlineKeyboardMarkup()
speed_mining_kb_end.add(
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)

max_amount_ore_upgrade_kb_1 = types.InlineKeyboardMarkup()
max_amount_ore_upgrade_kb_1.add(
    types.InlineKeyboardButton('50.000', callback_data='max_amount_ore_1'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)

max_amount_ore_upgrade_kb_2 = types.InlineKeyboardMarkup()
max_amount_ore_upgrade_kb_2.add(
    types.InlineKeyboardButton('100.000', callback_data='max_amount_ore_2'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)

max_amount_ore_upgrade_kb_3 = types.InlineKeyboardMarkup()
max_amount_ore_upgrade_kb_3.add(
    types.InlineKeyboardButton('250.000', callback_data='max_amount_ore_3'),
    types.InlineKeyboardButton('Назад', callback_data='back_upgrade_mine')
)