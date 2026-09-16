# Tests

This directory contains the **automated, offline test suite** for PyEMC.

Unlike the interactive examples in [`examples/`](../examples), these tests do not
hit the live EarthMC API, they mock HTTP responses with `httpx.MockTransport`,
so they run anywhere with no network access and do not require user input.

## Running the tests

```bash
uv run pytest
```

## What is tested

- `test_client.py`, the `EmcClient` public API:
  - `get_server_info()` returns a validated `ServerResponse`.
  - The `overview` / `detailed` modes for towns, nations and players.
  - Computed fields such as `VotepartyStatus.numVotes`.
  - Error handling: `ValueError` when a `detailed` request is missing its
    request body, and `HTTPStatusError` for non-200 responses.
- `test_models.py`, validation and computed fields of the Pydantic models.

Run a single file with `uv run pytest tests/test_client.py`.
