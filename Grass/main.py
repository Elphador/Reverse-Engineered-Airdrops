import requests
import asyncio
import random
import ssl
import json
import time
import uuid
from loguru import logger
import websockets
from fake_useragent import UserAgent
import os
import pyfiglet
from colorama import Fore, Style, init


def create_gradient_banner(text):
    banner = pyfiglet.figlet_format(text).splitlines()
    colors = [Fore.GREEN + Style.BRIGHT, Fore.YELLOW + Style.BRIGHT, Fore.RED + Style.BRIGHT]
    total_lines = len(banner)
    section_size = total_lines // len(colors)
    for i, line in enumerate(banner):
        if i < section_size:
            print(colors[0] + line)  # Green
        elif i < section_size * 2:
            print(colors[1] + line)  # Yellow
        else:
            print(colors[2] + line)  # Red

def print_info_box(social_media_usernames):
    colors = [Fore.CYAN, Fore.MAGENTA, Fore.LIGHTYELLOW_EX, Fore.BLUE, Fore.LIGHTWHITE_EX]
    
    box_width = max(len(social) + len(username) for social, username in social_media_usernames) + 4
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')
    
    for i, (social, username) in enumerate(social_media_usernames):
        color = colors[i % len(colors)]  # Cycle through colors
        print(color + f'| {social}: {username} |')
    
    print(Fore.WHITE + Style.BRIGHT + '+' + '-' * (box_width - 2) + '+')

init(autoreset=True)

async def connect_to_wss(user_id):
    user_agent = UserAgent(os=['windows', 'macos', 'linux'], browsers='chrome')
    random_user_agent = user_agent.random
    device_id = str(uuid.uuid4())
    logger.info(device_id)
    while True:
        try:
            await asyncio.sleep(random.randint(1, 10) / 10)
            custom_headers = {
                "User-Agent": random_user_agent,
                "Origin": "chrome-extension://lkbnfiajjmbhnfledhphioinpickokdi"
            }
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            urilist = ["wss://proxy.wynd.network:4444/","wss://proxy.wynd.network:4650/"]
            uri = random.choice(urilist)
            server_hostname = "proxy.wynd.network"
            async with websockets.connect(uri, ssl=ssl_context, extra_headers=custom_headers,server_hostname=server_hostname) as websocket:
                async def send_ping():
                    while True:
                        send_message = json.dumps(
                            {"id": str(uuid.uuid4()), "version": "1.0.0", "action": "PING", "data": {}})
                        logger.debug(send_message)
                        await websocket.send(send_message)
                        await asyncio.sleep(5)

                await asyncio.sleep(1)
                asyncio.create_task(send_ping())

                while True:
                    response = await websocket.recv()
                    message = json.loads(response)
                    logger.info(message)
                    if message.get("action") == "AUTH":
                        auth_response = {
                            "id": message["id"],
                            "origin_action": "AUTH",
                            "result": {
                                "browser_id": device_id,
                                "user_id": user_id,
                                "user_agent": custom_headers['User-Agent'],
                                "timestamp": int(time.time()),
                                "device_type": "extension",
                                "version": "4.26.2",
                                "extension_id": "lkbnfiajjmbhnfledhphioinpickokdi"
                            }
                        }
                        logger.debug(auth_response)
                        await websocket.send(json.dumps(auth_response))

                    elif message.get("action") == "PONG":
                        pong_response = {"id": message["id"], "origin_action": "PONG"}
                        logger.debug(pong_response)
                        await websocket.send(json.dumps(pong_response))
        except Exception as e:
            logger.error(e)


async def main():
    banner_text = "WHYWETAP"
    os.system('cls' if os.name == 'nt' else 'clear')
    create_gradient_banner(banner_text)
    social_media_usernames = [
        ("CryptoNews", "@ethcryptopia"),
        ("Auto Farming", "@whywetap"),
        ("Auto Farming", "@autominerx"),
        ("Thanks @ylasgamers", "for simpliyfing most work"),
        ("improved by ", "@demoncratos"),
    ]

    print_info_box(social_media_usernames)
    with open('credits.txt', 'r') as file:
            credit = file.read()
    if '|' in credit :
        email , password = credit.split('|') 
    else:
        email = input("\nEnter your Grass Email : ")
        password = input("Enter your Grass Password : ")
    data = {"username":email,"password":password}
    response = requests.post('https://api.getgrass.io/login', json=data)
    _user_id  = (response.json()['result']['data']['userId'])
    await connect_to_wss(_user_id)

if __name__ == '__main__':
    asyncio.run(main())
