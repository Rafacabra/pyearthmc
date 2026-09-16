
from pyearthmc.models.common import NamedRequest
from pyearthmc.models.server import ServerResponse, VotepartyStatus


class TestServerModels:
    def test_voteparty_num_votes_computed(self):
        vp = VotepartyStatus(target=100, numRemaining=60)
        assert vp.numVotes == 40

    def test_server_response_has_response_arrived(self):
        response = ServerResponse.model_validate(
            {
                "version": "1.20.4",
                "moonPhase": "FULL_MOON",
                "timestamps": {"newDayTime": 1, "serverTimeOfDay": 2},
                "status": {"hasStorm": False, "isThundering": False},
                "stats": {
                    "time": 1,
                    "fullTime": 2,
                    "maxPlayers": 100,
                    "numOnlinePlayers": 1,
                    "numOnlineNomads": 1,
                    "numResidents": 1,
                    "numNomads": 1,
                    "numTowns": 1,
                    "numTownBlocks": 1,
                    "numNations": 1,
                    "numQuarters": 1,
                    "numCuboids": 1,
                },
                "voteParty": {"target": 100, "numRemaining": 60},
            }
        )
        assert response.metadata.response_arrived is not None


class TestNamedRequest:
    def test_query(self):
        req = NamedRequest(query=["Colombia", "Springfield"])
        assert req.query == ["Colombia", "Springfield"]
        assert req.model_dump() == {"query": ["Colombia", "Springfield"]}
