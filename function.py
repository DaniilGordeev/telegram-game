import random

def random_ore(): # Функция рандомного выбора руды.
    number = random.randint(0,100)/100
    if number >= 0 and number <= 0.6:
        return 'add_stone'
    elif number >= 0.61 and number <= 0.8:
        return 'add_metall'
    elif number >= 0.81 and number <= 0.95:
        return 'add_silver'
    else:
        return 'add_gold'

    