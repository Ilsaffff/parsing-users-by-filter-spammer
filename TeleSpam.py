import time
import random
import requests
from bs4 import BeautifulSoup as bs

from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PeerFloodError, SessionPasswordNeededError


class TeleSpam:
    def __init__(self, api_id, api_hash, phone, time_inf, time_sup, keywords):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.time_inf = time_inf
        self.time_sup = time_sup
        self.keywords = keywords
        self.client = TelegramClient(self.phone, self.api_id, self.api_hash)

    def connect(self):
        """Connecting client to Telegram"""
        self.client.connect()
        print('Connecting...', end='\r')
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            try:
                self.client.sign_in(self.phone, input('Enter verification code: '))
            except SessionPasswordNeededError:
                self.client.sign_in(password=input("Enter password: "))
        print('Client is connected.', end='\r')

    def get_chats(self):
        """Getting all user`s chats"""
        groups = [dialog for dialog in self.client.get_dialogs() if dialog.is_group and dialog.is_channel]
        print('From which chat you want to parse members:')
        [print(str(groups.index(g) + 1) + ' - ' + g.title) for g in groups]
        print('Exit - any other symbol')
        self.choice_checker(groups)

    def choice_checker(self, groups):
        if not (user_input := input("\nPlease! Enter a Number: ")).isdigit() or \
                int(user_input) not in range(1, len(groups)):
            print('\nBye!\n')
            pass
        else:
            self.chat_scraper(groups[int(user_input) - 1])

    def search_description(self, user):
        url = 'https://t.me/' + user
        r = requests.get(url)
        soup = bs(r.text, "html.parser")
        description_html = soup.find(class_='tgme_page')
        is_search = False
        for description in self.keywords:
            is_description = description in description_html.text.lower().replace(' ', '')
            if is_description:
                is_search = True
        return is_search

    def chat_scraper(self, target_group):
        """Collecting chat members"""
        filter_users = []
        print('Scraping members...', end='\r')
        users = [user.username for user in self.client.get_participants(target_group, aggressive=False) if
                 user.username]
        for user in users:
            if self.search_description(user):
                filter_users.append(user)
                print(user)
        print(f'Scraped {len(filter_users)} members!')
        while (answer := input('\nDo you wanna save(1) or continue to spam(2)? ')) not in ['1', '2']:
            print('Choose 1 or 2')
        if answer == '2':
            messages = self.message_text()
            self.spam(filter_users, messages)
        elif answer == '1':
            print('Saving In file...')
            with open(f"{target_group.title}", "w", encoding='UTF-8') as f:
                [f.write(user + '\n') for user in filter_users]
            print('Done!')

    def message_text(self):
        messages = self.base_opening('message_database.txt')
        print(messages)
        return messages

    def base_opening(self, file_name):
        """Opening database"""
        base = []
        with open(file_name, "r", encoding="utf-8") as f:
            [base.append(element.strip()) for element in f.readlines()]
        return base

    def spam(self, users, messages):
        """Spam to users"""
        delay = random.randint(self.time_inf, self.time_sup)
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
    new_obj.get_chats()
