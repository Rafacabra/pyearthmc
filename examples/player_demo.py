import asyncio

from pyfiglet import figlet_format
from rich import print
from rich.progress import track
from rich.prompt import Prompt

from pyearthmc import EmcClient
from pyearthmc.models.players import PlayerResponse


async def main():
    """
    Asks the user for a player name and prints the details of that player.
    if the player is RafaCabra, prints a special message.
    """

    print(f"[purple]{figlet_format('pyEMC', font='larry3d')}")

    emc_client = EmcClient()

    all_players = await emc_client.get_players()
    print(
        "[red] Please have in mind that if this takes more time to run is because of rich's print that is used in the examples."
        " It adds color and is completely optional [/red]"
    )
    print(all_players)


    player_name = Prompt.ask("[bold][yellow]Enter the name of the player[/yellow][/bold]")
    player_details: PlayerResponse = await emc_client.get_players(player_request=player_name)


    player_details.show()
    residents = player_details.players

    for resident in track(residents, description="printing the names of the residents ..."):
        if resident.name == "RafaCabra":
            print(f"[purple]{resident.name} lives in Colombia and he developed this library[/purple]")

        else:
            print(f"[green]{resident.name} is an amazing resident![/green]")


    print(f"[purple] Player name: {player_details.players[0].name}")
    print(f"[purple] Player surname: {player_details.players[0].surname}")
    print(f"[purple] Player formatted name: {player_details.players[0].formatted_name}")
    print(f"[purple] Player about: {player_details.players[0].about}")
    print(f"[purple] Player town: {player_details.players[0].town}")
    print(f"[purple] Player nation: {player_details.players[0].nation}")
    print(f"[purple] Player timestamps: {player_details.players[0].timestamps}")
    print(f"[purple] Player status: {player_details.players[0].status}")
    print(f"[purple] Player stats: {player_details.players[0].stats}")
    print(f"[purple] Player ranks: {player_details.players[0].ranks}")
    print(f"[purple] Player friends: {player_details.players[0].friends}")
    print(f"[purple] Player discord: {player_details.players[0].discord}")

    print("[bold][yellow][italic]The test ran without errors[/italic][/yellow][/bold]")




if __name__ == "__main__":
    asyncio.run(main())
