from urllib.parse import urlparse, parse_qs
import requests
import os
import pyfiglet
from colorama import Fore, Style, init
from loguru import logger

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'authorization': 'Bearer ',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://play.tap.chaingpt.org',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://play.tap.chaingpt.org/',
    'x-requested-with': 'org.telegram.plus',
}

def genJwt(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.fragment)
    tgWebAppData = parse_qs(query_params.get('tgWebAppData')[0])
    json_data = {
        'initData': tgWebAppData,
    }
    response = requests.post('https://tapapi.chaingpt.org/authenticate', headers=headers, json=json_data)
    return (response.json())


def doCN(jwt):
    headers['authorization'] = 'Bearer '+jwt
    while True:         
        json_data = {
            'points': 100000000000000000,
            'taps': 100000000000000000,
            'isTurboMode': True,
        }
        response = requests.post('https://tapapi.chaingpt.org/tap', headers=headers, json=json_data)
        logger.info(response.text)
        
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
        color = colors[i % len(colors)]
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
    link = input("\nEnter your ChainGpt session link : ")
    doCN(genJwt(link)['accessToken'])
