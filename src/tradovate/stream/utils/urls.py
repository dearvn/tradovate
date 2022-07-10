## Imports
from __future__ import annotations
from enum import Enum
import os

## Constants
# -Base URLs
_domains = (
    "://live.tradovateapi.com/v1/",     # -Live Account Functionality
    "://demo.tradovateapi.com/v1/",     # -Demo Account Functionality
    "://md.tradovateapi.com/v1/",       # -Live Market Functionality
    #"://md-demo.tradovateapi.com/v1/",  # -Demo Market Functionality [?]
    #"://replay.tradovateapi.com/v1",    # -Replay Market Functionality
)
http_base_live, http_base_demo, http_base_market = [
    f"https{domain}" for domain in _domains
]
wss_base_live, wss_base_demo, wss_base_market = [
    f"wss{domain}websocket" for domain in _domains
]
# -Authorization
#  -HTTP[Live Only]
http_base_auth = http_base_live + "auth/" if os.getenv('TO_ENV') == 'LIVE' else http_base_demo + "auth/"
http_auth_oauth = http_base_auth + "oauthtoken"
http_auth_request = http_base_auth + "accesstokenrequest"
http_auth_renew = http_base_auth + "renewaccesstoken"
http_auth_me = http_base_auth + "me"
#  -Websocket
wss_auth = "authorize"
# -User
wss_user_sync = "user/syncrequest"
# -Market
wss_market_sub = "md/subscribeQuote"
wss_market_usub = "md/unsubscribeQuote"
wss_market_dom_sub = "md/subscribeDOM"
wss_market_dom_usub = "md/unsubscribeDOM"
wss_market_histogram_sub = "md/subscribeHistogram"
wss_market_histogram_usub = "md/unsubscribeHistogram"
wss_market_chart_sub = "md/getChart"
wss_market_chart_usub = "md/cancelChart"


## Functions
# -Account
def get_account(endpoint: ENDPOINT, id_: int) -> str:
    """URL Endpoint for getting single account"""
    url = "account/item"
    if endpoint == ENDPOINT.WEBSOCKET:
        return url
    return endpoint.value + url + f"/?id={id_}"


def get_accounts(
    endpoint: ENDPOINT, ids: list[int] | None = None
) -> str:
    """URL Endpoint for getting multiple accounts - by id or full list"""
    url = "account/items" if ids else "account/list"
    if endpoint == ENDPOINT.WEBSOCKET:
        return url
    url += "/?ids=" + ','.join(str(i) for i in ids) if ids else ""
    return endpoint.value + url


## Classes
class ENDPOINT(Enum):
    """URL Endpoint Enum"""
    LIVE = http_base_live
    DEMO = http_base_demo
    WEBSOCKET = None
