#!/usr/bin/env python
import telepot
import time
import sys
import os
from telepot.loop import MessageLoop
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

BOT_KEY = 'TELEGRAM_BOT_API_KEY_HERE'
bot = telepot.Bot(BOT_KEY)
DEVELOPER_KEY = 'YOUTUBE_DATA_API_KEY_HERE'


def youtube_search(msg_text):
    youtube = build('youtube', 'v3', developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(q=msg_text, part='id,snippet', maxResults=10).execute()

    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            result = {'id': search_result['id']['videoId'], 'name': search_result['snippet']['title']}
            return result


def handle(msg):
    try:
        chat_id = msg['chat']['id']
        msg_text = msg['text']
        if '/start' in msg_text:
            return

        bot.sendMessage(chat_id=chat_id, text='Processing request...')
    
        result = youtube_search(msg_text)
        browser.get('https://www.youtube.com/watch?v='+result['id'])
        bot.sendMessage(chat_id=chat_id, text='*Now Playing:* ' + result['name'], parse_mode='markdown')

    except WebDriverException as e1:
        bot.sendMessage(chat_id=chat_id, text='Error processing request. Try again!')
        print "Error: " + str(e1)
        python = sys.executable
        os.execl(python, python, * sys.argv)    #restarts script if browser has been closed
    except Exception as e2:
        bot.sendMessage(chat_id=chat_id, text='Error processing request.')
        print "Error: " + str(e2)

browser = webdriver.Firefox()
MessageLoop(bot, handle).run_as_thread()
while 1:
        time.sleep(10)