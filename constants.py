import configparser
import logging

config = configparser.RawConfigParser()
config.read("config.properties")
# application's secrets
SECRETS = "secrets"
API_ID = config.get(SECRETS, "api.id")
API_HASH = config.get(SECRETS, "api.hash")
# application's settings
APPLICATION = "application"
case = config.get(APPLICATION, "log.level")
if case == "info":
	LOG_LEVEL = logging.INFO
elif case == "debug":
	LOG_LEVEL = logging.DEBUG
elif case == "error":
	LOG_LEVEL = logging.ERROR
else:
	LOG_LEVEL = logging.DEBUG
# channels and group
CHANNELS_AND_GROUPS = 'channels_and_groups'
C1 = config.get(CHANNELS_AND_GROUPS, "c1")
C2 = config.get(CHANNELS_AND_GROUPS, "c2")
C3 = config.get(CHANNELS_AND_GROUPS, "c3")
C4 = config.get(CHANNELS_AND_GROUPS, "c4")
