from telethon import TelegramClient

import constants as c

if __name__ == '__main__':
	api_id = c.API_ID
	api_hash = c.API_HASH

	client = TelegramClient('session_name', api_id, api_hash)
	client.start()
