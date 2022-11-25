import csv
import time
import random
import requests
from bs4 import BeautifulSoup as bs
import pandas

from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError, SessionPasswordNeededError


class TeleSpam:
    def __init__(self, api_id, api_hash, phone):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)

    def connect(self):
        """Connecting client to Telegram"""
        self.client.connect()
        print('Connecting...', end='\r')
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            try:
                self.client.sign_in(self.phone, input('Введите код верификации: '))
            except SessionPasswordNeededError:
                self.client.sign_in(password=input("Введите пароль: "))
        print('Соединение установлено.', end='\r')

    def parsing_users(self, is_sorting, keywords):
        chat_title = self.get_chat()
        self.chat_scraper(chat_title, is_sorting, keywords)

    def get_chat(self):
        """Getting all user`s chats"""
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

    def get_description(self, user):
        url = 'https://t.me/' + str(user)
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        if user:
            description_html = soup.find(class_='tgme_page_description')
            if description_html:
                description_html = description_html.text
                return description_html

    def chat_scraper(self, target_group, is_sorting, keywords):
        """Collecting chat members"""
        # users = {'username': [], 'description': []}
        users = []
        user_number = 0
        print('Scraping members...', end='\r')
        print(self.client.get_participants(target_group, aggressive=False))
        parsing_users = [user for user in self.client.get_participants(target_group, aggressive=False) if user]
        with open(f"{input('Укажите название CSV файла для сохранения данных')}.csv", "w", encoding='UTF-8') as file:
            csv.writer(file).writerow(('Username', 'First Name', 'Phone', 'Description'))
            if is_sorting:
                for user in parsing_users:
                    if user.username and user.first_name:
                        for keyword in keywords:
                            is_keyword = keyword in self.get_description(user.username)
                            if is_keyword:
                                user_number = user_number + 1
                                users.append({
                                    'username': user.username,
                                    'first_name': user.first_name,
                                    'phone': user.phone,
                                    'description': self.get_description(user.username)
                                })
                                csv.writer(file).writerow(
                                    (user['username'], user['first_name'], user['phone'], user['description']))
                                print(f'Сохранено: {user_number}')
            else:
                for user in parsing_users:
                    if user.username and user.username:
                        user_number = user_number + 1
                        users.append({
                            'username': user.username,
                            'first_name': user.first_name,
                            'phone': user.phone,
                            'description': self.get_description(user.username)
                        })
                        csv.writer(file).writerow(
                            (user['username'], user['first_name'], user['phone'], user['description']))
                        if user_number % 10 == 0:
                            print(f'Сохранено: {user_number}')
            print(f'Сохранено {user_number} пользователей!\n')
            print('Все данные сохранены!')

    def get_messages(self):
        messages = self.base_opening('message_database.txt')
        print(messages)
        return messages

    def base_opening(self, file_name):
        """Opening database"""
        base = []
        with open(file_name, "r", encoding="utf-8") as f:
            [base.append(element.strip()) for element in f.readlines()]
        return base

    def spam(self, users, time_inf, time_sup):
        """Spam to users"""
        delay = random.randint(time_inf, time_sup)
        messages = self.get_messages()
        for user in users:
            print("Sending Message to: ", user)
            try:
                self.client.send_message(user, random.choice(messages))
            except PeerFloodError:
                print("[!] Getting Flood Error from telegram. \n [!] Script is stopping now. \n"
                      "[!] Please try again after some time.")
                self.client.disconnect()
                self.client.disconnect()
                break
            except Exception as e:
                print("[!] Error:", e, "\n[!] Trying to continue...")
                continue
            else:
                if user != users[-1]:
                    print(f"Waiting {delay} seconds")
                    time.sleep(delay)
                    time.sleep(delay)
        print('\nEnd of the program')


if __name__ == '__main__':
    api_id = 0000000
    api_hash = ''
    phone = ''

    new_obj = TeleSpam(api_id, api_hash, phone)
    new_obj.connect()
    new_obj.get_chat()