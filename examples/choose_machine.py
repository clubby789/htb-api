import random
import asyncio


async def main(client):
    machines = await client.get_machines()
    print(f"Chosen Machine: {random.choice(machines)}")

if __name__ == "__main__":
    from base import client as example_client
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(example_client))
