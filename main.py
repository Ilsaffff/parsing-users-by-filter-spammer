from TeleSpam import TeleSpam

# API_ID и API_HASH берутся с сайта https://my.telegram.org/
api_id = 0
api_hash = ''
phone = ''
time_inf = 50  # нижняя грань времени
time_sup = 60  # верхняя грань
keywords = ['']
new_obj = TeleSpam(api_id, api_hash, phone)
new_obj.connect()

choise = int(input(
    'Выбери, что ты хочешь сделать:\n'
    '(1) Парсинг всех пользователей с описанием профиля в CSV файл с возможностью рассылки\n'
    '(2) Парсинг пользователей с сортировкой по описанию профиля в CSV файл с возможностью рассылки\n'
    '(3) Рассылка уже имеющихся пользователей\n'
    'Напиши свой выбор'))

if choise in [1, 2]:
    users = None
    if choise == 1:
        users = new_obj.parsing_users(False, keywords)
    elif choise == 2:
        users = new_obj.parsing_users(True, keywords)
    if int(input('Хочешь ли ты сделать рассылку по данным пользователям?\n'
                 '(1) Да\n'
                 '(2) Нет\n'
                 'Напиши свой выбор')) == 1:
        new_obj.spam(users, time_inf, time_sup)
if choise == 3:
    users = new_obj.base_opening('users_database.txt')
    messages = new_obj.base_opening('message_database.txt')
    new_obj.spam(users, time_inf, time_sup)
