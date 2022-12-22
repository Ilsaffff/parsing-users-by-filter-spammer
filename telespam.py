import time
import random
import requests

from bs4 import BeautifulSoup as bs
from db import DBHelper

from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError, PhoneNumberBannedError, SessionPasswordNeededError


class TeleSpam:
    def __init__(self, file_db):
        self.file_db = file_db
        self.db = DBHelper(file_db)
        self.api_id = self.db.get_log().api_id
        self.api_hash = self.db.get_log().api_hash
        self.phone = self.db.get_log().phone
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)

    def connect(self):
        self.client.connect()
        print('Connecting...', end='\r')
        if not self.client.is_user_authorized():
            try:
                self.client.send_code_request(self.phone)
            except PhoneNumberBannedError:
                print('Данный аккаунт забанен\nМеняем аккаунт')
                self.db.delete_log(self.api_id)
                logs = self.db.get_log()
                self.api_id = logs.api_id
                self.api_hash = logs.api_hash
                self.phone = logs.phone
                self.client = TelegramClient(self.phone, self.api_id, self.api_hash)
            try:
                self.client.sign_in(self.phone, input('Введите код верификации: '))
            except SessionPasswordNeededError:
                self.client.sign_in(password=input("Введите пароль: "))
        print('Соединение установлено.', end='\r')

    def switching_account(self, current_api_id):

        self.db.delete_log(current_api_id)
        log = self.db.get_log()
        self.api_id = log.api_id
        self.api_hash = log.api_hash
        self.phone = log.phone

    def parsing_users(self, is_sorting):
        chat_title = self.get_chat()
        users_id = self.chat_scraper(chat_title, is_sorting)
        return users_id

    def get_chat(self):
        chats = [dialog for dialog in self.client.get_dialogs() if dialog.is_group and dialog.is_channel]
        print('С какого чата ты хочешь парсить участников?:')
        [print(str(chats.index(g)) + ' - ' + g.title) for g in chats]
        print('Выход - любой другой символ')
        if not (user_input := input("\nВыбери номер чата")).isdigit() or \
                int(user_input) not in range(len(chats)):
            print('\nBye!\n')
            pass
        else:
            chat = chats[int(user_input)]
            return chat

    @staticmethod
    def get_description(username):
        url = 'https://t.me/' + str(username)
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if username:
            time.sleep(0.1)
            description_html = soup.find(class_='tgme_page_wrap').find(class_='tgme_body_wrap').find(
                class_='tgme_page').find(class_='tgme_page_description')
            if description_html:
                description = description_html.text
                return description

    def chat_scraper(self, target_group, is_sorting):
        users = {'first_name': [], 'username': []}
        print('Scraping members...', end='\r')
        users_list = [user for user in self.client.get_participants(target_group, aggressive=False) if user]
        table_name = self.db.add_table_users(input('Введи название таблицы, куда будут сохранены пользователи'))
        if is_sorting:
            for user in users_list:
                if user.username:
                    for keyword in self.db.get_keywords():
                        is_keyword = keyword.text.lower() in self.get_description(user.username).lower()
                        if is_keyword:
                            users['first_name'].append(user.first_name)
                            users['username'].append(user.username)
                            self.db.add_user(users_table=table_name, username=user.username,
                                             first_name=user.first_name, last_name=user.last_name,
                                             phone=user.phone, description=self.get_description(user.username))
                            print(f'Сохранено: {len(users["username"])}')
        else:
            for user in users_list:
                if user.username:
                    print(user)
                    users['first_name'].append(user.first_name)
                    users['username'].append(user.username)
                    self.db.add_user(users_table=table_name, username=user.username,
                                     first_name=user.first_name, last_name=user.last_name,
                                     phone=user.phone, description=self.get_description(user.username))
                    if len(users['username']) % 10 == 0:
                        print(f'Сохранено: {len(users["username"])}')
            print(f'Сохранено {len(users["username"])} пользователей!\n')
            print('Все данные сохранены!')
            return users

    def spam(self, users, file_db, time_inf, time_sup):
        messages = self.db.get_messages()
        messages_count = 0
        for user in range(len(users['username'])):
            print("Отправка сообщения пользователю: ", users['username'][user])
            messages_count += 1
            print(f'Отправлено {messages_count} сообщений!')
            try:
                message = f'{users["first_name"][user]}' + random.choice(messages).text
                self.client.send_message(users["username"][user], message=message)
            except (PhoneNumberBannedError, PeerFloodError):
                print("[!] Telegram забанил данный аккаунт.\n[!] Скрипт приостановлен.\n"
                      "[!] Переключаем аккаунт")
                self.switching_account(file_db, self.api_id)
                self.connect()
                print('Аккаунт успешно сменён, продолжаем работу')
            except Exception as e:
                print("[!] Ошибка:", e, "\n[!] Пытаемся продолжить работу...")
                continue
            if user != len(users['username']):
                delay = random.randint(time_inf, time_sup)
                print(f"Ждём {delay} секунд")
                time.sleep(delay)
        print('\nDone!')
