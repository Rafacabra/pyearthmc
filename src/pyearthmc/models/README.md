# Models

This directory contains the **Pydantic v2 data models** used by PyEMC.

They define the structure of the data exchanged between the client and the
EarthMC API. Every request and response in the library is handled through these
models, providing validation, serialization, autocompletion, and type checking.

Because everything is a typed model, you get IDE autocompletion and static
type-checking out of the box, you don't need to re-check the raw API docs for
every field.

## Files

| File | Contents |
| --- | --- |
| `common.py` | Shared building blocks used by all endpoints |
| `server.py` | `ServerResponse` and its nested server/status/stats/vote-party models |
| `towns.py` | `Town`, `TownResponse` and town-specific models |
| `nations.py` | `Nation`, `NationResponse` and nation-specific models |
| `players.py` | `Player`, `PlayerResponse` and player-specific models |

## Shared primitives (`common.py`)

- `RequestMode`, `Literal["overview", "detailed"]`, controls the request method
  and the shape of the response.
- `NamedRequest`, the `detailed` request body: `query: list[str]` of names or
  UUIDs to look up.
- `NamedEntity`, the minimal `{name, uuid}` pair returned by `overview` mode and
  used to reference related entities (mayor, nation, residents, etc.).
- `UnnamedEntity`, an entity identified by `uuid` only.
- `Metadata`, adds a computed `response_arrived` timestamp to every response.
- `DefaultResponse`, base for all typed detailed responses; carries `metadata`.

## Computed fields

Some fields are generated on top of the raw API response via
`@computed_field`. These add value without altering the underlying data:

- `Metadata.response_arrived`, a Unix timestamp recorded when the model was
  constructed, so you know how stale the data is.
- `VotepartyStatus.numVotes`, the current vote-party vote count, derived from
  `target - numRemaining`.

## Conventions

- Field names mirror the raw EarthMC API (camelCase, e.g. `isOnline`,
  `numTownBlocks`), so the JSON maps 1:1 onto the models.
- Optional fields that the API may omit are typed `Optional` / `None`.
- When a new endpoint is added, create a matching module here following the
  `server.py` / `towns.py` pattern and export its response via the client.
