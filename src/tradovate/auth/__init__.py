import os

import requests

def access_token():
    url = "https://demo.tradovateapi.com/v1/auth/accesstokenrequest"
    if os.getenv('TO_ENV') == 'LIVE':
        url = "https://live.tradovateapi.com/v1/auth/accesstokenrequest"
    resp = requests.post(
        url,
        data={
            "name": os.getenv('TO_NAME'),
            "password": os.getenv('TO_PASSWORD'),
            "appId": os.getenv('TO_APPID'),
            "appVersion": "1.0",
            "cid": os.getenv('TO_CID'),
            "sec": os.getenv('TO_SEC')
        },
    )
    if resp.status_code != 200:
        raise Exception("Could not authenticate!")
    return resp.json()
