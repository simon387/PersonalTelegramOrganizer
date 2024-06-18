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
log.info(f"blacklist={blacklist}")


@app.on_message()
async def on_message_set_it_as_read(client, message):
	channel = message.chat.username
	chat_id = message.chat.id
	await refresh_chats(channel)  # for better management
	log.info(f"Got message from channel: {channel}")
	if channel not in blacklist:
		log.info(f"Channel {channel} NOT found in the blacklist! Nothing to do...")
		return
	# channel is in the blacklist
	log.info(f"Channel {channel} found in the blacklist! Setting it as read!")
	log.debug(f"{client.APP_VERSION} - Setting channel {channel} as read! message = {message}")
	await app.read_chat_history(chat_id)  # this fails if it's a topic's chat
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
	# END topic's management
	except BadRequest as e:
		log.error(f"Telegram API error: {e}")
	except AttributeError as e:
		log.debug(f"Telegram error: {e}. Ignore this if {channel} doesn't have topics!")
	except Exception as e:
		log.error(f"Telegram error: {e}. This need to be investigated!")


async def refresh_chats(channel):
	try:
		chat = await app.get_chat(channel)
		log.debug(chat)
	except BadRequest as e:
		log.error(f"Telegram API error: {e}")


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	return firstline


log.info(f'Starting PersonalTelegramOrganizer, {get_version()}')
app.run()
