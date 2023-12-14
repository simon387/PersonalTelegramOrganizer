import logging as log
from logging.handlers import RotatingFileHandler

from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw.functions.messages import ReadDiscussion

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

app = Client("default_session", Constants.API_ID, Constants.API_HASH)
blacklist = Constants.channels.split(",")


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	return firstline


@app.on_message()
async def on_message_set_it_as_read(client, message):
	log.info("|")
	channel = message.chat.username
	log.info(f"Got message from this channel: {channel}")
	if channel not in blacklist:
		log.info(f"Channel {channel} NOT found in the blacklist! Nothing to do...")
		return
	# channel is in the blacklist
	log.info(f"Channel {channel} found in the blacklist! Setting it as read!")
	log.debug(f"{client.APP_VERSION} - Setting channels {channel} as read! message = {message}")
	await app.read_chat_history(channel)  # it fails if is a topic's chat
	# START topic's management - Following code block is just for topic's chat
	top = message.reply_to_top_message_id
	if top:
		topic_id = top
	else:
		topic_id = message.reply_to_message_id
	resolved_peer = await client.resolve_peer(peer_id=message.chat.id)
	log.debug(f"resolved_peer= {resolved_peer}")
	log.debug(f"message.id= {message.id}")
	try:
		await client.invoke(ReadDiscussion(peer=resolved_peer, msg_id=topic_id, read_max_id=2 ** 31 - 1))
	except BadRequest as e:
		log.error(f"Telegram API error: {e}")
	except Exception as e:
		log.error(f"Telegram error: {e}. Ignore this if {channel} doesn't have topics!")
	# END topic's management


log.info(f'Starting PersonalTelegramOrganizer, {get_version()}')
app.run()
