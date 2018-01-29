#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path
import json
from slackclient import SlackClient
from telegram import Bot


class ChelentanoEdaException(Exception):
    pass


class ChelentanoEda:

    def __init__(self, config_file):
        self.config_file = config_file

        self.__read_config()

    def run(self):
        if self.channel is None or self.timestamp is None:
            self.__print_question()
        else:
            self.__send_count()
            self.__reset_question()

        self.__save_config()

    def __print_question(self):
        sc = SlackClient(self.slack_token)
        result = sc.api_call(
            'chat.postMessage',
            channel=self.quiz_channel,
            text=self.who_will_eat
        )

        sc.api_call('reactions.add', name='+1', channel=result['channel'], timestamp=result['ts'])

        self.channel = result['channel']
        self.timestamp = result['ts']

    def __send_count(self):
        sc = SlackClient(self.slack_token)
        result = sc.api_call('reactions.get', channel=self.channel, timestamp=self.timestamp, full=True)

        count = 0

        for reaction in result['message']['reactions']:
            count += reaction['count']

        count -= 1  # minus bot

        message = self.how_much_eat % count

        # help to add bot at private channel
        # https://gist.github.com/vertigra/0f9c37b6fe0bb187a478c47e46b388c9
        bot = Bot(token=self.telegram_token)
        bot.send_message(chat_id=self.telegram_chat, text=message)

    def __reset_question(self):
        self.channel = None
        self.timestamp = None

    def __read_config(self):
        if not os.path.isfile(self.config_file):
            raise ChelentanoEdaException('config not found')

        with open(self.config_file) as f:
            config = json.load(f)
            self.channel = config['channel']
            self.timestamp = config['timestamp']
            self.webhook_url = config['webhook_url']
            self.slack_token = config['slack_token']
            self.telegram_token = config['telegram_token']
            self.who_will_eat = config['who_will_eat']
            self.how_much_eat = config['how_much_eat']
            self.quiz_channel = config['quiz_channel']
            self.telegram_chat = config['telegram_chat']

    def __save_config(self):
        config = {
            'channel': self.channel,
            'timestamp': self.timestamp,
            'webhook_url': self.webhook_url,
            'slack_token': self.slack_token,
            'telegram_token': self.telegram_token,
            'who_will_eat': self.who_will_eat,
            'how_much_eat': self.how_much_eat,
            'quiz_channel': self.quiz_channel,
            'telegram_chat': self.telegram_chat,
        }

        config = json.dumps(config, indent=4, ensure_ascii=False)

        with open(self.config_file, 'w') as f:
            f.write(config)
