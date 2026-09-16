from pydantic import BaseModel

from pyearthmc.models.common import NamedEntity


class OnlinePlayersResponse(BaseModel):
    count: int
    players: list[NamedEntity]
