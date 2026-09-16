
from pydantic import BaseModel
from pydantic.fields import computed_field

from pyearthmc.models.common import (
    DefaultResponse,
    NamedEntity,
    UnnamedCoordinates,
    UnnamedEntity,
    WorldCoordinates,
)


class TownTimestamp(BaseModel):
    registered: int
    joinedNationAt: int | None = None
    ruinedAt: int | None = None

class TownStats(BaseModel):
    numTownBlocks: int
    maxTownBlocks: int
    numResidents: int
    numTrusted: int
    numOutlaws: int
    balance: int
    forSalePrice: int | None


    @computed_field
    @property
    def claimableTownBlocks(self) -> int:
        return self.maxTownBlocks - self.numTownBlocks

    @computed_field
    @property
    def townBlocksWorth(self) -> int:
        return self.numTownBlocks*16

    @computed_field
    @property
    def balanceToPriceRatio(self) -> int | None:
        return self.balance - self.forSalePrice if self.forSalePrice is not None else None

    @computed_field
    @property
    def totalWorth(self) -> int:
        return self.balance + self.townBlocksWorth

    @computed_field
    @property
    def worthToPriceRatio(self) -> int | None:
        return self.totalWorth - self.forSalePrice if self.forSalePrice is not None else None




class TownStatus(BaseModel):
    isPublic: bool
    isOpen: bool
    isNeutral: bool
    isCapital: bool
    isOverclaimed: bool | None = None
    isRuined: bool
    isForSale: bool
    hasNation: bool
    hasOverclaimShield: bool | None = None
    canOutsiderSpawn: bool | None = None


class TownRanks(BaseModel):
    Councilor: list[NamedEntity] | None = None
    Builder: list[NamedEntity] | None = None
    Recruiter: list[NamedEntity] | None = None
    Police: list[NamedEntity] | None = None
    Tax_exempt: list[NamedEntity] | None = None
    Treasurer: list[NamedEntity] | None = None
    Realtor: list[NamedEntity] | None = None
    Settler: list[NamedEntity] | None = None

class TownCoordinates(BaseModel):
    spawn: WorldCoordinates
    homeBlock: UnnamedCoordinates
    townBlocks: list[UnnamedCoordinates]


class Town(NamedEntity):
    board: str
    founder: str
    wiki: str | None = None
    mayor: NamedEntity
    nation: NamedEntity
    timestamps: TownTimestamp
    status: TownStatus
    stats: TownStats
    coordinates: TownCoordinates
    residents: list[NamedEntity]
    trusted: list[NamedEntity] | None = None

    outlaws: list[NamedEntity] | None = None
    quarters: list[UnnamedEntity] | None = None
    ranks: TownRanks




class TownResponse(DefaultResponse):
    towns: list[Town]
