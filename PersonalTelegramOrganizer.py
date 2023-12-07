import logging as log
from logging.handlers import RotatingFileHandler

import pyrogram
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


def get_version():
	with open("changelog.txt") as f:
		firstline = f.readline().rstrip()
	return firstline


@app.on_message()
async def on_message_set_it_as_read(client, message):
	log.info("|")
	channel = message.chat.username
	log.info(f"Got message from this channel: {channel}")

	if channel == 'cascorossoclub':
		await app.read_chat_history(channel)
		return

	if channel in Constants.channels.split(","):
		log.info(f"Channel {channel} found in the black list! Setting it as read!")
		log.debug(f"{client.APP_VERSION} - Setting channels {channel} as read! message = {message}")
		await app.read_chat_history(channel)

		top = message.reply_to_top_message_id
		if top:
			topic_id = top
		else:
			topic_id = message.reply_to_message_id

		# pyrogram.raw.functions.messages.ReadDiscussion()
		# await app.read_chat_history(message.link.replace('https://t.me/', ''))
		# await client.invoke('ReadDiscussion(message.id)')
		# await app.invoke(ReadDiscussion(peer=Client.resolve_peer(peer_id=message.chat.id, self=message.chat.id), msg_id=message.id, read_max_id=2**31-1))

		# Use await with client.invoke() instead of app.invoke()
		# await client.invoke(ReadDiscussion(peer=Client.resolve_peer(peer_id=message.chat.id, self=message.chat.id), msg_id=message.id, read_max_id=2**31-1))
		# await client.invoke(ReadDiscussion(peer=await Client.resolve_peer(peer_id=message.chat.id, self=message.chat.id), msg_id=message.id, read_max_id=2**31-1))

		# Resolve the peer, ensuring to use `await` as it might be asynchronous
		# resolved_peer = await client.resolve_peer(peer_id=message.chat.id, self=message.chat.id)
		resolved_peer = await client.resolve_peer(peer_id=message.chat.id)
		log.info("________________________________")
		log.info(f"resolved peer= {resolved_peer}")
		log.info("________________________________")
		log.info(f"message.id= {message.id}")
		log.info("________________________________")
		# Use the resolved peer in ReadDiscussion
		try:
			await client.invoke(ReadDiscussion(peer=resolved_peer, msg_id=message.id, read_max_id=2**31-1))
		except BadRequest as e:
			log.error(f"Telegram API error: {e}")
			# Add additional logging or handling as needed

	else:
		log.info(f"Channel {channel} NOT found in the black list! Nothing to do...")


log.info(f'Starting PersonalTelegramOrganizer, {get_version()}')
app.run()

# 'https://t.me/salottoprogrammatori/331685'