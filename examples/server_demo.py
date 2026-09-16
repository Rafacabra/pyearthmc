
import asyncio

from pyfiglet import figlet_format
from rich import print

from pyearthmc.client import EmcClient


async def main():
    print(f"[purple]{figlet_format('pyEMC', font='larry3d')}")

    emc_client = EmcClient()
    server_response = await emc_client.get_server_info()
    server_response.show()

if __name__ == "__main__":
    asyncio.run(main())
