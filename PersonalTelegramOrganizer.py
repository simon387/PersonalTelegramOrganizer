import logging as log
from logging.handlers import RotatingFileHandler

from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.raw.functions.messages import ReadDiscussion
from pyrogram.raw.functions.channels import GetForumTopics

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
	#
	# Topic's management - Following code block is just for topic's chat
	#
	topic_ids = [t.id for t in await get_topics(app, chat_id)]
	if len(topic_ids) > 0:
		resolved_peer = await client.resolve_peer(peer_id=message.chat.id)
		for topic_id in topic_ids:
			await client.invoke(ReadDiscussion(peer=resolved_peer, msg_id=topic_id, read_max_id=2 ** 31 - 1))


async def get_topics(client, chat_id):
	topics = []
	date, offset, offset_topic, total = 0, 0, 0, 0

	while True:
		r = await client.invoke(
			GetForumTopics(
				channel=await client.resolve_peer(chat_id),
				offset_date=date,
				offset_id=offset,
				offset_topic=offset_topic,
				limit=100
			)
		)
		if not total: total = r.count
		topic_list = r.topics
		if not topic_list or len(topics) >= total: break
		topics.extend(topic_list)

		last = topic_list[-1]
		offset_topic, offset = last.id, last.top_message
		date = {m.id: m.date for m in r.messages}.get(offset, 0)
		log.info(f"topics_id found: {topics}")
	return topics


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
