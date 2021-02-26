import asyncio


async def main(client):
    print(await client.user)

if __name__ == "__main__":
    from base import client as example_client
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(example_client))
