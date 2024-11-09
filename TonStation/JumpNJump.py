import requests
import json 
from urllib.parse import urlparse,  parse_qs
from random import randint
from time import sleep

query = input('Enter your Jump N Jump game session : ')
query_params = parse_qs(urlparse(query).fragment)
tgWebAppData = query_params.get('tgWebAppData', [None])[0]
id = str(json.loads(parse_qs(tgWebAppData)['user'][0])['id'])
name = str(json.loads(parse_qs(tgWebAppData)['user'][0])['first_name'])
params = {
        'id': id,
        'name': name,
        'initData':tgWebAppData,
    }
response = requests.get('https://api-jumper.sidusheroes.world/user', params=params)
acc = (response.json()['accessToken'])
json_data = {
        'id': str(id),
        'name': name,
        'accessToken':acc,
        'coins': randint(400,499),
        'jumps': randint(10,100),

    }
while True:
    response = requests.post('https://api-jumper.sidusheroes.world/end',  json=json_data)
    sleep(3)
    try :
        print(response.json()['user'])
    except Exception:
        print('No Tickets left')
        break
