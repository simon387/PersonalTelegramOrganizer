import asyncio
import logging as log
import os
import sys
import time as time_os
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


async def custom_exception_handler(loop_, context) -> None:
	# first, handle with default handler
	loop_.default_exception_handler(context)
	exception = context.get('exception')
	if isinstance(exception, ValueError):
		log.error(context['exception'])
	# Restart the bot
	time_os.sleep(5.0)
	os.execl(sys.executable, sys.executable, *sys.argv)


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
		await sleep(16)


version = get_version()
log.info("Starting PersonalTelegramOrganizer, " + version)
loop = asyncio.get_event_loop()
loop.set_exception_handler(custom_exception_handler)
loop.run_until_complete(main())
# loop.create_task(main())
# loop.run_forever()
