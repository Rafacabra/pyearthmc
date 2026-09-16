from pydantic.main import BaseModel

from pyearthmc.models.common import (
    DefaultResponse,
    NamedEntity,
    SimpleTimestamp,
    WorldCoordinates,
)


class NationStats(BaseModel):
    numTownBlocks: int
    numResidents: int
    numTowns: int
    numAllies: int
    numEnemies: int
    balance: int

class NationStatus(BaseModel):
    isPublic: bool
    isOpen: bool
    isNeutral: bool

class NationCoordinates(BaseModel):
    spawn: WorldCoordinates

#There might be no ranks assigned in a nation.
class NationRanks(BaseModel):
    Chancellor: list[NamedEntity] | None = None
    Colonist: list[NamedEntity] | None = None
    Diplomat: list[NamedEntity] | None = None


class Nation(NamedEntity):
    board: str
    dynmapColour: str
    dynmapOutline: str
    wiki: str | None = None
    king: NamedEntity
    capital: NamedEntity
    timestamps: SimpleTimestamp
    status: NationStatus
    stats: NationStats
    coordinates: NationCoordinates
    residents: list[NamedEntity]
    towns: list[NamedEntity]
    allies: list[NamedEntity] | None = None
    enemies: list[NamedEntity] | None = None
    sanctions: list[NamedEntity] | None = None
    ranks: NationRanks

class NationResponse(DefaultResponse):
    nations: list[Nation]
