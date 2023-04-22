import logging as log
import os
import sys
import time as time_os
from logging.handlers import RotatingFileHandler

from pyrogram import Client

import constants as c

log.basicConfig(
	handlers=[
		RotatingFileHandler(
			'_PersonalTelegramOrganizer.log',
			maxBytes=10240000,
			backupCount=5
		),
		log.StreamHandler()
	],
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level=c.LOG_LEVEL
)

counter = 0
app = Client("session_name", c.API_ID, c.API_HASH)


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


@app.on_message()
async def on_message_set_it_as_read(client, message):
	channel = message.chat.username
	if channel in c.channels.split(","):
		global counter
		counter += 1
		log.info(f"Setting channels {channel} as read! counter = {counter}")
		await app.read_chat_history(channel)


version = get_version()
log.info(f'Starting PersonalTelegramOrganizer, {version}')
app.run()
