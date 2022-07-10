## Imports
from __future__ import annotations
import asyncio
import logging
from datetime import timedelta

from .profile import Profile
from .profile.session import Session, WebSocket
from .utils import urls
from .utils.typing import CredentialAuthDict

## Constants
log = logging.getLogger(__name__)


## Classes
class Client(Profile):
    """Tradovate Client"""

    # -Constructor
    def __init__(self) -> Client:
        self.id: int = 0
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._session: Session = Session(loop=self._loop)
        self._handle_auto_renewal: asyncio.TimerHandle | None = None
        self._live: WebSocket | None = None
        self._demo: WebSocket | None = None
        self._mdlive: WebSocket | None = None
        self._mddemo: WebSocket | None = None
        self._mdreplay: WebSocket | None = None

    # -Instance Methods: Private
    def _dispatch(self, event: str, *args, **kwargs) -> None:
        '''Dispatch task for event name'''
        log.debug(f"Client event '{event}'")

        print("===========>>>>>>>>>>>",event)

        method = "on_" + event
        try:
            coro = getattr(self, method)
        except AttributeError:
            pass
        else:
            self._loop.create_task(coro(*args, **kwargs))

    async def _renewal(self) -> None:
        '''Task for Session authorization renewal loop'''
        while self._session.authenticated.is_set():
            time = self._session.token_duration - timedelta(minutes=10)
            await asyncio.sleep(time.total_seconds())
            await self._session.renew_access_token()

    async def _run(
        self, auth: CredentialAuthDict, auto_renew: bool,
        live: bool, demo: bool, mdlive: bool
    ) -> None:
        '''Private client loop run method'''
        await self.create_websockets(live, demo, mdlive)
        await self.authorize(auth, auto_renew)
        await self.authorizion_hold()
        await self.sync_websockets()
        for websocket in self._websockets:
            self._loop.create_task(self.process_message(websocket))

        self._dispatch('connect')

    # -Instance Methods: Public
    async def authorize(
        self, auth: CredentialAuthDict, auto_renew: bool = True
    ) -> None:
        '''Initialize Client authorization and auto-renewal'''
        self.id = await self._session.request_access_token(
            auth, account_websockets=self._websockets_account,
            market_websockets=self._websockets_market
        )
        if auto_renew:
            self._loop.create_task(self._renewal(), name="client-renewal")

    async def authorizion_hold(self) -> None:
        '''Wait for all authentication setup to be finished'''
        await self._session.authenticated.wait()
        for websocket in self._websockets:
            await websocket.authenticated.wait()

    async def close(self) -> None:
        for websocket in self._websockets:
            await websocket.close()
        await self._session.close()

    async def create_websockets(self, live: bool, demo: bool, mdlive: bool) -> None:
        '''Initialize Client WebSockets'''
        self._live = (
            await WebSocket.from_session(urls.wss_base_live, self._session)
            if live else None
        )
        self._demo = (
            await WebSocket.from_session(urls.wss_base_demo, self._session)
            if demo else None
        )
        self._mdlive = (
            await WebSocket.from_session(urls.wss_base_market, self._session)
            if mdlive else None
        )

    async def process_message(self, websocket: WebSocket) -> None:
        '''Task for WebSocket loop'''
        while websocket.connected.is_set():
            msgs = (await websocket.poll_message())
            if not msgs:
                continue
            msg = msgs[0]
            if not msg:
                continue
            print("********************",msg)

    def run(
        self, auth: CredentialAuthDict, *, auto_renew: bool = True,
        live_websocket: bool = False, demo_websocket: bool = False,
        mdlive_websocket: bool = False
    ) -> None:
        '''Public client loop run method'''
        self._loop.run_until_complete(self._run(
            auth, auto_renew, live_websocket,
            demo_websocket, mdlive_websocket
        ))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            for task in asyncio.all_tasks(loop=self._loop):
                task.cancel()
            self._loop.run_until_complete(self.close())
            self._loop.close()

    async def subscribe_symbol(
        self, id_: int | str, *, dom: bool = True, histogram: bool = True
    ) -> None:
        '''Add symbol to market subscription'''
        if not self._mdlive:
            return None
        # -Market
        await self._mdlive.request(urls.wss_market_sub, body={"symbol": id_})
        # -DOM
        if not dom:
            return None
        await self._mdlive.request(urls.wss_market_dom_sub, body={"symbol": id_})
        # -Histogram
        if not histogram:
            return None
        await self._mdlive.request(urls.wss_market_histogram_sub, body={"symbol": id_})

    async def sync_websockets(self) -> None:
        for websocket in self._websockets_account:
            await websocket.request(urls.wss_user_sync, body={'users': [self.id]})

    async def unsubscribe_symbol(self, id_: int | str) -> None:
        '''Remove symbol from market subscription'''
        await self._mdlive.request(urls.wss_market_usub, body={"symbol": id_})
        await self._mdlive.request(urls.wss_market_dom_usub, body={"symbol": id_})
        await self._mdlive.request(urls.wss_market_histogram_usub, body={"symbol": id_})

    # -Properties: Private
    @property
    def _websockets(self) -> tuple[WebSocket]:
        websockets = []
        if self._live:
            websockets.append(self._live)
        if self._demo:
            websockets.append(self._demo)
        if self._mdlive:
            websockets.append(self._mdlive)
        if self._mddemo:
            websockets.append(self._mddemo)
        if self._mdreplay:
            websockets.append(self._mdreplay)
        if websockets:
            return tuple(websockets)
        return None

    @property
    def _websockets_account(self) -> tuple[WebSocket]:
        websockets = []
        if self._live:
            websockets.append(self._live)
        if self._demo:
            websockets.append(self._demo)
        if websockets:
            return tuple(websockets)
        return None

    @property
    def _websockets_market(self) -> tuple[WebSocket]:
        websockets = []
        if self._mdlive:
            websockets.append(self._mdlive)
        if self._mddemo:
            websockets.append(self._mddemo)
        if self._mdreplay:
            websockets.append(self._mdreplay)
        if websockets:
            return tuple(websockets)
        return None

    # -Properties: Authenticated
    @property
    def authenticated(self) -> bool:
        if not self._session.authenticated.is_set():
            return False
        for websocket in self._websockets:
            if not websocket.authenticated.is_set():
                return False
        return True
