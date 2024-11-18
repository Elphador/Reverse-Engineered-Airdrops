from urllib.parse import urlparse, parse_qs
import requests
import os
import pyfiglet
from colorama import Fore, Style, init
from loguru import logger
import random
from time import sleep
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en,en-GB;q=0.9,en-US;q=0.8',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'webapp': 'true',
    'x-requested-with': 'org.telegram.messenger',
}
def genJwt(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.fragment)
    tgWebAppData = parse_qs(query_params.get('tgWebAppData')[0])
    auth_date = tgWebAppData.get('auth_date', [''])[0]
    query_id = tgWebAppData.get('query_id', [''])[0]
    user  = tgWebAppData.get('user', [''])[0]
    hash = tgWebAppData.get('hash', [''])[0]
    params = {
        'query_id': query_id,
        'user':f'{user}',
        'auth_date': auth_date,
        'hash': hash,
    }
    response = requests.get('https://fintopio-tg.fintopio.com/api/auth/telegram', params=params, headers=headers)
    return (response.json())

def doCN(jwt,key):
    while True:         
        data = {'jwt':jwt,'key':key}
        response = requests.get('http://77.37.63.209:4000/fin', json=data)
        logger.info(response.json())
        rest =random.randint(1,20)
        logger.debug(f'[sleeping for : {rest} sec]')
        sleep(rest)
        
    
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
    link = input("\nEnter your Fintopio session link : ")
    key = input("\nEnter your Authorization Key : ")
    doCN(genJwt(link)['token'],key)
