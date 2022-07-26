import typer
import random
import requests, json
from time import sleep
from threading import Thread

app = typer.Typer()

@app.command()
def main(amount: int, delay: int, single: bool = False, verbose: bool = False):
    global messages, wait, proxy_list
    messages = list(open("messages.txt", "r"))
    webhooks = list(open("urls.txt", "r"))
    proxy_list = list(open("proxies.txt", "r"))
    wait = delay
    if single:
        url = webhooks[0]
        token = url.split("/")[-1]
        wid = url.split("/")[-2]
        Thread(target=spam, args=(amount, wid, token, verbose)).start()
    else:
        for url in webhooks:
            token = url.split("/")[-1]
            wid = url.split("/")[-2]
            Thread(target=spam, args=(amount, wid, token, verbose)).start()

def spam(amount, wid, token, verbose):
    for request in range(amount):
        global proxy
        proxy = random.choice(proxy_list)
        message = random.choice(messages)
        execute(wid, token, message, verbose)
        sleep(wait)

def execute(wid, token, message, verbose):
    data = json.load(open("config.json", "r"))
    data["content"] = message
    data["username"] = token[2:10]
    try:
        response = requests.post(f"https://discord.com/api/v9/webhooks/{wid}/{token}", json=data, proxies={"http": proxy, "https": proxy}, timeout=3)
    except:
        print("Bad Proxy")
        return
    if verbose:
        print("---------------")
        print(response)
        print(proxy[:-1])
        print(response.headers["x-ratelimit-remaining"])
        print("---------------")

if __name__ == "__main__":
    app()
