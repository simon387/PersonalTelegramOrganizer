import logging as log
from logging.handlers import RotatingFileHandler

from pyrogram import Client

import Constants

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
	level=Constants.LOG_LEVEL
)

counter = 0
app = Client("session_name", Constants.API_ID, Constants.API_HASH)


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	return firstline


@app.on_message()
async def on_message_set_it_as_read(client, message):
	channel = message.chat.username
	if channel in Constants.channels.split(","):
		global counter
		counter += 1
		log.info(f"Setting channels {channel} as read! counter = {counter}, APP_VERSION = {client.APP_VERSION}")
		await app.read_chat_history(channel)


version = get_version()
log.info(f'Starting PersonalTelegramOrganizer, {version}')
app.run()
