import logging as log
import os
import sys
import time as time_os
from logging.handlers import RotatingFileHandler

from telethon import TelegramClient, events

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

client = TelegramClient('session_name', c.API_ID, c.API_HASH)
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


@client.on(events.NewMessage(c.C1))
@client.on(events.NewMessage(c.C2))
@client.on(events.NewMessage(c.C3))
@client.on(events.NewMessage(c.C4))
async def on_new_msg_c1(event):
	log.info(f'Got new Message from {event.chat.username}, setting it as read')
	channel = await client.get_entity(event.chat.username)
	await client.send_read_acknowledge(channel)


version = get_version()
log.info(f'Starting PersonalTelegramOrganizer, {version}')
client.run_until_disconnected()
