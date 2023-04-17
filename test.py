# pip3 install -U pyrogram
# pip3 install -U tgcrypto
import constants as c
import asyncio
from pyrogram import Client

api_id = c.API_ID
api_hash = c.API_HASH


async def main():
	async with Client("my_account", api_id, api_hash) as app:
		await app.send_message("me", "Greetings from **Pyrogram**!")


asyncio.run(main())