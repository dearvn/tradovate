## Imports
from typing import TypedDict


## Classes
class AccountDict(TypedDict, total=False):
    """Tradovate Account typed dictionary"""
    id: int
    userId: int
    name: str
    nickname: str
    accountType: str
    active: bool
    clearingHouseId: int
    riskCategoryId: int
    autoLiqProfileId: int
    marginAccountType: str
    legalStatus: str
    archived: bool
    timestamp: str
    approveForACH: bool


class MeAuthDict(TypedDict):
    """"""
    userId: int
    fullName: str
    email: str
    emailVerified: bool
    isTrial: bool


class CredentialAuthDict(TypedDict):
    """Credentials authorization typed dictionary"""
    name: str
    password: str
    deviceId: str
    cid: str
    sec: str
    appID: str
    appVersion: str


class OAuth2Dict(TypedDict):
    """OAuth2 authorization typed dictionary"""
    pass
