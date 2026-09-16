import asyncio

from pyfiglet import figlet_format
from rich import print
from rich.progress import track
from rich.prompt import Prompt

from pyearthmc import EmcClient
from pyearthmc.models.towns import TownResponse


async def main():
    """
    Asks the user for a town name and prints the names of the residents in that town.
    if the resident is RafaCabra, prints a special message.
    """

    print(f"[purple]{figlet_format('pyEMC', font='larry3d')}")

    emc_client = EmcClient()

    all_towns = await emc_client.get_towns()
    print(
        "[red] Please have in mind that if this takes more time to run is because of Rich library's print that is used in the examples."
        " It adds color and is completely optional [/red]"
    )

    print(all_towns)


    town_name = Prompt.ask("[bold][yellow]Enter the name of the town[/yellow][/bold]")
    town_details: TownResponse = await emc_client.get_towns(town_request=town_name)


    town_details.show()
    residents = town_details.towns[0].residents
    for resident in track(residents, description="printing the names of the residents ..."):
        if resident.name == "RafaCabra":
            print(f"[purple]{resident.name} lives in Colombia and he developed this library[/purple]")

        else:
            print(f"[green]{resident.name} is an amazing resident![/green]")


    print(f"[purple] Town name: {town_details.towns[0].name}")
    print(f"[purple] Town board: {town_details.towns[0].board}")
    print(f"[purple] Town founder: {town_details.towns[0].founder}")

    print("[bold][yellow][italic]The test ran without errors[/italic][/yellow][/bold]")




if __name__ == "__main__":
    asyncio.run(main())
