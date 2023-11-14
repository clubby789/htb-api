import asyncio
import hackthebox
import os

async def main():
    client = hackthebox.HTBClient(os.environ["APP_TOKEN"])
    print(await client.do_get_request("user/profile/basic/1"))

asyncio.run(main())
