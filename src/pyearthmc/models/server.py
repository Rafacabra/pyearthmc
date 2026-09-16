from pydantic import BaseModel
from pydantic.fields import computed_field

from pyearthmc.models.common import DefaultResponse


class ServerTimestamp(BaseModel):
    newDayTime: int
    serverTimeOfDay: int

class ServerStatus(BaseModel):
    hasStorm: bool
    isThundering: bool

class ServerStats(BaseModel):
    time: int
    fullTime: int
    maxPlayers: int
    numOnlinePlayers: int
    numOnlineNomads: int
    numResidents: int
    numNomads: int
    numTowns: int
    numTownBlocks: int
    numNations: int
    numQuarters: int
    numCuboids: int


    @computed_field
    @property
    def AvailablePlayerSlots(self) -> int:
        return self.maxPlayers - self.numOnlinePlayers

class VotepartyStatus(BaseModel):
    target: int
    numRemaining: int

    @computed_field
    def numVotes(self) -> int:
        return self.target - self.numRemaining


class ServerResponse(DefaultResponse):
    version: str
    moonPhase: str
    timestamps: ServerTimestamp
    status: ServerStatus
    stats: ServerStats
    voteParty: VotepartyStatus
