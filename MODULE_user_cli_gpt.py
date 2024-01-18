import requests
import asyncio
import time
import logging
import flask
import json
from colorama import Fore


logging.basicConfig(level=logging.INFO, format="%(name)s: %(asctime)s - %(levelname)s - %(message)s")
logging.info("[+] MODULE_user_cli_gpt ready")

# for interaction with the backend
r_headers ={
    "content-type": "application/json",
    'API-KEY': "1234567890"
}


mainloop_endpoint = "http://127.0.0.1:8888/MODULE_usercli_input"


async def main():
    logging.info("Starting user interface module")
    
    while True:
        time.sleep(0.2)
        try:
            r = requests.post(mainloop_endpoint, headers=r_headers, json={"test": 200})
            break
        except Exception:
            logging.debug("Waiting for flask server to start")
    
    
    while True:
        data = input(Fore.RED + "Enter text: ")
        usercli_r = requests.post(mainloop_endpoint, json={"text": data}, headers=r_headers)
        try:
            response = usercli_r.json()
            response = json.loads(response)['output']
        except Exception:
            response = usercli_r.text
        print(Fore.GREEN + response)


    
if __name__ == "__main__":
    asyncio.run(main())