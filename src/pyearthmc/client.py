
from typing import overload

import httpx
from rich.progress import track

from pyearthmc.models.common import NamedEntity, NamedRequest, RequestMode
from pyearthmc.models.nations import Nation, NationResponse
from pyearthmc.models.players import Player, PlayerResponse
from pyearthmc.models.server import ServerResponse
from pyearthmc.models.towns import Town, TownResponse


class EmcClient:
    """
    Main client for interacting with the EarthMC API.
    It coordinates requests and responses.
    All the requests begin with `get_` and return a response model.
    Every single request and response is handled via pydantic models
    providing type safety and validation. Feel free to check the docs for each function
    and the models to know exactly what each response contains.

    Args:
        client (httpx.AsyncClient | None): An optional async HTTP client.
            When omitted, a client with automatic retries is created internally.

    Examples:
        ```python
            emc_client = EmcClient()
        ```

    Notes:
        The client is created internally with retries when not provided.
        If you want to manage your own lifecycle, pass your own `httpx.AsyncClient`.

        As always, contributions will be appreciated, even if only to improve the documentation.
    """


    def __init__(self, client: httpx.AsyncClient | None = None):
        # Check if tke player provided a client.
        # If he didn't, create one.

        if client is None:
            transport = httpx.AsyncHTTPTransport(retries=3)
            client = httpx.AsyncClient(transport=transport)

        self.client: httpx.AsyncClient = client

    async def get_server_info(self) -> ServerResponse:
        """
        Examples:
            ```python
                emc_client = EmcClient()
                server_info = await emc_client.get_server_info()
                server_info.show()
            ```

        Get the core server information.
        It includes the server version, moon phase, timestamps, status, stats and voteparty status.
        Check the API documentation for more details.

        Args:
            None

        Note:
            Replaces a GET request to https://api.earthmc.net/v4/

        Returns:
            ServerResponse: The server information including voteparty status, version and others.
        """
        #Just a GET request
        response = await self.client.get("https://api.earthmc.net/v4/")

        #Raise on status code
        if response.status_code != 200:
            raise httpx.HTTPStatusError(f"Unexpected status code: {response.status_code, response.text}", request=response.request, response=response)

        # Return the response validated as a ServerResponse
        return ServerResponse.model_validate(response.json())

    # If no input, it returns a list of named entities (name and uuid)
    @overload
    async def get_towns(self) -> list[NamedEntity]: ...

    # If it receives a town, output a full town response (POST)
    @overload
    async def get_towns(self, town_request: list[str] | str ) -> TownResponse: ...

    async def get_towns(self, town_request: list[str] | str | None = None) -> list[NamedEntity] | TownResponse:  # type: ignore[misc]
        """
        Get information about towns in the server.
        If you want to query a specific town, provide the town request parameters.
        You can provide either the town name or UUID.

        Note:
            Calling without arguments performs a GET request to
            https://api.earthmc.net/v4/towns returning a name/UUID list.
            Passing a request performs a POST request to
            https://api.earthmc.net/v4/towns returning full town data.

        Args:
            town_request (list[str] | str | None):
                The town request parameters. Can be a single name or UUID or a list
                of names. When None, an overview is returned.

        Returns:
            list[NamedEntity] | TownResponse:
                It returns a list of NamedEntity when no request is provided,
                and a TownResponse when a request is provided.

        Raises:
            httpx.HTTPStatusError: If the request fails.

        Examples:
            ```python
                emc_client = EmcClient()
                towns = await emc_client.get_towns()
                print(towns)
            ```

            ```python
                emc_client = EmcClient()
                towns = await emc_client.get_towns("Colombia")
                towns.show()
            ```
        """
        # If no input provided should do a GET request
        if town_request is None:
            mode: RequestMode = 'overview'
            payload = None
            response = await self.client.get("https://api.earthmc.net/v4/towns")

        # Otherwise prepare the payload to match the API and send a POST request
        else:
            mode = "detailed"
            if isinstance(town_request, str):
                town_query = NamedRequest(query=[town_request])

            else:
                town_query = NamedRequest(query=town_request)

            payload = town_query.model_dump()
            response = await self.client.post("https://api.earthmc.net/v4/towns", json=payload)

        # Raise on status code
        if response.status_code != 200:
            raise httpx.HTTPStatusError(f"Unexpected status code: {response.status_code, response.text} to request {payload}",
                request=response.request, response=response)

        # Validate all the towns in the GET request are Named Entity
        if mode == "overview":
            overview_towns: list[NamedEntity] = [NamedEntity.model_validate(town) for town in track(response.json(),
                description="[green] Loading and validating town overviews... [/green]")]

            return overview_towns

        # Validate all the towns in the POST request are Towns
        elif mode == "detailed":
            detailed_towns: list[Town] = [Town.model_validate(town) for town in track(response.json(),
                description="[green] Loading and validating town details... [/green]")]

            return TownResponse(towns=detailed_towns)


    # If no input return a list of named entity (name and uuid)
    @overload
    async def get_nations(self) -> list[NamedEntity]: ...

    # Otherwise return a Nation Response
    @overload
    async def get_nations(self, nation_request: str | list[str]) -> NationResponse: ...

    async def get_nations(self, nation_request: str | list[str] | None = None) -> list[NamedEntity] | NationResponse:  # type: ignore[misc]
        """
        Get information about nations in the server.
        If you want to query a specific nation, provide the nation request parameters.
        You can provide either the nation name or UUID.

        Note:
            Calling without arguments performs a GET request to
            https://api.earthmc.net/v4/nations returning a name/UUID list.
            Passing a request performs a POST request to
            https://api.earthmc.net/v4/nations returning full nation data.

        Args:
            nation_request (str | list[str] | None):
                The nation request parameters. Can be a single name, UUID or a
                list of names. When None, an overview is returned.

        Returns:
            list[NamedEntity] | NationResponse:
                It returns a list of NamedEntity when no request is provided,
                and a NationResponse when a request is provided.

        Raises:
            httpx.HTTPStatusError: If the request fails.

        Examples:
            ```python
                emc_client = EmcClient()
                nations = await emc_client.get_nations()
                print(nations)
            ```

            ```python
                emc_client = EmcClient()
                nations = await emc_client.get_nations("Amazon")
                nations.show()
            ```

        """
        # If no input perform a GET request
        if nation_request is None:
            mode: RequestMode = "overview"
            response = await self.client.get("https://api.earthmc.net/v3/nations")

        # Otherwise a POST request
        else:
            mode = "detailed"

            if isinstance(nation_request, str):
                nation_query = NamedRequest(query=[nation_request])

            else:
                nation_query = NamedRequest(query=nation_request)

            payload = nation_query.model_dump()
            response = await self.client.post("https://api.earthmc.net/v4/nations", json=payload)

        # Raise on error
        if response.status_code != 200:
            raise httpx.HTTPStatusError(f"Unexpected status code: {response.status_code, response.text}", request=response.request, response=response)

        # Validate both responses
        if mode == "overview":
            overview_nations: list[NamedEntity] = [NamedEntity.model_validate(nation) for nation in track(response.json(),
            description="[green] Loading and validating nation overviews... [/green]")]
            return overview_nations

        elif mode == "detailed":
            detailed_nations: list[Nation] = [Nation.model_validate(nation) for nation in track(response.json(),
                description="[green] Loading and validating nation details... [/green]")]
            return NationResponse(nations=detailed_nations)

    # If no input return a list of Named entity (name and uuid)
    @overload
    async def get_players(self) -> list[NamedEntity]: ...

    # Otherwise return a Player Response
    @overload
    async def get_players(self, player_request: str | list[str]) -> PlayerResponse: ...

    async def get_players(self, player_request: str | list[str] | None = None) -> list[NamedEntity] | PlayerResponse:  # type: ignore[misc]
        """
        Get information about players.
        If you want to query a specific player, provide the player request parameters.
        You can provide either the player name or UUID.

        Note:
            Calling without arguments performs a GET request to
            https://api.earthmc.net/v4/players returning a name/UUID list.
            Passing a request performs a POST request to
            https://api.earthmc.net/v4/players returning full player data.

        Args:
            player_request (str | list[str] | None):
                The player request parameters. Can be a single name, UUID or a
                list of names. When None, an overview is returned.

        Returns:
            list[NamedEntity] | PlayerResponse:
                It returns a list of NamedEntity when no request is provided,
                and a PlayerResponse when a request is provided.

        Raises:
            httpx.HTTPStatusError: If the request fails.

        Examples:
            ```python
                emc_client = EmcClient()
                players = await emc_client.get_players()
                print(players)
            ```

            ```python
                emc_client = EmcClient()
                players = await emc_client.get_players("RafaCabra")
                players.show()
            ```
        """
        # If no input perform a GET request
        if player_request is None:
            mode: RequestMode = "overview"
            response = await self.client.get("https://api.earthmc.net/v4/players")

        # Otherwise a POST request
        else:
            mode = "detailed"

            if isinstance(player_request, str):
                player_query = NamedRequest(query=[player_request])

            else:
                player_query = NamedRequest(query=player_request)

            payload = player_query.model_dump()
            response = await self.client.post("https://api.earthmc.net/v4/players", json=payload)

        # Raise on error
        if response.status_code != 200:
            raise httpx.HTTPStatusError(f"Unexpected status code: {response.status_code, response.text}", request=response.request, response=response)

        # Validate responses
        if mode == "overview":
            overview_players: list[NamedEntity] = [NamedEntity.model_validate(player) for player in track(response.json(),
                description="[green] Loading and validating player details... [/green]")]
            return overview_players

        elif mode == "detailed":
            detailed_players: list[Player] = [Player.model_validate(player) for player in track(response.json(),
                description="[green] Loading and validating player details... [/green]")]
            return PlayerResponse(players=detailed_players)
