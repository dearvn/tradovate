## Imports
from __future__ import annotations
import asyncio,os,requests,json,logging
from asyncio import AbstractEventLoop
from datetime import datetime, timedelta, timezone

import aiohttp
from aiohttp import ClientWebSocketResponse as ClientWebSocket

from ..utils import timestamp_to_datetime, urls
from ..utils.errors import (
    LoginInvalidException, LoginCaptchaException,
    WebSocketOpenException, WebSocketAuthorizationException,
    WebSocketClosedException
)
from ..utils.typing import CredentialAuthDict

## Constants
log = logging.getLogger(__name__)


## Classes
class Session:
    """Tradovate Session"""

    # -Constructor
    def __init__(self, *, loop: AbstractEventLoop | None = None) -> Session:
        self.authenticated: asyncio.Event = asyncio.Event()
        self.token_expiration: datetime | None = None
        self._aiosession: aiohttp.ClientSession | None = None
        self._loop: AbstractEventLoop = loop if loop else asyncio.get_event_loop()
        self._loop.create_task(self.__ainit__(), name="session-init")

    # -Dunder Methods
    async def __ainit__(self) -> None:
        self._aiosession = aiohttp.ClientSession(loop=self._loop, raise_for_status=True)

    def __repr__(self) -> str:
        str_ = f"Session(authenticated={self.authenticated.is_set()}"
        if self.authenticated.is_set():
            str_ += f", duration={self.token_duration}"
        return str_ + ")"

    # -Instance Methods: Private
    async def _update_authorization(
        self, res: aiohttp.ClientResponse
    ) -> dict[str, str]:
        '''Updates Session authorization fields'''
        res_dict = await res.json()

        #print(">>>>>>>>>>>+++++", res_dict)

        # -Invalid Credentials
        if 'errorText' in res_dict:
            self.authenticated.clear()
            raise LoginInvalidException(res_dict['errorText'])
        # -Captcha Limiting
        if 'p-ticket' in res_dict:
            self.authenticated.clear()
            raise LoginCaptchaException(
                res_dict['p-ticket'], int(res_dict['p-time']),
                bool(res_dict['p-captcha'])
            )
        # -Access Token
        log.debug("Session event 'authorized'")
        self.authenticated.set()
        self.token_expiration = timestamp_to_datetime(res_dict['expirationTime'])
        self._aiosession.headers.update({
            'AUTHORIZATION': "Bearer " + res_dict['accessToken']
        })
        return res_dict

    # -Instance Methods: Public
    async def close(self) -> None:
        await self._aiosession.close()
        self.authenticated.clear()

    async def create_websocket(self, url: str, *args, **kwargs) -> ClientWebSocket:
        '''Return an aiohttp WebSocket'''
        return await self._aiosession.ws_connect(url, *args, **kwargs)

    async def get(self, url, *args, **kwargs) -> dict[str, str]:
        res = await self._aiosession.request('GET', url, *args, **kwargs)
        return await res.json()

    async def renew_access_token(self) -> None:
        '''Renew Session authorization'''
        log.debug("Session event 'renew'")
        res = await self._aiosession.post(urls.http_auth_renew)
        await self._update_authorization(res)

    async def request_access_token(
        self, auth: CredentialAuthDict, *,
        account_websockets: tuple[WebSocket] | None = None,
        market_websockets: tuple[WebSocket] | None = None,
    ) -> int:
        '''Request Session authorization'''
        log.debug("Session event 'request'")
        #print("Session event 'request'>>>>>>>>>>>>>>>>>", urls.http_auth_request)
        res = await self._aiosession.post(urls.http_auth_request, json=auth)
        res_dict = await self._update_authorization(res)

        if account_websockets:
            for account_websocket in account_websockets:
                await account_websocket.authorize(res_dict['accessToken'])
        if market_websockets:
            for market_websocket in market_websockets:
                await market_websocket.authorize(res_dict['mdAccessToken'])
        return res_dict['userId']

    # -Property
    @property
    def loop(self) -> AbstractEventLoop:
        return self._loop

    @property
    def token_duration(self) -> timedelta:
        return self.token_expiration - datetime.now(timezone.utc)

    @property
    def token_expired(self) -> bool:
        return datetime.now(timezone.utc) >= self.token_expiration


class WebSocket:
    """Tradovate WebSocket"""

    # -Constructor
    def __init__(
        self, url: str, websocket: ClientWebSocket, *,
        loop: AbstractEventLoop | None = None
    ) -> WebSocket:
        self.id: int = WebSocket.id
        WebSocket.id += 1
        self.url: str = url
        self.connected: asyncio.Event = asyncio.Event()
        self.authenticated: asyncio.Event = asyncio.Event()
        self._request: int = 0
        self._aiowebsocket: ClientWebSocket = websocket
        self._loop: AbstractEventLoop = loop if loop else asyncio.get_event_loop()
        self._loop.create_task(self.__ainit__(), name=f"websocket[{self.id}]-init")

    # -Dunder Methods
    async def __ainit__(self) -> None:
        if await self._aiowebsocket.receive_str() != 'o':
            raise WebSocketOpenException(self.url)
        self.connected.set()
        self._loop.create_task(
            self._heartbeat(), name=f"websocket[{self.id}]-heartbeat"
        )

    def __repr__(self) -> str:
        return (
            f"WebSocket(url={self.url}, connected={self.connected.is_set()},"
            f"authenticated={self.authenticated.is_set()})"
        )

    # -Instance Methods: Private
    async def _heartbeat(self) -> None:
        '''Send heartbeat packet to aiowebsocket'''
        while self.connected.is_set():
            await asyncio.sleep(2.5)
            await self._aiowebsocket.send_str("[]")

    async def _socket_send(self, url: str, query: str = "", body: str = "") -> None:
        '''Send formatted request string to aiowebsocket'''
        req = f"{url}\n{self._request}\n{query}\n{body}"
        self._request += 1
        await self._aiowebsocket.send_str(req)

    # -Instance Methods: Public
    async def authorize(self, token: str) -> None:
        '''Request WebSocket authorization'''
        await self._socket_send(urls.wss_auth, body=token)
        res = (await self.poll_message())
        if res == None:
            raise WebSocketAuthorizationException(self.url, token)
        ws_res = res[0]
        if not ws_res or ws_res['s'] != 200:
            raise WebSocketAuthorizationException(self.url, token)
        self.authenticated.set()

    async def close(self) -> None:
        if self.connected.is_set():
            await self._aiowebsocket.close()
        self.connected.clear()
        self.authenticated.clear()

    async def poll_message(self, ticker = None, interval = None) -> None:
        '''Recieve dictionary object or None from aiowebsocket'''
        ws_res = await self._aiowebsocket.receive()
        #print("*****************************************>>",len(ws_res.data), "<<*****************************************")
        if not ws_res or not ws_res.data or isinstance(ws_res.data, int):
            return None
        init_ = ws_res.data[0]
        if init_ == 'a':
            return json.loads(ws_res.data[1:])
        elif init_ == 'c':
            raise WebSocketClosedException(self.url)
        return None

    async def request(
        self, url: str, *, body: dict[str, str] | None = None, **kwargs
    ) -> None:
        '''Send a formatted request to aiowebsocket'''
        log.debug(f"WebSocket[{self.id}] event '{url}'")
        if kwargs:
            fields = []
            for key, val in kwargs.items():
                if isinstance(val, list):
                    val = ','.join(str(i) for i in val)
                fields.append(f"{key}={val}")
            query = '&'.join(fields)
        else:
            query = ""
        body = json.dumps(body) if body else ""
        await self._socket_send(url, query, body)

    # -Class Methods
    @classmethod
    async def from_session(
        cls, url: str, session: Session, *,
        loop: AbstractEventLoop | None = None
    ) -> WebSocket:
        '''Create WebSocket from Session'''
        loop = loop if loop else session.loop
        websocket = await session.create_websocket(url)
        return cls(
            url, websocket, loop=loop
        )

    # -Class Properties
    id: int = 0
