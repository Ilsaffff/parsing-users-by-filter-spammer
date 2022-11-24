from TeleSpam import TeleSpam

# API_ID и API_HASH берутся с сайта https://my.telegram.org/
api_id = 0
api_hash = ''
phone = ''
time_inf = 50  # нижняя грань времени
time_sup = 60  # верхняя грань
keywords = ['', '']  # слова, которые должны встречаться в описании
new_obj = TeleSpam(api_id, api_hash, phone, time_inf, time_sup, keywords)
new_obj.connect()

choise = int(input(
    'Выбери, что ты хочешь сделать:\n(1) Парсинг пользователей с фильтром с группы Telegram и рассылка по ним\n'
    '(2) Рассылка уже имеющихся пользователей\n'
    'Нажми 1 или 2'))
print(choise)
match choise:
    case 1:
        new_obj.get_chats()
    case 2:
        users = new_obj.base_opening('users_database.txt')
        messages = new_obj.base_opening('message_database.txt')
        new_obj.spam(users, messages)
