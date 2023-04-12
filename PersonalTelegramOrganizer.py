import asyncio
from asyncio import sleep

from telethon import TelegramClient

import constants as c

api_id = c.API_ID
api_hash = c.API_HASH

client = TelegramClient('session_name', api_id, api_hash)
client.start()


async def main():
	while True:
		channel = await client.get_entity('offertepromozioniscontibaby')
		await client.send_read_acknowledge(channel)
		print ("ciao")
		await sleep(3) # sleep for a min

	# messages = await client.get_messages(channel, limit=50)  # pass your own args
	#
	# # then if you want to get all the messages text
	# for x in messages:
	# 	print(x.text)  # return message.text


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
#
# if __name__ == '__main__':
# 	loop = asyncio.new_event_loop()
# 	asyncio.set_event_loop(loop)
# 	try:
# 		asyncio.run(main( ))
# 	except KeyboardInterrupt:
# 		pass