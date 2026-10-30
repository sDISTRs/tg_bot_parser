import requests
import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("TOKEN")
parsing_url =os.environ.get("PARSING_URL")
proxy_address = os.environ.get("PROXY_ADDRESS")
group_id = os.environ.get("GROUP_ID")
chat__id = os.environ.get("CHAT_ID")
url = f"https://api.telegram.org/bot{token}/sendMessage"

response = requests.get(str(parsing_url))


def send_message(chat_id, text):
    proxies = {
        "http": proxy_address,
        "https": proxy_address
    }
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload, proxies=proxies)




while True:
    if response.status_code == 200:
        response_json = {}
        try:
            response_json = response.json()
        except Exception as e:
            print("error convert to json", e)
        if response_json:
            response_list = []
            try:
                response_list = response_json.get("data").get("type").values()
            except Exception as e:
                print("convert json to list error", e)
            if response_list:
                sign_dict ={}
                for sign in response_list:
                    try:
                        name = sign.get("name")
                        today = sign.get("today")
                        sign_dict[name] = today
                    except Exception as e:
                        print("module sign error", e)
                if len(sign_dict) == 12:
                    try:
                        send_message(group_id, datetime.datetime.now().strftime("%d.%m.%Y"))
                        for sign in sign_dict.values():
                            send_message(group_id, sign)
                        break
                    except Exception as e:
                        print("module send tg error", e)
                else:
                    print("error len sign")
            else:
                print("no response_dict")
        else:
            print("no response_json")
    else:
        print("error response", response.status_code)
    time.sleep(3600)