## Imports
from __future__ import annotations
from typing import AsyncGenerator

import aiohttp

from .account import Account
from .session import Session
from ..utils.typing import CredentialAuthDict, MeAuthDict

from ..utils import urls


## Classes
class Profile:
    """Tradovate Profile"""

    # -Constructor
    def __init__(self, session: Session) -> Profile:
        self.id: int = 0
        self._session = session

    # -Instance Methods: Private
    async def _get_accounts(self) -> AsyncGenerator[Account, None]:
        '''Returns full list of accounts from live+demo endpoints'''
        async for account in self._get_accounts_by_endpoint(urls.ENDPOINT.LIVE):
            yield account
        async for account in self._get_accounts_by_endpoint(urls.ENDPOINT.DEMO):
            yield account

    async def _get_accounts_by_endpoint(
        self, endpoint: urls.ENDPOINT
    ) -> AsyncGenerator[Account, None]:
        '''Returns full list of accounts from given endpoint'''
        for account in await self._session.get(urls.get_accounts(endpoint)):
            yield await Account.from_profile(account, endpoint, self)

    async def _get_account_by_id(
        self, ids: int | list[int]
    ) -> Account | tuple[Account]:
        '''Returns Account or list of Accounts from ID or IDs'''
        accounts = []
        for endpoint in [urls.ENDPOINT.LIVE, urls.ENDPOINT.DEMO]:
            # -URL handling
            if isinstance(ids, int):
                url = urls.get_account(endpoint, ids)
            else:
                url = urls.get_accounts(endpoint, ids)
            # -Account handling
            try:
                result = await self._session.get(url)
            except aiohttp.ClientResponseError:
                result = None
            # -Result Handling
            if result:
                if isinstance(ids, int):
                    return await Account.from_profile(result, endpoint, self)
                for account in result:
                    accounts.append(await Account.from_profile(account, endpoint, self))
        if accounts:
            return tuple(accounts)
        return None

    # -Instance Methods: Public
    async def authorize(self, authorization: CredentialAuthDict) -> bool:
        '''Initialize Profile authorization'''
        self.id = await self._session.request_access_token(authorization)
        return self.authenticated

    async def get_account(
        self, *, id_: int | None = None,
        name: str | None = None, nickname: str | None = None
    ) -> Account | None:
        '''Get account by id, name, or nickname'''
        if id_ is not None:
            return await self._get_account_by_id(id_)
        async for account in self._get_accounts():
            if account.name == name:
                return account
            elif account.nickname and account.nickname == nickname:
                return account
        return None

    async def get_accounts(
        self, *, ids: list[int] | None = None,
        names: list[str] | None = None, nicknames: list[str] | None = None
    ) -> tuple[Account] | None:
        '''Get accounts by ids, names, or nicknames or full account list'''
        # -TODO: Async Generator?
        if ids:
            return await self._get_account_by_id(ids)
        elif names or nicknames:
            accounts = []
            async for account in self._get_accounts():
                if names and account.name in names:
                    accounts.append(account)
                elif nicknames and account.nickname and account.nickname in nicknames:
                    accounts.append(account)
            if accounts:
                return tuple(accounts)
            return None
        else:
            return tuple([account async for account in self._get_accounts()])

    async def me(self) -> MeAuthDict:
        '''Profile details'''
        return await self._session.get(urls.http_auth_me)

    # -Property
    @property
    def authenticated(self) -> bool:
        return self._session.authenticated.is_set()

    @property
    def session(self) -> Session:
        return self._session
