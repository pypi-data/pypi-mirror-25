# -*- coding: utf-8 -*-
import json
import time

import requests

__author__     = "Usman Mahmood"
__license__    = "MIT"
__version__    = "1.0.2"
__maintainer__ = "Usman Mahmood"

class TelegramBot:
    def __init__(self, token):
        """TelegramBot interacts with Telegram bot servers to send and receive 
        messages.
        """
        self.URI_FMT    = 'https://api.telegram.org/bot{token}/{method_name}'
        self.token      = token
        self.chat_id    = 0
        self.timeout    = 30
        self.handler_fn = None
        self.running    = False

    def set_chat_id(self, chat_id):
        """Set the unique identifier for the target private chat
        
        chat_id -- (integer) - unique chat id
        """
        self.chat_id = chat_id

    def get_chat_id(self):
        """Return the bots current chat id"""
        return self.chat_id

    def set_message_handler(self, handler_fn):
        """Set the message handler to invoke when a new message is received.

        message handler functions have the following signature:

        handler_fn(bot_instance, message)

        'bot_instance' - an instance of the bot which invoked the message handler.
        'message'      - a dict with the structure (assuming text message):

        {
            "message_id" : 123,
            "from": {
                "id"            : 123456789,
                "is_bot"        : false,
                "first_name"    : "<first_name>",
                "language_code" : "en-GB"
            },
            "chat": {
                "id"        : 123456789,
                "first_name": "<first_name>",
                "type"      : "private"
            },
            "date": 1504981128,
            "text": "Hello world!"
        }

        Example:

        def on_new_message(bot, message):
            if message['text'] == "Hello":
                bot.send_message('Hi!')
        
        bot = telegrambot.TelegramBot(<token>)
        bot.set_message_handler(on_new_message)
        bot.wait_for_messages()

        handler_fn -- (function) - function to invoke on new message arrival
        """
        if handler_fn: self.handler_fn = handler_fn

    def me(self):
        """Get basic information about the bot.
        
        Returns (dict):
            
            {
                "id"        : 123456789,
                "is_bot"    : true,
                "first_name": "<first_name>",
                "username"  : "<username>"
            }

        Raises requests.exceptions.HTTPError
        """
        uri      = self.URI_FMT.format(token=self.token, method_name="getMe")
        response = requests.get(uri, timeout=60)            
        if response.status_code != requests.codes.ok:
            response.raise_for_status()
        return json.loads(response.text)['result']

    def send_message(self, text_message, chat_id=0):
        """Send a text message on to a private chat

        If you want a bot that just sends messages on a private chat, and do 
        not care about receiving messages. Then use this method and provide 
        your 'chat_id', i.e.:

        bot.send_message('hello', 123456)

        If you want a bot that can both send and receives messages in different
        chats. Then set the chat id via the set_chat_id method. 

        bot.set_chat_id(123456)
        bot.send_message('hello')

        Here you can adjust the chat id dynamically based on the incoming 
        message.

        text_message -- (str)     - the plain text message to be sent
        chat_id      -- (integer) - unique chat id
        """
        payload = {'text': text_message}
        if chat_id != 0:
            payload['chat_id'] = chat_id
        else:
            payload['chat_id'] = self.chat_id
        uri = self.URI_FMT.format(token=self.token, method_name='sendMessage')
        requests.request('POST', uri, params=payload)

    def wait_for_messages(self):
        """Continually poll, waiting for incoming messages. This method blocks.

        When a message is received, it invokes the set message handler.
        
        Raises requests.exceptions.HTTPError
        """
        uri     = self.URI_FMT.format(token=self.token, method_name='getUpdates')
        payload = {'timeout': self.timeout}
        self.running = True
        while self.running:
            response = requests.get(uri, params=payload, timeout=60)            
            if response.status_code != requests.codes.ok:
                response.raise_for_status()

            update = json.loads(response.text)
            if update['ok'] and len(update['result']) >= 1:
                most_recent       = len(update['result']) - 1
                message           = update['result'][most_recent]['message']
                offset            = update['result'][most_recent]['update_id']
                payload['offset'] = offset + 1
                self.chat_id      = message['chat']['id']
                
                self.handler_fn(self, message)

    def stop(self):
        """Stop the bot from waiting for messages"""
        self.running = False
