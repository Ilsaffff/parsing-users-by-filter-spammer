### Chat member parser by filter in description and spammer for Telegram

#### Installing
Use the command to install dependencies "pip install -r requirements.txt" or "pip3 install -r requirements.txt"

#### Import
```from TeleSpam import TeleSpam```

#### Use my.telegram.org for getting api_id and api_hash. 'phone' should be str, time - int, keywords - list of str.
 ```new_obj = TeleSpam(api_id, api_hash, phone, time_inf, time_sup, keywords)```\
 ```new_obj.connect()```

#### Example of importing the entire program.
```new_obj.get_chats()```

#### Example of using only a spammer with ready-made databases. Each message must be on a separate line. Delay it's randoint(time_inf, time_sup). Check Telegram limits for sending messages. It`s change often.
```users = new_obj.base_opening('users_database.txt')```\
```messagess = new_obj.base_opening('message_database.txt')```\
```new_obj.spam(users, message)```

#### The same example, but the spam function takes lists as input.
```users = ['user1', 'user2', 'user3']```\
```messagess = ['Привет! Как дела?', 'Занимаешься бизнесом?', 'Я создаю стартап, хочешь присоединиться в мою команду?']```\
```new_obj.spam(users, messagess)```
