import requests
import hashlib
from urllib.parse import urlparse,  parse_qs
from time import sleep
from loguru import logger

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en',
    'authorization': 'Bearer false',
    'cache-control': 'no-cache',
    'origin': 'https://app.bums.bot',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://app.bums.bot/'
}
def compute_md5(amount ,seq):
    prefix = str(amount) + str(seq) + "7be2a16a82054ee58398c5edb7ac4a5a"
    return hashlib.md5(prefix.encode()).hexdigest() 

def genToken(initData):
    query_params = parse_qs(urlparse(initData).fragment)
    tgWebAppData = query_params.get('tgWebAppData', [None])[0]
    data = {
        'invitationCode':  '',
        'initData': tgWebAppData,
    }
    response = requests.post('https://api.bums.bot/miniapps/api/user/telegram_auth', headers=headers, data=data)
    return (response.json())
    
def mine_bums(cred):
    headers['authorization'] = 'Bearer ' +  cred['data']['token']
    data = ''
    #daily check in Api call
    #response = requests.post('https://api.bums.bot/miniapps/api/sign/sign', headers=headers, data=data)
    data = {'count':  '1', 'propId':  '500010001'}
    #spin APi call
    response = requests.post('https://api.bums.bot/miniapps/api/game_spin/Start', headers=headers, data=data)
    params = {'blumInvitationCode': ''}
    response = requests.get('https://api.bums.bot/miniapps/api/user_game_level/getGameInfo', params=params, headers=headers)
    Seq = response.json()['data']['tapInfo']['collectInfo']['collectSeqNo']
    hsh = compute_md5('10000000000000000',Seq)
    params = {
        'collectAmount':'10000000000000000' ,
        'hashCode': hsh,
        'collectSeqNo': str(Seq),
    }
    response = requests.post('https://api.bums.bot/miniapps/api/user_game/collectCoin', headers=headers,data=params)
    logger.info(response.json())
    
if __name__ == '__main__':  
    query = input('Enter your Bums  session link : ')
    re = genToken(query)
    while True:    
        mine_bums(re)
        sleep(1)
