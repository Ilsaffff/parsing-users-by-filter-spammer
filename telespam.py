import csv
import time
import random
import requests
import telethon
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

    def parsing_users(self, is_sorting, keywords):
        chat_title = self.get_chat()
        users = self.chat_scraper(chat_title, is_sorting, keywords)
        return users

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
    def get_description(user):
        url = 'https://t.me/' + str(user)
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if user:
            time.sleep(0.1)
            description_html = soup.find(class_='tgme_page_wrap').find(class_='tgme_body_wrap').find(
                class_='tgme_page').find(class_='tgme_page_description')
            if description_html:
                description = description_html.text
                return description

    def chat_scraper(self, target_group, is_sorting, keywords):
        users = []
        print('Scraping members...', end='\r')
        parsing_users = [user for user in self.client.get_participants(target_group, aggressive=False) if user]
        with open(f"{input('Укажите название CSV файла для сохранения данных')}.csv", "w", encoding='UTF-8',
                  newline='') as file:
            csv.writer(file).writerow(('Username', 'First Name', 'Phone', 'Description'))
            if is_sorting:
                for user in parsing_users:
                    if user.username and user.first_name:
                        for keyword in keywords:
                            is_keyword = keyword in self.get_description(user.username).lower()
                            if is_keyword:
                                users.append(user.username)

                                csv.writer(file).writerow(
                                    (user.username, user.first_name, user.phone, self.get_description(user.username)))
                                print(f'Сохранено: {len(users)}')
            else:
                for user in parsing_users:
                    if user.username or user.first_name:
                        users.append(user.username)
                        csv.writer(file).writerow(
                            (user.username, user.first_name, user.phone, self.get_description(user.username)))
                        if len(users) % 10 == 0:
                            print(f'Сохранено: {len(users)}')
            print(f'Сохранено {len(users)} пользователей!\n')
            print('Все данные сохранены!')
            return users

    @staticmethod
    def base_opening(file_name):
        base = []
        with open(file_name, "r", encoding="utf-8") as f:
            [base.append(element.strip()) for element in f.readlines()]
        return base

    def spam(self, users, file_db, time_inf, time_sup):
        delay = random.randint(time_inf, time_sup)
        messages = self.db.get_messages()
        for user in users:
            print("Отправка сообщения пользователю: ", user)
            try:
                self.client.send_message(user, random.choice(messages).text)
            except (PhoneNumberBannedError, PeerFloodError):
                print("[!] Telegram забанил данный аккаунт.\n[!] Скрипт приостановлен.\n"
                      "[!] Переключаем аккаунт")
                self.switching_account(file_db, self.api_id)
                self.connect()
                print('Аккаунт успешно сменён, продолжаем работу')
            except Exception as e:
                print("[!] Ошибка:", e, "\n[!] Пытаемся продолжить работу...")
                continue
            if user != users[-1]:
                print(f"Ждём {delay} секунд")
                time.sleep(delay)
                time.sleep(delay)
        print('\nDone!')
