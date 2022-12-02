from telespam import TeleSpam


file_db = ''

# API_ID и API_HASH берутся с сайта https://my.telegram.org/
time_inf = 50  # нижняя грань времени
time_sup = 60  # верхняя грань
keywords = ['']
obj = TeleSpam(file_db)
obj.connect()

choise = int(input(
    'Выбери, что ты хочешь сделать:\n'
    '(1) Парсинг всех пользователей с описанием профиля в CSV файл с возможностью рассылки\n'
    '(2) Парсинг пользователей с сортировкой по описанию профиля в CSV файл с возможностью рассылки\n'
    '(3) Рассылка уже имеющихся пользователей\n'
    'Напиши свой выбор'))

if choise in [1, 2]:
    users = None
    file_name = input('Введи название файла, куда ты хочешь спарсить юзеров')
    if choise == 1:
        users = obj.parsing_users(False, keywords)
    elif choise == 2:
        users = obj.parsing_users(True, keywords)
    if int(input('Хочешь ли ты сделать рассылку по данным пользователям?\n'
                 '(1) Да\n'
                 '(2) Нет\n'
                 'Напиши свой выбор')) == 1:
        obj.spam(users, file_db, time_inf, time_sup)
if choise == 3:
    users = obj.base_opening('users_database.txt')
    messages = obj.base_opening('message_database.txt')
    obj.spam(users, file_db, time_inf, time_sup)
