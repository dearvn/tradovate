## Imports
from __future__ import annotations
import logging
from typing import TYPE_CHECKING

from .session import Session
from ..utils import urls
from ..utils.typing import AccountDict
if TYPE_CHECKING:
    from . import Profile

## Constants
log = logging.getLogger(__name__)


## Classes
class Account:
    """Tradovate Account"""

    # -Constructor
    def __init__(
        self, id_: int, profile_id: int, name: str,
        session: Session, endpoint: urls.ENDPOINT, *,
        nickname: str | None = None,  # loop: asyncio.AbstractEventLoop | None = None,
    ) -> Account:
        self.id: int = id_
        self.profile_id: int = profile_id
        self.name: str = name
        self.nickname: str | None = nickname
        self.endpoint: urls.ENDPOINT = endpoint
        #self._loop: asyncio.AbstractEventLoop = loop if loop else self._session.loop
        self._session: Session = session

    # -Dunder Methods
    def __repr__(self) -> str:
        str_ = f"Account(id={self.id}, name={self.name}, endpoint={self.endpoint.name}"
        str_ += f", nickname={self.nickname})" if self.nickname else ")"
        return str_

    # Class Methods
    @classmethod
    async def from_profile(
        cls, account: AccountDict, endpoint: urls.ENDPOINT, profile: Profile
    ) -> Account:
        '''Create account from Profile parameters'''
        log.debug(f"Getting account {account['id']}")
        return cls(
            account['id'], account['userId'], account['name'],
            profile.session, endpoint,
            nickname=account['nickname'] if 'nickname' in account else None,
        )
