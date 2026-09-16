```
 ____           ____             ____      
/\  _`\        /\  _`\   /'\_/`\/\  _`\    
\ \ \L\ \__  __\ \ \L\_\/\      \ \ \/\_\  
 \ \ ,__/\ \/\ \\ \  _\L\ \ \__\ \ \ \/_/_ 
  \ \ \/\ \ \_\ \\ \ \L\ \ \ \_/\ \ \ \L\ \
   \ \_\ \/`____ \\ \____/\ \_\\ \_\ \____/
    \/_/  `/___/> \\/___/  \/_/ \/_/\/___/ 
             /\___/                        
             \/__/                         
```

# PyEMC

A complete Python client for the [EarthMC](https://earthmc.net/)
Minecraft server API.

PyEMC models the raw EarthMC JSON endpoints as validated [Pydantic v2](https://docs.pydantic.dev/)
objects and wraps them behind an async HTTP client. You get autocompletion,
type checking, and data validation out of the box.

## Features

- **Type-safe:** Every request and response is a Pydantic v2 model. Typos and
  malformed payloads fail fast instead of silently breaking later.
- **Async:** Built on `httpx.AsyncClient` for concurrent requests with automatic
  retries.
- **Flexible queries:** Call `get_towns()` with no arguments for a light overview,
  or pass a name, UUID, or list of names for full entity data.
- **Computed fields:** Extra data is generated on top of the raw API response
  (e.g. when the response arrived, the current vote-party vote count, or
  available player slots).

## Requirements

- Python **3.14+**
- An internet connection to reach `https://api.earthmc.net`

## Installation

```bash
pip install pyearthmc
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add pyearthmc
```

## Quickstart

```python
import asyncio

from pyearthmc import EmcClient


async def main():
    emc = EmcClient()

    server = await emc.get_server_info()
    print(server.version)
    print(server.voteParty.numVotes)


if __name__ == "__main__":
    asyncio.run(main())
```

## Usage

### Overview (no arguments)

Calling `get_*()` with no arguments returns a plain list of `NamedEntity`
(`name` and `uuid`).

```python
towns = await emc.get_towns()
nations = await emc.get_nations()
players = await emc.get_players()
```

### Detailed queries

Pass a name, UUID, list of names, or a `NamedRequest` to get full entity data.

```python
town = await emc.get_towns("Colombia")
print(town.towns[0].mayor.name)

player = await emc.get_players("RafaCabra")
print(player.players[0].status.isOnline)

# Multiple names at once
nations = await emc.get_nations(["Amazon", "Colombia"])
```

> **Note:** When no request is provided the method performs a lightweight `GET`
> returning name/UUID pairs. When a request is provided it performs a `POST`
> returning the full entity payload.

## Contributing

Contributions are welcome! See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for
development setup and conventions.

## License

[MIT](./LICENSE)
