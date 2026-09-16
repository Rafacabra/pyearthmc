
import pytest
from httpx import AsyncClient, MockTransport, Response

from pyearthmc import EmcClient
from pyearthmc.models.common import NamedRequest
from pyearthmc.models.nations import NationResponse
from pyearthmc.models.players import PlayerResponse
from pyearthmc.models.server import ServerResponse
from pyearthmc.models.towns import TownResponse


@pytest.fixture
def server_payload() -> dict:
    return {
        "version": "1.20.4",
        "moonPhase": "FULL_MOON",
        "timestamps": {"newDayTime": 1000, "serverTimeOfDay": 500},
        "status": {"hasStorm": False, "isThundering": False},
        "stats": {
            "time": 100,
            "fullTime": 200,
            "maxPlayers": 100,
            "numOnlinePlayers": 10,
            "numOnlineNomads": 2,
            "numResidents": 500,
            "numNomads": 20,
            "numTowns": 30,
            "numTownBlocks": 1000,
            "numNations": 5,
            "numQuarters": 40,
            "numCuboids": 10,
        },
        "voteParty": {"target": 100, "numRemaining": 60},
    }


@pytest.fixture
def town_overview_payload() -> list[dict]:
    return [{"name": "Colombia", "uuid": "1111"}, {"name": "Springfield", "uuid": "2222"}]


@pytest.fixture
def town_detail_payload() -> dict:
    return {
        "name": "Colombia",
        "uuid": "1111",
        "board": "Welcome!",
        "founder": "RafaCabra",
        "wiki": None,
        "mayor": {"name": "RafaCabra", "uuid": "3333"},
        "nation": {"name": None, "uuid": None},
        "timestamps": {"registered": 1000, "joinedNationAt": None, "ruinedAt": None},
        "status": {
            "isPublic": True,
            "isOpen": True,
            "isNeutral": False,
            "isCapital": False,
            "isOverclaimed": None,
            "isRuined": False,
            "isForSale": False,
            "hasNation": False,
            "hasOverclaimShield": None,
            "canOutsiderSpawn": None,
        },
        "stats": {
            "numTownBlocks": 100,
            "maxTownBlocks": 200,
            "numResidents": 5,
            "numTrusted": 10,
            "numOutlaws": 1,
            "balance": 1000,
            "forSalePrice": None,
        },
        "coordinates": {
            "spawn": {"world": "earth", "x": 1.0, "y": 64, "z": 2.0, "pitch": 0.0, "yaw": 90.0},
            "homeBlock": (1, 2),
            "townBlocks": [(1, 2), (3, 4)],
        },
        "residents": [{"name": "RafaCabra", "uuid": "3333"}],
        "trusted": None,
        "outlaws": None,
        "quarters": None,
        "ranks": {},
    }


def build_client(handler) -> EmcClient:
    transport = MockTransport(handler)
    return EmcClient(AsyncClient(transport=transport))


class TestServerInfo:
    async def test_returns_server_response(self, server_payload):
        def handler(request):
            return Response(200, json=server_payload)

        client = build_client(handler)
        result = await client.get_server_info()

        assert isinstance(result, ServerResponse)
        assert result.version == "1.20.4"
        assert result.voteParty.target == 100
        assert result.voteParty.numVotes == 40
        assert result.metadata.response_arrived is not None

    async def test_raises_on_non_200(self, server_payload):
        def handler(request):
            return Response(500, json={})

        client = build_client(handler)
        with pytest.raises(Exception):
            await client.get_server_info()


class TestTowns:
    async def test_overview_returns_entities(self, town_overview_payload):
        def handler(request):
            assert request.method == "GET"
            return Response(200, json=town_overview_payload)

        client = build_client(handler)
        result = await client.get_towns()

        assert len(result) == 2
        assert result[0].name == "Colombia"

    async def test_detailed_returns_town_response(self, town_detail_payload):
        def handler(request):
            assert request.method == "POST"
            assert request.url.path == "/v4/towns"
            return Response(200, json=[town_detail_payload])

        client = build_client(handler)
        result = await client.get_towns(mode="detailed", town_request=NamedRequest(query=["Colombia"]))

        assert isinstance(result, TownResponse)
        assert result.towns[0].name == "Colombia"
        assert result.towns[0].mayor.name == "RafaCabra"

    async def test_detailed_without_request_raises(self):
        client = EmcClient(AsyncClient(transport=MockTransport(lambda r: Response(200, json=[]))))
        with pytest.raises(ValueError):
            await client.get_towns(mode="detailed")


class TestNations:
    async def test_detail_returns_nation_response(self):
        payload = {
            "name": "Amazon",
            "uuid": "aaaa",
            "board": "Hello",
            "dynmapColour": "#ff0000",
            "dynmapOutline": "#00ff00",
            "wiki": None,
            "king": {"name": "King", "uuid": "bbbb"},
            "capital": {"name": "Metro", "uuid": "cccc"},
            "timestamps": {"registered": 100},
            "status": {"isPublic": True, "isOpen": True, "isNeutral": False},
            "stats": {
                "numTownBlocks": 10,
                "numResidents": 20,
                "numTowns": 3,
                "numAllies": 1,
                "numEnemies": 0,
                "balance": 500,
            },
            "coordinates": {"spawn": {"world": "earth", "x": 1.0, "y": 64, "z": 1.0, "pitch": 0.0, "yaw": 0.0}},
            "residents": [{"name": "King", "uuid": "bbbb"}],
            "towns": [{"name": "Metro", "uuid": "cccc"}],
            "allies": None,
            "enemies": None,
            "sanctions": None,
            "ranks": {},
        }

        client = build_client(lambda r: Response(200, json=[payload]))
        result = await client.get_nations(mode="detailed", nation_request=NamedRequest(query=["Amazon"]))

        assert isinstance(result, NationResponse)
        assert result.nations[0].king.name == "King"

    async def test_detail_without_request_raises(self):
        client = EmcClient(AsyncClient(transport=MockTransport(lambda r: Response(200, json=[]))))
        with pytest.raises(ValueError):
            await client.get_nations(mode="detailed")


class TestPlayers:
    async def test_detail_returns_player_response(self):
        payload = {
            "name": "RafaCabra",
            "uuid": "dddd",
            "title": None,
            "surname": None,
            "formatted_name": "[RafaCabra]",
            "about": None,
            "town": {"name": "Colombia", "uuid": "1111"},
            "nation": {"name": None, "uuid": None},
            "timestamps": {"registered": 100, "joinedTownAt": 200, "lastOnline": 300},
            "status": {
                "isOnline": True,
                "isNPC": False,
                "isMayor": True,
                "isKing": False,
                "hasTown": True,
                "hasNation": False,
            },
            "stats": {"balance": 10, "numFriends": 2},
            "ranks": {"townRanks": ["Mayor"], "nationRanks": []},
            "friends": [{"name": "Friend", "uuid": "eeee"}],
            "discord": None,
        }

        client = build_client(lambda r: Response(200, json=[payload]))
        result = await client.get_players(mode="detailed", player_request=NamedRequest(query=["RafaCabra"]))

        assert isinstance(result, PlayerResponse)
        assert result.players[0].status.isOnline is True

    async def test_detail_without_request_raises(self):
        client = EmcClient(AsyncClient(transport=MockTransport(lambda r: Response(200, json=[]))))
        with pytest.raises(ValueError):
            await client.get_players(mode="detailed")
