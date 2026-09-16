# Contributing to PyEMC

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. Please make sure to read
the relevant section before making your contribution. It will make it a lot
easier for us maintainers and smooth out the experience for all involved. The
community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's
> fine. There are other easy ways to support the project and show your
> appreciation, which we would also be very happy about:
> - Star the project
> - Refer this project in your project's readme
> - Tell your friends!

## Development setup

The project is managed with [uv](https://docs.astral.sh/uv/).

```bash
# Install the project and the dev toolchain (pytest, mypy, pyright, ruff, pyfiglet)
uv sync

# Run the automated, offline test suite
uv run pytest

# Run the interactive demos (needs a network connection)
uv run python examples/town_demo.py
```

## Project structure

- `src/pyearthmc/client.py`, `EmcClient`, the main public API.
- `src/pyearthmc/models/`, the Pydantic v2 data models, one module per endpoint.
- `tests/`, the automated, offline pytest suite (uses `httpx.MockTransport`).
- `examples/`, interactive demos that query the live EarthMC API.

## Conventions

- **Adding an endpoint.** Add the request/response methods on `EmcClient`
  prefixed with `get_`, and the corresponding models in
  `src/pyearthmc/models/`.
- **Pydantic v2.** All request/response data is a Pydantic v2 model. Never
  return raw dictionaries from the client.
- **Field names.** Mirror the raw EarthMC API exactly (camelCase, e.g.
  `isOnline`, `numTownBlocks`) so JSON maps 1:1 onto the models.
- **Request-based return types.** Methods return an overview (list of
  `NamedEntity`) when called with no arguments, and a full response when a
  request is passed. Use `@overload` on the request argument so callers get a
  precise return type. Keep the implementation signature (union return) and
  the overload stubs in sync.
- **Docstrings.** Every public method documents its args, return type, possible
  exceptions, and shows at least one example.
- **Type checking & linting.** Keep these green before submitting:

  ```bash
  uv run mypy src examples
  uv run pyright src tests examples
  uv run ruff check src tests examples
  uv run pytest
  ```

- **Tests.** Add or update offline tests in `tests/` for any new behavior. Avoid
  relying on the live API inside the test suite.

## Commit messages

Git commits should follow the [Conventional Commits](https://www.conventionalcommits.org/)
specification.
