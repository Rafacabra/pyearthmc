import asyncio

from pyfiglet import figlet_format
from rich import print
from rich.progress import track
from rich.prompt import Prompt

from pyearthmc import EmcClient
from pyearthmc.models.nations import NationResponse


async def main():
    """
    Asks the user for a nation name and prints the names of the residents in that nation.
    if the resident is RafaCabra, prints a special message.
    """

    print(f"[purple]{figlet_format('pyEMC', font='larry3d')}")

    emc_client = EmcClient()

    all_nations = await emc_client.get_nations()
    print(
        "[red] Please have in mind that if this takes more time to run is because of rich's print that is used in the examples."
        " It adds color and is completely optional [/red]"
    )

    print(all_nations)


    nation_name = Prompt.ask("[bold][yellow]Enter the name of the nation[/yellow][/bold]")
    nation_details: NationResponse = await emc_client.get_nations(nation_name)


    nation_details.show()
    residents = nation_details.nations[0].residents
    for resident in track(residents, description="printing the names of the residents ..."):
        if resident.name == "RafaCabra":
            print(f"[purple]{resident.name} lives in Colombia and he developed this library[/purple]")

        else:
            print(f"[green]{resident.name} is an amazing resident![/green]")


    print(f"[purple] Nation name: {nation_details.nations[0].name}")
    print(f"[purple] Nation board: {nation_details.nations[0].board}")
    print(f"[purple] Nation king: {nation_details.nations[0].king.name}")

    print("[bold][yellow][italic]The test ran without errors[/italic][/yellow][/bold]")




if __name__ == "__main__":
    asyncio.run(main())
