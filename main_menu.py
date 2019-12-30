import requests
import json
import testbot
import urllib
import sys


def send_keyboard():
    rjs = testbot.get_updates()
    text, chat_id = testbot.get_last_text_and_id(rjs)
    # Send message and keyboard to specific chat.
    reply_markup = {'keyboard': [[{'text': 'STUFF'}], [{'text': 'INFORMATION'}], [{'text': 'SELLER'}]], 'resize_keyboard': True,
                    'one_time_keyboard': True}
    reply_markup = json.dumps(reply_markup)
    params = ({'text': None, 'chat_id': chat_id, 'reply_markup': reply_markup, 'disable_web_page_preview': 'true'})
    data = urllib.parse.urlencode(params).encode("utf-8")
    return data


def ways_menu():
    rjs = testbot.get_updates()
    text, chat_id = testbot.get_last_text_and_id(rjs)
    keyboard = send_keyboard()
    testbot.send_message(chat_id, keyboard, text="Choose a mode which is necessary for you")
    # forwarder()


# def forwarder():
#     text, chat_id = testbot.get_last_text_and_id(testbot.get_updates())
#     if text == "STUFF":
#         testbot.send_message(chat_id, text="Forward to STUFF mode")
#     elif text == "INFORMATION":
#         testbot.send_message(chat_id, text="Forward to INFORMATION mode")
#     elif text == "SELLER":
#         testbot.send_message(chat_id, text="Forward to SELLER mode")
