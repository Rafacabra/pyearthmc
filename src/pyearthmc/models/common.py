
import datetime
from typing import Literal

from pydantic import BaseModel, computed_field
from rich import print

RequestMode = Literal['overview', 'detailed']
type UnnamedCoordinates = tuple[int, int]

# Metadata field to add information about the responses.
class Metadata(BaseModel):
    @computed_field
    def entityTimestamp(self) -> int:
        return int(datetime.datetime.now(datetime.UTC).timestamp())

# The default response is a pydantic model with metadata and the show function
# All responses are derived from this class.
class DefaultResponse(BaseModel):
    metadata: Metadata = Metadata()

    def show(self):
        print(self)

class NamedRequest(BaseModel):
    # I absolutely hate doing this without type safety,
    # but the API expects a list of strings and I don't want to write a custom validator
    # Let me know if you have a better solution.
    query: list[str]


class SimpleTimestamp(BaseModel):
    registered: int

class NamedEntity(BaseModel):
    name: str
    uuid: str


class UnnamedEntity(BaseModel):
    uuid: str

class SimpleCoordinates(BaseModel):
    x: float
    z: float

class WorldCoordinates(SimpleCoordinates):
    world: str
    y: int
    pitch: float
    yaw: float


# Responses that only include names or uuid or both.
# Usually they are GET requests.
class NamedResponse(NamedEntity):
    metadata: Metadata = Metadata()

class UnnamedResponse(UnnamedEntity):
    metadata: Metadata = Metadata()
