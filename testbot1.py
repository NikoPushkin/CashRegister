import requests
import time
import json
import urllib
import main_menu
from informationMode import DBHelper

db = DBHelper()


TOKEN = "1036896432:AAGW_qwSgpWxfNRTMJmLTaXRbblcGf81uRk"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    r = requests.get(url)
    content = r.content.decode("utf8")
    rjs = json.loads(content)
    return rjs


def get_last_update_id(rjs):
    update_ids = []
    for update in rjs["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def handle_updates(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.get_items()
            if text in items:
                db.delete_item(text)
                items = db.get_items()
            else:
                db.add_item(text)
                items = db.get_items()
            message = "\n".join(items)
            send_message(message, chat)
        except KeyError:
            pass


def get_last_text_and_id(rjs):
    try:
        text = rjs['result'][-1]['message']['text']
        chat_id = rjs['result'][-1]['message']['from']['id']
    except:
        pass

    return (text, chat_id)

def send_message(chat_id, keyboard=None, text=None):
    text = urllib.parse.quote_plus(text)
    r = requests.get(URL + 'sendMessage?chat_id={}&text={}'.format(chat_id, text), keyboard)
    content = r.content.decode("utf8")
    return content


def main():
    db.setup()
    last_update_id = None
    while True:
        rjs = get_updates(last_update_id)
        text, chat_id = get_last_text_and_id(rjs)
        if len(rjs["result"]) > 0:
            if text == "/start":
                last_update_id = get_last_update_id(rjs) + 1
                send_message(chat_id, text="Hello, dear friend! My congratulations with new working day")
                main_menu.ways_menu()
            elif text == "INFORMATION":
                handle_updates(rjs)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
