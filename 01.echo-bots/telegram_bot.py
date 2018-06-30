import json
import requests

#  봇 토큰
TOKEN = "<TOKEN>"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    try:
        js = json.loads(content)
    except:
        return {}
    else:
        return js


def get_updates(offset):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def parse_messages(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat_id = update["message"]["chat"]["id"]
        except:
            continue
        send_message(chat_id, text)


def send_message(chat_id, text):
    url = URL + "sendMessage?chat_id={}&text={}".format(chat_id, text)
    get_url(url)


def main():
    last_id = 0
    while True:
        try:
            updates = get_updates(last_id)
            if updates.get("result") != "None" and len(updates["result"]) > 0:
                last_id = get_last_update_id(updates) + 1
                parse_messages(updates)
        except:
            pass


if __name__ == "__main__":
    main()
