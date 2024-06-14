import sqlite3
from typing import Optional
from telebot import TeleBot


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database:

    _user_id: Optional[int]
    _db: sqlite3.Connection
    _cursor: sqlite3.Cursor

    def __init__(self, user_id: Optional[int] = None, bot: Optional[TeleBot] = None): # Инициализация БД
        self._user_id = user_id
        self._db = sqlite3.Connection("users.db", check_same_thread=False)
        self._db.row_factory = dict_factory
        self._cursor = self._db.cursor()
    
    def check_users(self, user_id): # Проверка, существует ли пользователь
        self._user_id = user_id
        self._cursor.execute("SELECT * FROM users WHERE id = ?", (self._user_id,))
        user = self._cursor.fetchone()
        if user is None:
            return True
        else:
            return False
    
    def check_name_users(self, name): # Проверка свободного имени
        self._name = str(name)
        self._cursor.execute("SELECT name FROM users WHERE name = ?", (self._name, ))
        return self._cursor.fetchone()

    def get_user(self, user_id, name): # Регистрация пользователя
        self._name = str(name)
        self._user_id = user_id
        self._cursor.execute("INSERT INTO users (id, lvl, money, name, city, payday) VALUES (?, 1, 1000, ?, 'Пенза', 10)", (self._user_id, self._name,))
        self._db.commit()

    def get_me(self, user_id): # Получение данных о пользователе 
        self._user_id = user_id
        self._cursor.execute("SELECT * FROM users WHERE id = ?", (self._user_id, ))
        return self._cursor.fetchone()

    # Отправка в другие города 
    def send_to_city(self, user_id, city):
        self._user_id = user_id
        self._city = str(city)
        self._cursor.execute("UPDATE users SET city = ? WHERE id = ?", (self._city, self._user_id, ))
        self._db.commit()
    

    # Шахта - работа
    def check_mine(self, user_id): # Проверка, существует ли пользователь
        self._user_id = user_id
        self._cursor.execute("SELECT * FROM mine WHERE id = ?", (self._user_id,))
        user = self._cursor.fetchone()
        if user is None:
            return True
        else:
            return False
        
    def init_mine(self, user_id):
        self._user_id = user_id
        self._cursor.execute("INSERT INTO mine (id, max_amount_ore, spped_mining, stone, metall, silver, gold, mining_hour) VALUES (?, 30, 1, 0, 0, 0, 0, 0)", (self._user_id, ))
        self._db.commit()
    
    def get_me_mine(self, user_id):
        self._user_id = user_id
        self._cursor.execute("SELECT * FROM mine WHERE id = ?", (self._user_id, ))
        return self._cursor.fetchone()
    
    def add_stone(self, user_id):
        self._user_id = user_id
        self._cursor.execute("UPDATE mine SET stone = stone + 1 WHERE id = ?", (self._user_id, ))
        self._cursor.execute("UPDATE mine SET mining_hour = mining_hour + 1 WHERE id = ?", (self._user_id, ))
        self._db.commit()
    
    def add_metall(self, user_id):
        self._user_id = user_id
        self._cursor.execute("UPDATE mine SET metall = metall + 1 WHERE id = ?", (self._user_id, ))
        self._cursor.execute("UPDATE mine SET mining_hour = mining_hour + 1 WHERE id = ?", (self._user_id, ))
        self._db.commit()

    def add_silver(self, user_id):
        self._user_id = user_id
        self._cursor.execute("UPDATE mine SET silver = silver + 1, mining_hour = mining_hour + 1  WHERE id = ?", (self._user_id, ))
        self._cursor.execute("UPDATE mine SET mining_hour = mining_hour + 1 WHERE id = ?", (self._user_id, ))
        self._db.commit()

    def add_gold(self, user_id):
        self._user_id = user_id
        self._cursor.execute("UPDATE mine SET gold = gold + 1 WHERE id = ?", (self._user_id, ))
        self._cursor.execute("UPDATE mine SET mining_hour = mining_hour + 1 WHERE id = ?", (self._user_id, ))
        self._db.commit()

    # Улушение скорости
    def upgrade_speed(self, user_id, money):
        self._user_id = user_id
        self._money = str(money)
        self._cursor.execute("UPDATE mine SET speed_mining = speed_mining + 1 WHERE id = ?", (self._user_id, ))
        self._cursor.execute(f"UPDATE users SET money = money - {money} WHERE id = ?", (self._user_id, ))
        self._db.commit()
    
    # Улучшение объема добычи руды 
    def max_amount_ore(self, user_id, money, amount):
        self._user_id = user_id
        self._money = str(money)
        self._amount = str(amount)
        self._cursor.execute(f"UPDATE mine SET max_amount_ore = {self._amount} WHERE id = ?", (self._user_id, ))
        self._cursor.execute(f"UPDATE users SET money = money - {self._money} WHERE id = ?", (self._user_id, ))
        self._db.commit()

    # Продажа руды
    def sell_ore(self, user_id, price, count, ore):
        self._user_id = user_id
        self._price = price
        self._count = int(count)
        self._ore = ore
        self._cursor.execute(f"UPDATE mine SET {ore} = {ore} - {self._count} WHERE id = ?", (self._user_id, ))
        self._cursor.execute(f'UPDATE users SET money = money + {self._price * self._count} WHERE id = ?', (self._user_id, ))
        self._db.commit()


    def check_payday(self):
        self._cursor.execute("SELECT id FROM users WHERE payday >= 1")
        return self._cursor.fetchall()
    
    def update_data_payday(self, user_id):
        self._user_id = user_id
        self._cursor.execute("UPDATE users SET "\
                            "money = money + 5000, "\
                            "lvl = lvl + 1, "\
                            "payday = payday - 1 "\
                            "WHERE id = ? ",
                            (self._user_id, ))
        self._db.commit()