import requests
import json 
from urllib.parse import unquote ,parse_qs,urlparse
from loguru import logger
import time 
import os
import pyfiglet
from colorama import Fore, Style, init

headers = {
    'accept': '*/*',
    'accept-language': 'en,en-GB;q=0.9,en-US;q=0.8',
    'authorization': '',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://bot.toncircle.org',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://bot.toncircle.org/',
    'x-requested-with': 'org.telegram.messenger',
}

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


def watch(init):
    tgWebAppData =parse_qs( parse_qs(urlparse(init).fragment).get('tgWebAppData', [None])[0])
    user_data = unquote(tgWebAppData['user'][0])
    id = json.loads(user_data)['id']
    chat_instance = tgWebAppData['chat_instance'][0]
    params = {
        'blockId': '3852',
        'tg_id': str(id),
        'tg_platform': 'android',
        'platform': 'Linux arm64',
        'language': 'en',
        'chat_type': 'sender',
        'chat_instance': chat_instance,
    }
    for i in range(1,100000000000):
        requests.get((requests.get('https://api.adsgram.ai/adv', params=params ,headers=headers).json()['banner']['trackings'][-2])['value'])
        logger.info(f'{i} Ad reward claimed')
        time.sleep(60)
        logger.debug('sleeping 1 min for the next Ad')
    #json_data = { 'bet': 1000,'chance': 1}
    #requests.post('https://api.toncircle.org/user/games/upgrade/spin',json=json_data)
    

init(autoreset=True)
if __name__ == '__main__':
    banner_text = "WHYWETAP"
    os.system('cls' if os.name == 'nt' else 'clear')
    create_gradient_banner(banner_text)
    social_media_usernames = [
        ("CryptoNews", "@ethcryptopia"),
        ("Auto Farming", "@whywetap"),
        ("Auto Farming", "@autominerx"),
        #("", ""),
        ("programmer ", "@demoncratos"),
    ]
    print_info_box(social_media_usernames)
    link = input("\nEnter your Circle session link : ")
    watch(link)
