from telespam import TeleSpam
from db import DBHelper


file_db = 'test.db'

# API_ID и API_HASH берутся с сайта https://my.telegram.org/
time_inf = 50  # нижняя грань времени
time_sup = 60  # верхняя грань
obj = TeleSpam(file_db)
obj.connect()

choise = int(input(
    'Выбери, что ты хочешь сделать:\n'
    '(1) Парсинг всех пользователей с описанием профиля в базу данных с возможностью рассылки\n'
    '(2) Парсинг пользователей с сортировкой по описанию профиля в базу данных с возможностью рассылки\n'
    '(3) Рассылка уже имеющихся пользователей\n'
    'Напиши свой выбор'))

if choise in [1, 2]:
    users_id = None
    if choise == 1:
        users_id = obj.parsing_users(is_sorting=False)
    elif choise == 2:
        users_id = obj.parsing_users(is_sorting=True)
    if int(input('Хочешь ли ты сделать рассылку по данным пользователям?\n'
                 '(1) Да\n'
                 '(2) Нет\n'
                 'Напиши свой выбор')) == 1:
        obj.spam(users_id, file_db, time_inf, time_sup)
if choise == 3:
    db = DBHelper(file_db)
    users_id = db.get_users_id()
    obj.spam(users_id, file_db, time_inf, time_sup)
