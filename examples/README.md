# Examples

This directory contains **interactive demo scripts** that query the live EarthMC
API. 

## Requirements

The demos use `pyfiglet` to print an ASCII banner, so make sure it is installed:

```bash
uv sync --group dev
```

## Running a demo

Each script asks for a name and prints the corresponding live data:

```bash
uv run python examples/server_demo.py   # server overview + vote-party status
uv run python examples/town_demo.py     # all towns, then details for a town
uv run python examples/nation_demo.py   # all nations, then details for a nation
uv run python examples/player_demo.py   # all players, then details for a player
```

For the town/nation/player demos you will be prompted to enter a name. The
`detailed` request accepts either a name or a UUID.

## What each demo shows

| Script | Endpoint(s) | Highlights |
| --- | --- | --- |
| `server_demo.py` | `GET /v4/` | Server version, moon phase, stats, vote-party |
| `town_demo.py` | `GET /v4/towns` + `POST` | Residents list, board, founder |
| `nation_demo.py` | `GET /v4/nations` + `POST` | Residents list, board, king |
| `player_demo.py` | `GET /v4/players` + `POST` | Online status, town/nation, ranks, friends |

Run them from the repository root so `src/` is on the path (uv handles this automatically).
