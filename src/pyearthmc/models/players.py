from pydantic import BaseModel

from pyearthmc.models.common import DefaultResponse, NamedEntity


class PlayerTimestamp(BaseModel):
    registered: int
    joinedTownAt: int | None = None
    lastOnline: int

class PlayerStats(BaseModel):
    balance: int
    numFriends: int

class PlayerStatus(BaseModel):
    isOnline: bool
    isNPC: bool
    isMayor: bool
    isKing: bool
    hasTown: bool
    hasNation: bool

class PlayerRanks(BaseModel):
    townRanks: list[str]
    nationRanks: list[str]

class Player(NamedEntity):
    title: str | None = None
    surname: str | None = None
    formatted_name: str | None = None
    about: str | None = None
    town: NamedEntity | None = None
    nation: NamedEntity | None = None
    timestamps: PlayerTimestamp
    status: PlayerStatus
    stats: PlayerStats
    ranks: PlayerRanks | None = None
    friends: list[NamedEntity]
    discord: int | None = None

class PlayerResponse(DefaultResponse):
    players: list[Player]
