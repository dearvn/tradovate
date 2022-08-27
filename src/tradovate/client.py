## Imports
from __future__ import annotations
import asyncio,redis,logging,json,os

from datetime import datetime,timedelta

from .auth import Profile
from .accounting import Accounting
from .auth.session import Session
from .stream.utils import urls
from .stream.utils.typing import CredentialAuthDict

## Constants
log = logging.getLogger(__name__)
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"),
            port=int(os.environ.get("REDIS_PORT", "6379")),
            decode_responses=True)


## Classes
class Client(Profile):
    """Tradovate Client"""

    # -Constructor
    def __init__(self) -> Client:
        self._loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        self._session: Session = Session(loop=self._loop)
        self._handle_auto_renewal: asyncio.TimerHandle | None = None

        accounting = Accounting(self._session)
        account = asyncio.run(accounting.account_list())

        self.id = account[0]['id']
        self.name = account[0]['name']

    @property
    def accounting(self) -> Accounting:
        return Accounting(self._session)

    def run(self, event, *args, **kwargs) -> None:
        '''Public client loop run method'''
        self._loop.run_until_complete(self._run(event, *args, **kwargs))
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            for task in asyncio.all_tasks(loop=self._loop):
                task.cancel()
            self._loop.run_until_complete(self.close())
            self._loop.close()

    async def _run(self, event, *args, **kwargs) -> None:
        self._dispatch(event=event, *args, **kwargs)

    # -Instance Methods: Private
    def _dispatch(self, event: str, *args, **kwargs) -> None:
        '''Dispatch task for event name'''
        log.debug(f"Client event '{event}'")

        method = event
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

    # -Instance Methods: Public
    async def authorize(
        self, auth: CredentialAuthDict, auto_renew: bool = True
    ) -> None:
        '''Initialize Client authorization and auto-renewal'''
        self.id = await self._session.request_access_token(auth)
        if auto_renew:
            self._loop.create_task(self._renewal(), name="client-renewal")

    async def authorizion_hold(self) -> None:
        '''Wait for all authentication setup to be finished'''
        await self._session.authenticated.wait()


    async def close(self) -> None:
        await self._session.close()


    async def process_message(self) -> None:
        '''Task for WebSocket loop'''
        print(">>>>>>>")


    # -Properties: Authenticated
    @property
    def authenticated(self) -> bool:
        if not self._session.authenticated.is_set():
            return False

        return True
