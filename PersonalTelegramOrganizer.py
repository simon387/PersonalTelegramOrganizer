import asyncio
import logging as log
from asyncio import sleep
from logging.handlers import RotatingFileHandler

from telethon import TelegramClient

import constants as c

log.basicConfig(
	handlers=[
		RotatingFileHandler(
			'PersonalTelegramOrganizer.log',
			maxBytes=10240000,
			backupCount=5
		),
		log.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=c.LOG_LEVEL
)

api_id = c.API_ID
api_hash = c.API_HASH

client = TelegramClient('session_name', api_id, api_hash)
client.start()


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	return firstline


async def main():
	while True:
		log.info("New loop!")
		channel = await client.get_entity('offertepromozioniscontibaby')
		await client.send_read_acknowledge(channel)
		channel = await client.get_entity('scontioffertepromozionicuracorpo')
		await client.send_read_acknowledge(channel)
		channel = await client.get_entity('offertescontipromozionielettro')
		await client.send_read_acknowledge(channel)
		channel = await client.get_entity('schedevideooffertepromozioni')
		await client.send_read_acknowledge(channel)
		await sleep(8)

version = get_version()
log.info("Starting PersonalTelegramOrganizer, " + version)
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
